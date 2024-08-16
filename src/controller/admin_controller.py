from flask import Blueprint, jsonify, request
from src.service.admin_service import admin_signup, admin_login, update_feature_toggler, get_feature_toggler


admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/signup', methods=["POST"])
def signup():
    req = request.json
    # user = req['username']
    # password = req['password']
    admin = admin_signup(req)
    if admin:
        return "OK", 201
    return {'err': 400, 'msg': 'error occurred'}, 400


@admin_blueprint.route('/login', methods=['POST'])
def login():
    req = request.json
    user = req['username']
    password = req['password']
    admin = admin_login(user, password)
    if admin:
        return "OK", 200
    return {'err': 404, 'msg': 'username or password is invalid'}, 404


@admin_blueprint.route('/toggler', methods=['POST'])
def update_feature_toggle():
    req = request.json
    toggler = req['feature_toggler']
    toggle = req['toggle']
    res = update_feature_toggler(toggler, toggle)
    if res:
        return "OK", 200
    return {'err': 400, 'msg': 'updating toggler failed'}, 400


@admin_blueprint.route('/gettoggler', methods=['POST'])
def get_feature_toggle():
    req = request.json
    toggler = req['feature_toggler']
    res = get_feature_toggler(toggler)
    if res:
        return res, 200
    return {'err': 400, 'msg': 'updating toggler failed'}, 400
