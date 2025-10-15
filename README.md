# 0auth — Custom Authentication System (Django)

A production‑ready, fully customizable authentication module built with Python, HTML, and CSS. It includes email verification, user registration, login, logout, password reset via email, and change‑password flows, with secure defaults and clear separation of concerns.

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

- `INSTALLED_APPS` includes: `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.sessions`, `django.contrib.messages`, `django.contrib.staticfiles`, and the `accounts` app.
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

---

## URL Wiring

In the project’s `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # Routes provided by this module
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

Adjust names/paths to match your repo’s actual URLs.

---

## Authentication Flows

### 1) Registration with Email Verification

- User submits the registration form (`/accounts/register/`).
- A user record is created with `is_active=False`.
- A time‑limited tokenized verification link is emailed (built with `urlsafe_base64_encode(user.pk)` + `default_token_generator`).
- User clicks the link (`/accounts/verify/<uidb64>/<token>/`):
  - Token is validated; on success, user is activated (`is_active=True`).
  - The user is optionally auto‑logged in and redirected to the dashboard or login page.
- If a link is invalid/expired, show a helpful page and offer “Resend verification email.”

Notes:
- Tokens are single‑use and time‑limited by Django’s password reset token mechanism and session salt rotation.

### 2) Login

- Login form at `/accounts/login/` supports email or username (depending on form configuration).
- “Remember me” checkbox controls session expiration:
  - If checked, use `SESSION_COOKIE_AGE` (e.g., 2 weeks).
  - If not, session expires at browser close (`SESSION_EXPIRE_AT_BROWSER_CLOSE=True` or per‑request).
- Inactive (unverified) accounts are not allowed to log in by default (configurable).

### 3) Logout

- Logout route at `/accounts/logout/`.
- Uses POST with CSRF protection (recommended). If you provide a GET link, ensure you warn about CSRF implications.

### 4) Password Reset (Forgot Password)

- Request form at `/accounts/password-reset/` takes email.
- An email is sent with a tokenized link:
  - `/accounts/password-reset/confirm/<uidb64>/<token>/`
- The link opens the set‑new‑password form. On success:
  - User is notified; tokens are invalidated; optionally auto‑login or redirect to login.
- Email content is customizable via templates (see “Emails”).

### 5) Change Password (Authenticated)

- Authenticated users visit `/accounts/password-change/`.
- They must enter their current password, a new password, and confirmation.
- On success:
  - User session is updated to avoid logout (`update_session_auth_hash`).
  - Redirect to `/accounts/password-change/done/`.

---

## Templates

- Located under `templates/accounts/` (or your chosen path).
- Override or customize:
  - `register.html`, `login.html`, `verify_email_sent.html`, `email_verification_invalid.html`, `email_verification_success.html`
  - `password_reset.html`, `password_reset_done.html`, `password_reset_confirm.html`, `password_reset_complete.html`
  - `password_change.html`, `password_change_done.html`
- Include clear form errors, CSRF tokens, and accessible markup.

---

## Emails

- Plain text templates under `accounts/emails/`:
  - `verification_subject.txt`
  - `verification_body.txt` (use placeholders like `{{ user }}`, `{{ verification_url }}`, `{{ site_name }}`)
- For password reset, Django uses built‑in templates if you use `PasswordResetView`. You can override with your own templates for full control.
- Development options:
  - Console backend: `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` (prints to console)
  - File backend: `django.core.mail.backends.filebased.EmailBackend`
  - MailHog: point SMTP to `localhost:1025`
  - Gmail: use an App Password (not your login)

---

## Forms and Validation

- Registration form validates:
  - Unique email/username
  - Password strength (Django password validators)
  - Terms/consent (optional)
- Login form supports email or username; rate limiting can be added via throttling middleware or third‑party apps.
- Password reset and change use Django’s validators and token mechanisms.

---

## Security Best Practices

- Enforce HTTPS in production (`SECURE_SSL_REDIRECT`, HSTS, secure cookies).
- Keep `SECRET_KEY` secret; rotate on compromise.
- Use Django’s password validators and strong policy.
- Use POST for logout to mitigate CSRF.
- Limit token lifetime by periodically rotating salts; tokens are already time‑sensitive.
- Don’t leak account existence:
  - For password reset and registration confirmation pages, display generic success messages.
- Consider adding:
  - Account lockout after repeated failed logins
  - 2FA or WebAuthn (optional)
  - ReCAPTCHA on high‑risk endpoints

---

## Extensibility

- Custom user model:
  - Use `AbstractUser` (simple) or `AbstractBaseUser` (full control).
  - Set `AUTH_USER_MODEL = "accounts.CustomUser"`.
- Signals:
  - Send verification email on post‑save for new users, or trigger from the registration view.
- Adapters/Hooks:
  - Override form clean methods, success redirects, and email composition.

---

## Running Tests

If tests are included:

- Run: `pytest` or `python manage.py test`
- Add environment variables for test email backend and settings overrides as needed.

---

## Deployment Notes

- Use a production database (PostgreSQL).
- Set `DEBUG=False`, proper `ALLOWED_HOSTS`.
- Configure SMTP or an email provider (SendGrid, Mailgun, SES).
- Run `python manage.py collectstatic`.
- Set secure cookie and HSTS settings.
- Use a WSGI/ASGI server (gunicorn/uvicorn) behind a reverse proxy (nginx).

---

## Troubleshooting

- Not receiving emails:
  - Use console backend to verify templates first.
  - Check SMTP creds, ports, TLS/SSL.
  - Verify `DEFAULT_FROM_EMAIL` and provider domain verification.
- Invalid verification or reset link:
  - Token expired; resend.
  - Check that `SITE_DOMAIN` and `SITE_SCHEME` match the link you expect.
- Login failing after password change:
  - Ensure `update_session_auth_hash(request, user)` is called after setting a new password.
- “User already exists”:
  - Enforce unique email or adjust unique constraints/forms.

---

## Contributing

- Open an issue or PR describing changes you’d like to make.
- Follow existing code style and add/adjust tests for new behavior.
- Keep security in mind when changing auth flows.

---

## License

Add your license here (e.g., MIT). If none is specified, please include one for clarity.

---

## Acknowledgements

- Built on Django’s robust auth and token utilities.
- HTML/CSS templates designed for clarity and accessibility.

---

Need help tailoring this to the exact code in this repo? Open an issue or ask for a PR to wire everything up and push this README directly.
