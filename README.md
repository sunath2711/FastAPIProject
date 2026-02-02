# FastAPI Blog

A modern, full-stack blog application built with **FastAPI**, **SQLAlchemy**, and **Jinja2 templates**. This project demonstrates best practices for building web applications with both RESTful API endpoints and server-rendered HTML pages.

## 🎯 Project Overview

FastAPI Blog is a lightweight blogging platform that allows users to:
- Create and view user accounts
- Create, read, and browse blog posts
- View posts by specific users
- Access both web-based and JSON API interfaces

The application combines:
- **Backend API**: FastAPI with comprehensive REST endpoints
- **Frontend**: Server-rendered HTML with Jinja2 templates and Bootstrap styling
- **Database**: SQLite with SQLAlchemy ORM
- **Static Assets**: CSS, JavaScript, and user profile images

---

## 📁 Project Structure

```
fastAPIBlog/
├── main.py              # FastAPI application entry point with all routes
├── models.py            # SQLAlchemy ORM models (User, Post)
├── schemas.py           # Pydantic validation schemas
├── database.py          # Database configuration and session management
├── learning.md          # Development notes and learning documentation
├── templates/           # Jinja2 HTML templates
│   ├── layout.html      # Base template with common HTML structure
│   ├── home.html        # Home page with all posts
│   ├── post.html        # Individual post detail page
│   ├── user_posts.html  # User-specific posts page
│   ├── error.html       # Error page template
│   ├── home_raw.html    # Raw template (reference)
│   └── layout_raw.html  # Raw layout (reference)
├── static/              # Static assets (CSS, JavaScript, icons)
│   ├── css/
│   │   └── main.css     # Custom styling
│   ├── js/              # JavaScript files
│   ├── icons/           # Icon assets
│   └── profile_pics/    # Default profile images
├── media/               # User-uploaded content
│   └── profile_pics/    # User profile pictures
└── blog.db              # SQLite database (created at runtime)
```

---

## 🏗️ Architecture

### Database Models

#### User Model
```python
- id: Integer (Primary Key)
- username: String(50) - Unique, required
- email: String(120) - Unique, required
- image_file: String(200) - Optional profile picture
- posts: Relationship to Post (one-to-many)
```

#### Post Model
```python
- id: Integer (Primary Key)
- title: String(100) - Required
- content: Text - Required post content
- user_id: Integer (Foreign Key to User)
- date_posted: DateTime - Timestamp with timezone
- author: Relationship to User (many-to-one)
```

### API Endpoints

#### Web Pages (HTML Responses)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | Home page with all posts | 200 |
| GET | `/posts` | All posts (alias for home) | 200 |
| GET | `/posts/{post_id}` | Individual post details | 200/404 |
| GET | `/users/{user_id}/posts` | Posts by specific user | 200/404 |

#### API Endpoints (JSON Responses)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/users` | Create new user | 201/400 |
| GET | `/api/users/{user_id}` | Get user details | 200/404 |
| GET | `/api/users/{user_id}/posts` | Get user's posts (JSON) | 200/404 |
| POST | `/api/posts` | Create new post | 201/404 |
| GET | `/api/posts` | Get all posts (JSON) | 200 |
| GET | `/api/posts/{post_id}` | Get post details (JSON) | 200/404 |

### Validation Schemas

#### User Schemas
- **UserBase**: Common user fields (username, email)
- **UserCreate**: Used for POST requests
- **UserResponse**: API response with full user details including image path

#### Post Schemas
- **PostBase**: Common post fields (title, content)
- **PostCreate**: Used for POST requests (includes user_id)
- **PostResponse**: API response with full post details and author info

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd d:\fastAPIBlog
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy jinja2 pydantic python-multipart email-validator
   ```

### Running the Application

**Development mode** (with auto-reload):
```bash
fastapi dev main.py
```

**Production mode**:
```bash
uvicorn main.py:app --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Web Interface**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative API Docs**: http://127.0.0.1:8000/redoc (ReDoc)

---

## 🔧 Key Features

### 1. **Dual Interface**
   - Web pages for users (HTML responses)
   - JSON API for programmatic access
   - Route separation using `include_in_schema=False` for cleaner API documentation

### 2. **Template Inheritance**
   - Base `layout.html` template with common HTML structure
   - Child templates extend layout and override content blocks
   - Reduces code duplication across pages

### 3. **Database Features**
   - SQLite database with SQLAlchemy ORM
   - Foreign key relationships between User and Post
   - Automatic timestamps for posts (UTC timezone)
   - Database indexing for foreign keys and lookups

### 4. **Validation**
   - Pydantic schemas for request/response validation
   - Email validation using `EmailStr`
   - Field constraints (min/max length)
   - Automatic API documentation from schemas

### 5. **Error Handling**
   - Centralized exception handlers
   - Different responses for API vs web routes
   - User-friendly error pages
   - HTTP status codes (404, 400, 422)

### 6. **Static Assets**
   - Bootstrap 5 CSS framework for responsive design
   - Google Fonts (Montserrat, Nunito)
   - Custom CSS styling
   - Profile picture support with default fallback

---

## 📝 Usage Examples

### Creating a User via API
```bash
curl -X POST "http://127.0.0.1:8000/api/users" \
  -H "Content-Type: application/json" \
  -d {
    "username": "john_doe",
    "email": "john@example.com"
  }
```

### Creating a Post via API
```bash
curl -X POST "http://127.0.0.1:8000/api/posts" \
  -H "Content-Type: application/json" \
  -d {
    "title": "My First Post",
    "content": "This is the content of my blog post.",
    "user_id": 1
  }
```

### Fetching Data via API
```bash
# Get all posts
curl "http://127.0.0.1:8000/api/posts"

# Get specific user
curl "http://127.0.0.1:8000/api/users/1"

# Get user's posts
curl "http://127.0.0.1:8000/api/users/1/posts"
```

---

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap Components**: Cards, navigation, grid layout
- **Profile Pictures**: User avatars with default fallback image
- **Formatted Dates**: Posts display dates in human-readable format
- **Navigation Links**: Easy navigation between posts and users
- **Custom Styling**: Additional CSS in `/static/css/main.css`

---

## 🔐 Security Notes

- **Input Validation**: All inputs validated via Pydantic schemas
- **Email Validation**: Email addresses validated before storing
- **Unique Constraints**: Username and email must be unique
- **Foreign Key Validation**: Posts must reference valid users
- **Error Messages**: Generic error messages in production

### Future Improvements
- Add user authentication (password hashing, JWT tokens)
- Add authorization (users can only edit their own posts)
- Add CORS support for cross-origin requests
- Add rate limiting
- Add database transactions for data consistency

---

## 💾 Database

### SQLite Configuration
```python
# Located in database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
```

The database file (`blog.db`) is created automatically on first run. Tables are created based on the models defined in `models.py`.

### To Reset the Database
Delete `blog.db` and restart the application - a fresh database will be created.

---

## 📚 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Web framework for building APIs |
| **Uvicorn** | ASGI server for running FastAPI |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic** | Data validation and settings management |
| **Jinja2** | Template engine for HTML rendering |
| **SQLite** | Embedded database |
| **Bootstrap 5** | CSS framework for responsive UI |
| **Google Fonts** | Typography |

---

## 🎓 Learning Outcomes

This project demonstrates:
- Building modern REST APIs with FastAPI
- Database modeling with SQLAlchemy ORM
- Template rendering with Jinja2
- Request/response validation with Pydantic
- Exception handling strategies
- Separation of concerns (API routes vs web routes)
- Database relationships (one-to-many)
- Static file serving

---

## 📖 Additional Documentation

See `learning.md` for detailed notes on:
- FastAPI fundamentals
- Template inheritance concepts
- Database setup
- Development workflow

---

## 🚀 Next Steps / Features to Add

1. **Authentication & Authorization**
   - User login/logout
   - Password hashing with bcrypt
   - JWT tokens for API authentication
   - Permission-based access control

2. **Post Management**
   - Edit existing posts
   - Delete posts
   - Draft/published status
   - Categories/tags

3. **Comments System**
   - Comments on posts
   - Comment threads
   - Nested replies

4. **Search & Filtering**
   - Search posts by title/content
   - Filter by user
   - Pagination for large datasets

5. **Frontend Enhancement**
   - User dashboard
   - Post creation form
   - Rich text editor for post content
   - Like/favorite functionality

6. **Deployment**
   - Docker containerization
   - Deploy to cloud (Heroku, AWS, Railway)
   - Environment configuration

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created as a learning project for FastAPI and full-stack web development.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

---

## ❓ FAQ

**Q: How do I add a new route?**
A: Add a function decorated with `@app.get()` or `@app.post()` in `main.py`. For web pages, use `include_in_schema=False`.

**Q: How do I modify the database models?**
A: Edit `models.py`, then restart the application to create new tables automatically.

**Q: Can I use PostgreSQL instead of SQLite?**
A: Yes! Change the `SQLALCHEMY_DATABASE_URL` in `database.py` to a PostgreSQL connection string.

**Q: How do I upload user profile pictures?**
A: Currently, set the `image_file` field when creating a user. Upload handling would require additional file upload routes.

**Q: How do I add authentication?**
A: Install `python-jose` and `passlib`, then add login routes that generate JWT tokens.

---

Enjoy building with FastAPI! 🎉
