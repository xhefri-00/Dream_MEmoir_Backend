"""
Routes for handling blog-related actions.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Blog, Bookmark

blog_bp = Blueprint("blogs", __name__, url_prefix="/blogs")


@blog_bp.route("", methods=["GET"])
@jwt_required()
def get_blogs():
    """
    Retrieve all public blogs for the authenticated user.

    Returns:
        List of public blogs.
    """
    user = get_jwt_identity()
    if not user:
        return jsonify({"message": "Unauthorized access"}), 401

    # Fetch only public blogs for the feed
    blogs = Blog.query.filter_by(is_public=True).all()
    
    return jsonify(
        [
            {"id": blog.id, "title": blog.title, "content": blog.content, "user_id": blog.user_id}
            for blog in blogs
        ]
    ), 200


@blog_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_blogs_by_user(user_id):
    """
    Retrieve blogs by a specific user, ensuring privacy for private blogs.

    Args:
        user_id (int): The ID of the user whose blogs are being retrieved.

    Returns:
        List of blogs for the specified user.
    """
    user = get_jwt_identity()
    if int(user) != user_id:
        return jsonify({"message": "Unauthorized access"}), 403

    # Fetch all blogs by the user (private and public)
    blogs = Blog.query.filter_by(user_id=user_id).all()

    return jsonify(
        [
            {"id": blog.id, "title": blog.title, "content": blog.content, "is_public": blog.is_public}
            for blog in blogs
        ]
    ), 200



@blog_bp.route("", methods=["POST"])
@jwt_required()
def create_blog():
    """
    Create a new blog post.

    Returns:
        Success message.
    """
    data = request.json
    user = get_jwt_identity()
    if not all([data.get("title"), data.get("content")]):
        return jsonify({"message": "Title and content are required"}), 400

    new_blog = Blog(
        user_id=user, 
        title=data["title"], 
        content=data["content"], 
        is_public=data.get("is_public", False)
    )
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({"message": "Blog created successfully"}), 201


@blog_bp.route("/<int:blog_id>", methods=["PUT"])
@jwt_required()
def update_blog(blog_id):
    """
    Update an existing blog post.

    Returns:
        Success or error message.
    """
    data = request.json
    user = get_jwt_identity()
    blog = Blog.query.filter_by(id=blog_id, user_id=user).first()

    if not blog:
        return jsonify({"message": "Blog not found or unauthorized"}), 404

    blog.title = data.get("title", blog.title)
    blog.content = data.get("content", blog.content)
    blog.is_public = data.get("is_public", blog.is_public)
    db.session.commit()

    return jsonify({"message": "Blog updated successfully"}), 200


@blog_bp.route("/<int:user_id>/<int:blog_id>", methods=["DELETE"])
@jwt_required()
def delete_blog(user_id, blog_id):
    """
    Delete a blog post by user ID and blog ID, along with its related bookmarks.

    Args:
        user_id (int): The ID of the blog owner.
        blog_id (int): The ID of the blog to delete.

    Returns:
        Success or error message.
    """
    current_user = get_jwt_identity()

    try:
        # Ensure the logged-in user matches the provided user_id
        if int(current_user) != user_id:
            return jsonify({"message": "Unauthorized access"}), 403

        # Fetch the blog matching the ID and user ID
        blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()

        if not blog:
            return jsonify({"message": "Blog not found"}), 404

        # Delete related bookmarks for this blog
        Bookmark.query.filter_by(blog_id=blog_id).delete()

        # Proceed to delete the blog
        db.session.delete(blog)
        db.session.commit()

        return jsonify({"message": "Blog and related bookmarks deleted successfully"}), 200

    except ValueError:
        return jsonify({"message": "Invalid user ID or blog ID"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
