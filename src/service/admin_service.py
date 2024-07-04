from src.repository.admin_repository_helper import save_admin, get_admin


def admin_signup(values):
    user = values['username']
    password = values['password']
    admin = save_admin(user, password)
    return admin if admin else None


def admin_login(user, password):
    admin = get_admin(user, password)
    return admin if admin else None
