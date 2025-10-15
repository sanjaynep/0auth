# 0auth — Custom Authentication System (Django)

A production‑ready, fully customizable authentication module built with Python, HTML, and CSS. It includes email verification, user registration, login, logout, password reset via email, change password, and **social login** (Google, Facebook, GitHub, etc.).

If you are integrating this module into an existing project, you can drop in the `accounts` app (or similarly named app in this repo) and wire up the URLs, templates, and settings as described below.

> Note: This README assumes a Django stack based on the repository’s language composition (Python, HTML, CSS). If your stack differs, adapt the steps accordingly.

---

## Features

- User registration with email verification
- Login with email/username and “remember me” sessions
- Logout (CSRF‑protected)
- Password reset (email link with time‑limited token)
- Change password (requires current password)
- Resend verification email
- **Social login (Google, Facebook, GitHub, etc.)**
- Secure token generation/validation using Django’s standard utilities
- Accessible, responsive HTML/CSS templates
- Clear extension points for custom user model, forms, and email templates

---

## Tech Stack

- Python (Django)
- HTML templates (Django templating)
- CSS (vanilla or utility classes)
- SQLite for local development (PostgreSQL recommended for production)
- SMTP (or console backend) for emails
- **django-allauth or social-auth-app-django for social login**

---

## Project Structure (reference)

Your structure may look like:

```
.
├─ accounts/
│  ├─ migrations/
│  ├─ templates/
│  │  └─ accounts/
│  │     ├─ login.html
│  │     ├─ register.html
│  │     ├─ verify_email_sent.html
│  │     ├─ email_verification_invalid.html
│  │     ├─ email_verification_success.html
│  │     ├─ password_change.html
│  │     ├─ password_change_done.html
│  │     ├─ password_reset.html
│  │     ├─ password_reset_done.html
│  │     ├─ password_reset_confirm.html
│  │     └─ password_reset_complete.html
│  │     ├─ social_login.html          # Social login template
│  ├─ emails/
│  │  ├─ verification_subject.txt
│  │  └─ verification_body.txt
│  ├─ forms.py
│  ├─ models.py           # CustomUser (often extends AbstractUser)
│  ├─ tokens.py           # If you add custom token logic (optional)
│  ├─ urls.py
│  └─ views.py
├─ core/ or project_name/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py / asgi.py
├─ manage.py
├─ requirements.txt
└─ .env (not committed)
```

---

## Quick Start

1. Clone and enter the repo:
   - `git clone https://github.com/sanjaynep/0auth.git`
   - `cd 0auth`

2. Create and activate a virtual environment:
   - `python -m venv .venv`
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. Install dependencies:
   - `pip install -r requirements.txt`
   - **For social login:**  
     - `pip install django-allauth`  
     or  
     - `pip install social-auth-app-django`

4. Create a `.env` file (see “Configuration” below), then apply migrations:
   - `python manage.py migrate`

5. Create a superuser:
   - `python manage.py createsuperuser`

6. Run the server:
   - `python manage.py runserver`
   - Visit http://127.0.0.1:8000/

---

## Configuration (.env and settings)

Add a `.env` file in the project root (do not commit it). Example:

```
# Core
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# For SMTP, use:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.example.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your_username
# EMAIL_HOST_PASSWORD=your_password_or_app_password
# EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL="No Reply <no-reply@example.com>"

# Site
SITE_DOMAIN=localhost:8000
SITE_SCHEME=http
# In production:
# SITE_DOMAIN=yourdomain.com
# SITE_SCHEME=https
```

In `settings.py`, ensure:

- `INSTALLED_APPS` includes:  
  `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.sessions`, `django.contrib.messages`, `django.contrib.staticfiles`, the `accounts` app,  
  **and for social login:**  
  - `django.contrib.sites`  
  - `allauth`, `allauth.account`, `allauth.socialaccount`  
  - `allauth.socialaccount.providers.google` (and/or facebook, github, etc.)

- `SITE_ID = 1` (required for django-allauth)

- If using a custom user model:
  - `AUTH_USER_MODEL = "accounts.CustomUser"`

- Password validators:
  - `AUTH_PASSWORD_VALIDATORS = [...]` (use Django’s defaults for security)

- Email configuration reads from environment variables.

- Useful session settings:
  - `SESSION_COOKIE_SECURE = not DEBUG`
  - `CSRF_COOKIE_SECURE = not DEBUG`
  - `SECURE_HSTS_SECONDS` (production)
  - `SECURE_SSL_REDIRECT = not DEBUG`

- **Social login settings (django-allauth example):**
  ```python
  AUTHENTICATION_BACKENDS = (
      "django.contrib.auth.backends.ModelBackend",
      "allauth.account.auth_backends.AuthenticationBackend",
  )

  LOGIN_REDIRECT_URL = "/"
  ACCOUNT_EMAIL_VERIFICATION = "mandatory"
  ACCOUNT_EMAIL_REQUIRED = True
  SOCIALACCOUNT_PROVIDERS = {
      "google": {
          "SCOPE": ["profile", "email"],
          "AUTH_PARAMS": {"access_type": "online"},
      },
      # Add other providers here
  }
  ```

---

## URL Wiring

In the project’s `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # Routes provided by this module
    path("accounts/social/", include("allauth.socialaccount.urls")),  # Social login routes
]
```

Common routes exposed by `accounts.urls`:

- `accounts/register/`
- `accounts/login/`
- `accounts/logout/`
- `accounts/email/resend/`
- `accounts/verify/<uidb64>/<token>/`
- `accounts/password-reset/`
- `accounts/password-reset/done/`
- `accounts/password-reset/confirm/<uidb64>/<token>/`
- `accounts/password-reset/complete/`
- `accounts/password-change/`
- `accounts/password-change/done/`
- **Social routes (django-allauth):**
  - `/accounts/social/login/`
  - `/accounts/social/login/google/`
  - `/accounts/social/login/facebook/`
  - `/accounts/social/login/github/`
  - etc.

Adjust names/paths to match your repo’s actual URLs.

---

## Authentication Flows

### 1) Registration with Email Verification

*(See original section)*

### 2) Login

*(See original section)*

### 3) Social Login

- User clicks a “Login with Google/Facebook/GitHub” button on the login page.
- Redirected to the provider’s OAuth flow.
- On successful authentication, user is logged in and optionally registered if new.
- Email verification may still be required (configurable).
- Social accounts can be linked to existing user accounts.

**Template integration:**
Add social login buttons to `login.html` and/or a separate `social_login.html` template. Example:

```html
{% load socialaccount %}
<h3>Login with:</h3>
<a href="{% provider_login_url 'google' %}">Google</a>
<a href="{% provider_login_url 'facebook' %}">Facebook</a>
<a href="{% provider_login_url 'github' %}">GitHub</a>
```

### 4) Logout

*(See original section)*

### 5) Password Reset (Forgot Password)

*(See original section)*

### 6) Change Password (Authenticated)

*(See original section)*

---

## Templates

- Located under `templates/accounts/` (or your chosen path).
- Override or customize:
  - `register.html`, `login.html`, `verify_email_sent.html`, `email_verification_invalid.html`, `email_verification_success.html`
  - `password_reset.html`, `password_reset_done.html`, `password_reset_confirm.html`, `password_reset_complete.html`
  - `password_change.html`, `password_change_done.html`
  - `social_login.html` (add social login buttons and instructions)
- Include clear form errors, CSRF tokens, and accessible markup.

---

## Emails

*(See original section)*

---

## Forms and Validation

*(See original section)*

---

## Security Best Practices

*(See original section)*

- For social login, ensure callback URLs are set securely on provider dashboards and in settings.
- Review provider security options; avoid exposing sensitive scopes.

---

## Extensibility

- Custom user model
- Signals
- Adapters/Hooks
- **Social Account Adapters:**  
  Override `allauth.socialaccount.adapter.DefaultSocialAccountAdapter` for custom logic on social signup/login.

---

## Running Tests

*(See original section)*

---

## Deployment Notes

*(See original section)*

- For social login, set correct OAuth callback URLs and credentials for each provider in production.

---

## Troubleshooting

*(See original section)*

- Social login not working:
  - Check provider credentials and callback URLs.
  - Inspect error messages for OAuth flow.

---

## Contributing

*(See original section)*

---

## License

*(See original section)*

---

## Acknowledgements

- Built on Django’s robust auth and token utilities.
- **Social login powered by [django-allauth](https://github.com/pennersr/django-allauth) or [social-auth-app-django](https://github.com/python-social-auth/social-app-django).**
- HTML/CSS templates designed for clarity and accessibility.

---

Need help tailoring this to the exact code in this repo? Open an issue or ask for a PR to wire everything up and push this README directly.
