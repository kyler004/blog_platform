# Blog Platform API

A production-ready Django REST Framework API for a blog platform with comprehensive authentication, email verification, password reset, and advanced blog post management features.

## 🚀 Features

### Authentication & User Management

- 🔐 **JWT Authentication** with custom claims and token rotation
- ✉️ **Email Verification** for new user registrations
- 🔑 **Password Reset** functionality via email
- 👤 **User Profile Management** (view and update)
- 🛡️ **Enhanced Security** with password validation and username restrictions

### Blog Post Management

- 📝 **Markdown Support** for rich content formatting
- 🔍 **Advanced Filtering** by author, publication status, and date
- 🔎 **Full-Text Search** across titles and content
- 📄 **Pagination** (10 posts per page)
- 📊 **Draft Management** - separate endpoint for unpublished posts
- 🎯 **SEO-Friendly URLs** with auto-generated slugs
- 🔒 **Permission System** - author-only editing and deletion

### API Features

- 📚 **Interactive API Documentation** (Swagger UI & ReDoc)
- 🌐 **CORS Support** for frontend integration
- ⚡ **Rate Limiting** (100/hour anonymous, 1000/hour authenticated)
- 📖 **OpenAPI Schema** generation
- 🔄 **API Versioning** (v1)

## 📋 Tech Stack

- **Django 6.0** - Web framework
- **Django REST Framework** - API toolkit
- **djangorestframework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS handling
- **django-filter** - Advanced filtering
- **drf-spectacular** - API documentation
- **python-markdown** - Markdown rendering
- **python-dotenv** - Environment variable management
- **Pillow** - Image handling
- **SQLite** - Database (development)

## 📁 Project Structure

```
blog_platform/
├── blog_platform_api/          # Django project
│   ├── accounts/               # User authentication app
│   │   ├── models.py          # Custom User model
│   │   ├── serializers.py     # Auth serializers (Register, Profile, Password Reset)
│   │   ├── views.py           # Auth views
│   │   ├── utils.py           # Email utilities
│   │   ├── urls.py            # Auth endpoints
│   │   └── templates/         # Email templates
│   ├── blog/                  # Blog app
│   │   ├── models.py          # Post model with slug and indexes
│   │   ├── serializers.py     # Post serializer with validation
│   │   ├── views.py           # Post viewset with filtering/search
│   │   ├── permissions.py     # Custom permissions
│   │   ├── admin.py           # Admin configuration
│   │   └── urls.py            # Blog endpoints
│   ├── blog_platform_api/     # Project settings
│   │   ├── settings.py        # Configuration (JWT, CORS, Security)
│   │   └── urls.py            # Main URL routing
│   ├── logs/                  # Application logs
│   ├── media/                 # User-uploaded files
│   └── manage.py
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository:**

```bash
cd /home/kyler/Documents/React/backend/blog_platform
```

2. **Create and activate virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create environment file:**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Navigate to project directory:**

```bash
cd blog_platform_api
```

6. **Run migrations:**

```bash
python manage.py migrate
```

7. **Create a site object (required for email verification):**

```bash
python manage.py shell
```

Then in the shell:

```python
from django.contrib.sites.models import Site
Site.objects.create(domain='localhost:8000', name='Blog Platform')
exit()
```

8. **Create a superuser (optional):**

```bash
python manage.py createsuperuser
```

9. **Run the development server:**

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔧 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings (comma-separated origins)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Frontend URL (for email verification links)
FRONTEND_URL=http://localhost:3000

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📡 API Endpoints

### Base URL

```
http://127.0.0.1:8000/api/v1/
```

### Authentication Endpoints

#### Register New User

```http
POST /api/v1/auth/register/
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Response:** `201 Created`

```json
{
  "message": "User registered successfully. Please check your email to verify your account."
}
```

**Validation:**

- Email must be unique and valid
- Username: alphanumeric, underscore, hyphen only
- Password: Django's built-in validators (min 8 chars, not too common, etc.)
- Passwords must match

---

#### Verify Email

```http
GET /api/v1/auth/verify-email/<uidb64>/<token>/
```

**Response:** `200 OK`

```json
{
  "message": "Email verified successfully. You can now login."
}
```

---

#### Login

```http
POST /api/v1/auth/login/
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`

```json
{
  "refresh": "eyJhbGci...",
  "access": "eyJhbGci..."
}
```

**JWT Payload includes:**

- `user_id`
- `email`
- `username`
- `is_superuser`
- `exp` (expires in 15 minutes)

---

#### Refresh Token

```http
POST /api/v1/auth/token/refresh/
```

**Request Body:**

```json
{
  "refresh": "eyJhbGci..."
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci..." // New refresh token (rotation enabled)
}
```

---

#### Get User Profile

```http
GET /api/v1/auth/profile/
Authorization: Bearer <access_token>
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2026-01-13T10:00:00Z"
}
```

---

#### Update User Profile

```http
PUT/PATCH /api/v1/auth/profile/
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "username": "newusername",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Note:** Email and date_joined are read-only.

---

#### Request Password Reset

```http
POST /api/v1/auth/password-reset/
```

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`

```json
{
  "message": "Password reset email sent. Please check your email."
}
```

---

#### Confirm Password Reset

```http
POST /api/v1/auth/password-reset-confirm/<uidb64>/<token>/
```

**Request Body:**

```json
{
  "password": "NewSecurePass123!",
  "password_confirm": "NewSecurePass123!"
}
```

**Response:** `200 OK`

```json
{
  "message": "Password reset successfully. You can now login with your new password."
}
```

---

### Blog Post Endpoints

#### List All Posts (Paginated)

```http
GET /api/v1/posts/
```

**Query Parameters:**

- `page` - Page number (default: 1)
- `author` - Filter by author ID
- `is_published` - Filter by publication status (true/false)
- `search` - Search in title, content, author username/email
- `ordering` - Order by field (prefix with `-` for descending)
  - Options: `created_at`, `updated_at`, `title`
  - Example: `-created_at` (newest first)

**Example Requests:**

```http
GET /api/v1/posts/?page=2
GET /api/v1/posts/?author=1&is_published=true
GET /api/v1/posts/?search=django
GET /api/v1/posts/?ordering=-created_at
GET /api/v1/posts/?search=python&ordering=-created_at&page=1
```

**Response:** `200 OK`

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/v1/posts/?page=3",
  "previous": "http://127.0.0.1:8000/api/v1/posts/?page=1",
  "results": [
    {
      "id": 1,
      "author": "user@example.com",
      "author_username": "username",
      "title": "My First Post",
      "slug": "my-first-post",
      "content": "# Hello World\n\nThis is **markdown**!",
      "rendered_content": "<h1>Hello World</h1>\n<p>This is <strong>markdown</strong>!</p>",
      "created_at": "2026-01-13T10:00:00Z",
      "updated_at": "2026-01-13T10:00:00Z",
      "is_published": true
    }
  ]
}
```

---

#### Create New Post

```http
POST /api/v1/posts/
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "title": "My First Post",
  "content": "# Hello World\n\nThis is **markdown**!",
  "is_published": true
}
```

**Validation:**

- Title: 5-200 characters
- Content: minimum 10 characters
- Slug: auto-generated from title

**Response:** `201 Created`

---

#### Get Post Details

```http
GET /api/v1/posts/{id}/
```

**Response:** `200 OK` (same structure as list item)

---

#### Update Post

```http
PUT/PATCH /api/v1/posts/{id}/
Authorization: Bearer <access_token>
```

**Permission:** Only the author can update their posts.

**Request Body:**

```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "is_published": true
}
```

---

#### Delete Post

```http
DELETE /api/v1/posts/{id}/
Authorization: Bearer <access_token>
```

**Permission:** Only the author can delete their posts.

**Response:** `204 No Content`

---

#### Get My Drafts

```http
GET /api/v1/posts/my_drafts/
Authorization: Bearer <access_token>
```

**Description:** Returns all unpublished posts by the authenticated user.

**Response:** `200 OK` (paginated list of posts)

---

#### Publish a Post

```http
POST /api/v1/posts/{id}/publish/
Authorization: Bearer <access_token>
```

**Permission:** Only the author can publish their posts.

**Response:** `200 OK` (updated post object)

---

#### Unpublish a Post

```http
POST /api/v1/posts/{id}/unpublish/
Authorization: Bearer <access_token>
```

**Permission:** Only the author can unpublish their posts.

**Response:** `200 OK` (updated post object)

---

### API Documentation Endpoints

#### OpenAPI Schema

```http
GET /api/schema/
```

Returns the complete OpenAPI 3.0 schema in JSON format.

---

#### Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

Interactive API documentation with request/response examples and testing capabilities.

---

#### ReDoc

```
http://127.0.0.1:8000/api/redoc/
```

Alternative API documentation with a clean, three-panel design.

---

### Admin Panel

```
http://127.0.0.1:8000/admin/
```

Django admin interface for managing users and posts.

**Features:**

- User management with email-based authentication
- Post management with filtering, search, and date hierarchy
- Read-only timestamps
- Organized fieldsets

## 🔒 Security Features

### Development Mode (DEBUG=True)

- Console email backend (emails printed to terminal)
- Permissive CORS and CSRF settings
- Detailed error pages

### Production Mode (DEBUG=False)

- ✅ **SSL Redirect** - Force HTTPS
- ✅ **Secure Cookies** - Session and CSRF cookies over HTTPS only
- ✅ **HSTS** - HTTP Strict Transport Security (1 year, with subdomains and preload)
- ✅ **XSS Filter** - Browser XSS protection
- ✅ **Content Type Sniffing Protection**
- ✅ **JWT Token Rotation** - Refresh tokens rotate on use
- ✅ **Token Blacklisting** - Old tokens invalidated after rotation
- ✅ **Rate Limiting** - Prevent abuse (100/hour anon, 1000/hour auth)
- ✅ **Password Validation** - Strong password requirements
- ✅ **CORS Whitelist** - Only allowed origins can access API

## 📊 Database Schema

### User Model

- **Fields:** email (unique, USERNAME_FIELD), username, password, first_name, last_name, is_active, date_joined
- **Authentication:** Email-based login
- **Verification:** Email verification required (is_active flag)

### Post Model

- **Fields:** author (FK to User), title, slug (auto-generated), content (markdown), created_at, updated_at, is_published
- **Indexes:**
  - Single: author, created_at, is_published
  - Composite: (created_at, is_published), (author, is_published)
- **Ordering:** Newest first (-created_at)

## 🧪 Testing the API

### Using cURL

**Register:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

**Login:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Create Post:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "My First Post",
    "content": "# Hello World\n\nThis is **markdown**!",
    "is_published": true
  }'
```

**Search Posts:**

```bash
curl "http://127.0.0.1:8000/api/v1/posts/?search=django&ordering=-created_at"
```

### Using Swagger UI

1. Navigate to `http://127.0.0.1:8000/api/docs/`
2. Click "Authorize" and enter your JWT token
3. Try out any endpoint with the interactive interface

## 📝 Logging

Logs are stored in `blog_platform_api/logs/django.log`

**Log Levels:**

- Django framework: INFO
- Accounts app: DEBUG
- Blog app: DEBUG

**What's logged:**

- Authentication attempts
- API errors
- Database queries (in DEBUG mode)
- Email sending

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure strong `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_HOSTS` with your domain
- [ ] Configure `CORS_ALLOWED_ORIGINS` with frontend domain
- [ ] Set `FRONTEND_URL` to production frontend URL
- [ ] Configure production email backend (SMTP)
- [ ] Use PostgreSQL or MySQL instead of SQLite
- [ ] Run `python manage.py collectstatic`
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure proper WSGI/ASGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Enable database backups
- [ ] Set up monitoring and error tracking
- [ ] Review and adjust rate limiting settings

## 📄 License

MIT

## 👨‍💻 Author

Created with Django REST Framework

---

## 🆘 Troubleshooting

### "No module named 'django'"

Make sure you've activated your virtual environment:

```bash
source venv/bin/activate
```

### "You have unapplied migrations"

Run migrations:

```bash
python manage.py migrate
```

### "SITE_ID not found"

Create a site object as described in the installation steps.

### CORS errors from frontend

Make sure `CORS_ALLOWED_ORIGINS` in `.env` includes your frontend URL.

### Email verification not working

Check that `FRONTEND_URL` is set correctly in `.env` and matches your frontend application URL.
