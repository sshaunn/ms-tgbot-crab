from src.repository.admin_repository_helper import save_admin, get_admin, update_feature_toggle, get_feature_toggle


def admin_signup(values):
    user = values['username']
    password = values['password']
    admin = save_admin(user, password)
    return admin if admin else None


def admin_login(user, password):
    admin = get_admin(user, password)
    return admin if admin else None


def update_feature_toggler(feature_toggler, toggle):
    toggler = update_feature_toggle(feature_toggler, toggle)
    return toggler if toggler else None


def get_feature_toggler(feature_toggler):
    toggler = get_feature_toggle(feature_toggler)
    return toggler if toggler else None
