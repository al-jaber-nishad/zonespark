from uuid import uuid4
from django.utils.text import slugify
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


def generate_unique_username(base_name):
    """
    Generate a unique username based on the provided base name without looping.
    """
    User = get_user_model()
    
    # Create a slugified version of the base name
    base_name = slugify(base_name).lower()
    if not base_name:  # Ensure base_name isn't empty after slugifying
        base_name = "user"

    # Append a short UUID segment to ensure uniqueness
    unique_username = f"{base_name}-{uuid4().hex[:8]}"

    try:
        # Attempt to create a user with this username to ensure it's unique
        if not User.objects.filter(username=unique_username).exists():
            return unique_username
    except IntegrityError:
        # Handle any rare cases where a collision still occurs
        return f"{base_name}-{uuid4().hex[:8]}"

    return unique_username