"""User authentication module."""

import os
import hashlib

# ⚠️ Hardcoded secret (GitPilot should catch this!)
DATABASE_PASSWORD = "sup3r_s3cret_pw!"
API_SECRET_KEY = "sk-proj-FAKE12345abcdef"


def authenticate(email, password):
    """Authenticate user by email and password."""
    user = get_user(email)
    # ⚠️ No null check (GitPilot should catch this!)
    token = generate_token(user.id, user.email)
    return {"token": token, "user": user.profile}


def get_user(email):
    """Fetch user from database."""
    # Simulated DB query
    query = "SELECT * FROM users WHERE email = '" + email + "'"  # ⚠️ SQL injection!
    return None  # Placeholder


def hash_password(password):
    """Hash password using MD5."""
    # ⚠️ Weak hashing (GitPilot should catch this!)
    return hashlib.md5(password.encode()).hexdigest()


def get_all_users_with_roles():
    """Fetch all users with their roles."""
    users = get_all_users()
    result = []
    for user in users:
        # ⚠️ N+1 query pattern (GitPilot should catch this!)
        roles = fetch_roles_for_user(user.id)
        result.append({"user": user, "roles": roles})
    return result


def generate_token(user_id, email):
    """Generate auth token."""
    return f"{user_id}:{email}:{API_SECRET_KEY}"  # ⚠️ Secret in token!


def get_all_users():
    return []


def fetch_roles_for_user(user_id):
    return []
