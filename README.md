# Blog Platform API

A production-ready Django REST Framework API for a blog platform with user authentication, email verification, and markdown support.

## Features

- 🔐 **JWT Authentication** with custom claims
- ✉️ **Email Verification** for new user registrations
- 📝 **Markdown Support** for blog posts
- 🔒 **Production Security** settings
- 👤 **Custom User Model** with email-based authentication
- 🛡️ **Permission System** (author-only editing)

## Tech Stack

- **Django 6.0** - Web framework
- **Django REST Framework** - API toolkit
- **djangorestframework-simplejwt** - JWT authentication
- **python-markdown** - Markdown rendering
- **python-dotenv** - Environment variable management
- **SQLite** - Database (development)

## Project Structure

```
blog_platform/
├── blog_platform_api/          # Django project
│   ├── accounts/               # User authentication app
│   │   ├── models.py          # Custom User model
│   │   ├── serializers.py     # Registration & JWT serializers
│   │   ├── views.py           # Auth views
│   │   ├── utils.py           # Email verification utility
│   │   └── urls.py            # Auth endpoints
│   ├── blog/                  # Blog app
│   │   ├── models.py          # Post model
│   │   ├── serializers.py     # Post serializer
│   │   ├── views.py           # Post viewset
│   │   ├── permissions.py     # Custom permissions
│   │   └── urls.py            # Blog endpoints
│   └── blog_platform_api/     # Project settings
│       ├── settings.py        # Configuration
│       └── urls.py            # Main URL routing
└── README.md
```

## Installation

### Prerequisites

- Python 3.12+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository:**

```bash
cd /home/kyler/Documents/React/backend/blog_platform
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install django djangorestframework djangorestframework-simplejwt python-dotenv markdown
```

4. **Navigate to project directory:**

```bash
cd blog_platform_api
```

5. **Run migrations:**

```bash
python manage.py migrate
```

6. **Create a superuser (optional):**

```bash
python manage.py createsuperuser
```

7. **Run the development server:**

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Environment Variables

Create a `.env` file in the project root for production:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email Configuration (for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## API Endpoints

### Authentication

| Method | Endpoint                                   | Description            | Auth Required |
| ------ | ------------------------------------------ | ---------------------- | ------------- |
| POST   | `/api/auth/register/`                      | Register new user      | No            |
| GET    | `/api/auth/verify-email/<uidb64>/<token>/` | Verify email           | No            |
| POST   | `/api/auth/login/`                         | Login & get JWT tokens | No            |
| POST   | `/api/auth/token/refresh/`                 | Refresh access token   | No            |

### Blog Posts

| Method    | Endpoint           | Description               | Auth Required |
| --------- | ------------------ | ------------------------- | ------------- |
| GET       | `/api/posts/`      | List all published posts  | No            |
| POST      | `/api/posts/`      | Create new post           | Yes           |
| GET       | `/api/posts/{id}/` | Get post details          | No            |
| PUT/PATCH | `/api/posts/{id}/` | Update post (author only) | Yes           |
| DELETE    | `/api/posts/{id}/` | Delete post (author only) | Yes           |

### Admin

| Method | Endpoint  | Description        |
| ------ | --------- | ------------------ |
| GET    | `/admin/` | Django admin panel |

## Usage Examples

### 1. Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "SecurePass123!"
  }'
```

### 2. Verify Email

Check your console for the verification link, then visit it or:

```bash
curl -X GET "http://127.0.0.1:8000/api/auth/verify-email/<uidb64>/<token>/"
```

### 3. Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**

```json
{
  "refresh": "eyJhbGci...",
  "access": "eyJhbGci..."
}
```

### 4. Create a Blog Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "My First Post",
    "content": "# Hello World\n\nThis is **markdown**!",
    "is_published": true
  }'
```

### 5. List Posts

```bash
curl -X GET http://127.0.0.1:8000/api/posts/
```

## Custom JWT Payload

The access token includes custom claims:

```json
{
  "token_type": "access",
  "user_id": "1",
  "email": "user@example.com",
  "username": "username",
  "is_superuser": false,
  "exp": 1736784000,
  "iat": 1736780400
}
```

## Security Features

### Development

- Console email backend (emails printed to terminal)
- Debug mode enabled
- Permissive ALLOWED_HOSTS

### Production (when `DEBUG=False`)

- ✅ SSL redirect enabled
- ✅ Secure cookies (session & CSRF)
- ✅ XSS filter enabled
- ✅ Content type sniffing protection
- ✅ Environment-based configuration
- ✅ Secret key from environment

## Models

### User Model

- Email-based authentication (USERNAME_FIELD = 'email')
- Required fields: email, username, password
- Email verification via `is_active` flag

### Post Model

- Fields: title, content, author, created_at, updated_at, is_published
- Markdown content with rendered HTML output
- Author-only edit/delete permissions

## Permissions

- **AllowAny**: Registration, login, list posts, view post details
- **IsAuthenticatedOrReadOnly**: Create posts (authenticated only)
- **IsAuthorOrReadOnly**: Edit/delete posts (author only)

## Development

### Run Tests

```bash
python manage.py test
```

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Admin Panel

1. Create superuser: `python manage.py createsuperuser`
2. Visit: `http://127.0.0.1:8000/admin/`

## Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_HOSTS` in `.env`
- [ ] Configure production email backend (SMTP)
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure CORS for frontend domain
- [ ] Set up rate limiting
- [ ] Enable database backups

## License

MIT

## Author

Created with Django REST Framework
