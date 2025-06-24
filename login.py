import os


def login_coto():
    dni = os.getenv("COTO_DNI")
    password = os.getenv("COTO_PASSWORD")
    if not dni or not password:
        raise ValueError("COTO credentials are not set in environment variables")
    # Placeholder: replace with actual login logic
    return {
        "dni": dni,
        "password": password,
    }


def login_carrefour():
    email = os.getenv("CARREFOUR_EMAIL")
    password = os.getenv("CARREFOUR_PASSWORD")
    if not email or not password:
        raise ValueError("Carrefour credentials are not set in environment variables")
    # Placeholder: replace with actual login logic
    return {
        "email": email,
        "password": password,
    }