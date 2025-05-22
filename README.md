# E-Commerce Website with Django

![Project Preview](https://elshop.pythonanywhere.com)

A fully functional e-commerce website built with Django framework, featuring HTML, CSS, JavaScript for frontend and MySQL for database management.

## ✨ Key Features

- **Product Management**: Add, edit, and delete products with admin privileges
- **Shopping Cart**: Complete cart functionality with PayPal integration
- **User Authentication**: Secure registration, login, and password recovery 
- **Rating System**: Product reviews and ratings
- **Payment Gateway**: Secure PayPal payment processing
- **Admin Dashboard**: Comprehensive admin interface

## 🛠️ Technology Stack

### Frontend
- HTML5 (Semantic markup)
- CSS3 (Flexbox/Grid layouts)
- JavaScript (ES6+)
- JQuery

### Backend
- Python 3.x
- Django 3.x/4.x
- Django REST Framework (if applicable)
- Django Filter
- Django PayPal

### Database
- MySQL 8.0+

### Development Tools
- Git for version control
- Pipenv/Pip for package management

## 🚀 Installation Guide

### Prerequisites
- Python 3.8+
- MySQL Server
- PayPal developer account (for testing)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/cod-F123/django-shop.git
   cd django-shop

2. Set up virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Configure environment variables:
    ```bash
    # Edit .env file with your configurations

5. Database setup:
    ```bash
    python manage.py makemigrations
    python manage.py 
    
6. Create admin user:
    ```bash
    python manage.py createsuperuser

7. Run development server:
    ```bash
    python manage.py runserver