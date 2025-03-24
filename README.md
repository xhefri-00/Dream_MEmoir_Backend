# 🌙 Dream MEmoir - Backend  

**Dream Memoir** is a personal blogging platform with a sleek UI for exploring, managing, and bookmarking blog posts. Built with React.js and TailwindCSS.  

---

## 🚀 Features  

✅ Read and explore blog posts  
✅ Save favorite blogs as bookmarks  
✅ View and manage saved bookmarks  
✅ Responsive and modern UI  
## 🛠 Tech Stack
- **Backend:** Flask, SQLAlchemy  
- **Database:** SQLite / PostgreSQL  
- **Authentication:** Flask-Login, bcrypt  
- **API Requests:** Axios
- **API Handling:** Flask-RESTful

## 🔗 API Endpoints Used
- POST :: /register :: Register a new user
- POST :: /login :: Log in a user and return a JWT token
##
- GET :: /blogs :: Fetch all public blogs
- GET :: /blogs/user/<int:user_id> :: List of blogs for the specified user
- POST :: /blogs :: Create a new blog post
- PUT :: /blogs/<int:blog_id> :: Update an existing blog post
- DELETE :: blogs/<int:user_id>/<int:blog_id> :: Delete a blog post by user ID and blog ID, along with its related bookmarks.
##
- GET :: /bookmarks :: Get all bookmarks for the authenticated user
- POST :: /bookmarks :: Add a new bookmark for a blog post
- DELETE :: /bookmarks/<int:bookmark_id> :: Delete a specific bookmark
---
## 📊 Database Schema

### 🗂 Users Table  
| Column        | Type           | Constraints       |  
|--------------|---------------|-------------------|  
| `id`        | `INTEGER`      | PRIMARY KEY       |  
| `username`  | `VARCHAR(80)`  | UNIQUE, NOT NULL |  
| `email`     | `VARCHAR(120)` | UNIQUE, NOT NULL |  
| `password_hash` | `VARCHAR(128)` | NOT NULL |

### 📝 Blogs Table  
| Column      | Type           | Constraints                  |  
|------------|---------------|------------------------------|  
| `id`       | `INTEGER`      | PRIMARY KEY                  |  
| `title`    | `VARCHAR(255)` | NOT NULL                     |  
| `content`  | `TEXT`         | NOT NULL                     |  
| `is_public` | `BOOLEAN`     | Default: False               |  
| `created_at` | `DATETIME`   | Default: CURRENT_TIMESTAMP   |  
| `user_id`  | `INTEGER`      | REFERENCES `user(id)`        |

### 🔖 Bookmarks Table  
| Column      | Type           | Constraints                  |  
|------------|---------------|------------------------------|  
| `id`       | `INTEGER`      | PRIMARY KEY                  |  
| `user_id`  | `INTEGER`      | REFERENCES `user(id)`        |  
| `blog_id`  | `INTEGER`      | REFERENCES `blog(id)`        |  

## 📥 Installation
### **1️⃣ Clone the Repository**  
git clone https://github.com/xhefri-00/Dream_MEmoir_Backend.git

cd dream-memoir-backend
### 2️⃣ Create Virtual Environment & Install Dependencies
python -m venv venv  
source venv/bin/activate  (# On Windows use: venv\Scripts\activate)
pip install -r requirements.txt  
### **3️⃣ Set Up Database
flask db init  
flask db migrate -m "Initial migration"  
flask db upgrade  
### **4️⃣ Run the Server
flask run
