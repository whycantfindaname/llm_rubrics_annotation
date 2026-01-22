# `fastapi-trial-2025-07-03` Changelog

## `main`

### v0.0.1

- added `.gitignore` with boilerplate sorce control exclusions for FastAPI

### v0.0.2

- added `CHANGELOG.md` (this file)
- scaffolded FastAPI
- created Python virtual environment
- installed dependencies
- tested development server by checking OpenAPI docs: OK

### v0.1.0

- added views:
  - `app/static/login.html`
  - `app/static/dashboard.html`
- added route handlers:
  - `GET /login`
  - `POST /login`
  - `GET /dashboard`
- installed `python-multipart` for form parsing

### v0.1.1

- removed `required` from login form fields (will be part of a task to ensure fields are not empty)
