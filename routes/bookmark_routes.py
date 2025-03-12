"""
Routes for handling blog bookmarks.
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models import Bookmark, Blog
from flask_jwt_extended import jwt_required, get_jwt_identity

bookmark_bp = Blueprint("bookmarks", __name__)


@bookmark_bp.route("", methods=["GET"])
@jwt_required()
def get_bookmarks():
    """
    Get all bookmarks for the authenticated user.

    Returns:
        List of bookmarks.
    """
    user = get_jwt_identity()
    bookmarks = Bookmark.query.filter_by(user_id=user).all()
    # Filter out bookmarks with missing blogs
    valid_bookmarks = [
        {"id": bm.id, "title": bm.blog.title, "content": bm.blog.content} for bm in bookmarks if bm.blog is not None
    ]
    return jsonify(valid_bookmarks), 200


@bookmark_bp.route("", methods=["POST"])
@jwt_required()
def add_bookmark():
    """
    Add a new bookmark for a blog post.

    Returns:
        Success message.
    """
    data = request.json
    user = get_jwt_identity()
    blog_id = data.get("blog_id")

    # Validate the blog ID
    blog = Blog.query.filter_by(id=blog_id, is_public=True).first()
    if not blog:
        return jsonify({"message": "Blog does not exist or is not public"}), 404

    # Check if the bookmark already exists
    existing_bookmark = Bookmark.query.filter_by(user_id=user, blog_id=blog_id).first()
    if existing_bookmark:
        return jsonify({"message": "You have already bookmarked this blog"}), 400

    # Add the new bookmark
    new_bookmark = Bookmark(user_id=user, blog_id=blog_id)
    db.session.add(new_bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark added successfully"}), 201


@bookmark_bp.route("/<int:bookmark_id>", methods=["DELETE"])
@jwt_required()
def delete_bookmark(bookmark_id):
    """
    Delete a specific bookmark.

    Returns:
        Success or error message.
    """
    user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=user).first()

    if not bookmark:
        return jsonify({"message": "Bookmark not found or unauthorized"}), 404

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark deleted successfully"}), 200
