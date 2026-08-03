# 🛒 AlphaShop

AlphaShop is a simple e-commerce web application built with Django.

This project was developed to practice backend development with Django and build a complete CRUD application with user authentication, shopping cart management and order processing.

---

## Features

- User registration and authentication
- Product catalog
- Product detail page
- Shopping cart
- Quantity management
- Order checkout
- Order history
- Django administration panel
- Responsive interface

---

## Technologies

- Python / Django
- HTML5 / CSS3 / JavaScript
- SQLite (local development) / PostgreSQL (production)
- Gunicorn + WhiteNoise (production server & static files)
- Cloudinary (product image storage in production)
- Deployed on Render

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Alecdev-10/AlphaShop.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the environment file and keep the defaults for local development:

```bash
cp .env.example .env
```

Apply migrations:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Project Structure

```
AlphaShop/
├── alphaShop/
├── marketPlace/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── static/
    ├── context_processors.py
├── templates/
```

---

## Deployment

The app is set up to deploy on [Render](https://render.com) via `render.yaml`:

1. Push the repository to GitHub.
2. On Render, create a new **Blueprint** and point it at the repo — it will
   read `render.yaml` and provision a web service and a free Postgres
   database automatically.
3. In the service's environment settings, fill in the variables marked
   `sync: false` in `render.yaml`: `CLOUDINARY_CLOUD_NAME`,
   `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` (from a free
   [Cloudinary](https://cloudinary.com) account).
4. Deploy. The build step (`build.sh`) installs dependencies, runs
   `collectstatic`, and applies migrations automatically.

`DEBUG` defaults to `False` — it only needs to be set to `True` locally
(already done for you in `.env`). See `.env.example` for the full list of
environment variables used by the app.

---

## Screenshots

Coming soon.

---

## Author

Alecdev-10