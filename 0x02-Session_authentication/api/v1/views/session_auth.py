#!/usr/bin/env python3
"""Module of session_id views
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_id():
    """ POST /api/v1/auth_session/login
    Return:
      - loggin user id
    """
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    foundUsers = User.search({'email': email})
    if not foundUsers:
        return jsonify({"error": "no user found for this email"}), 404

    for user in foundUsers:
        valid_passwd = user.is_valid_password(password)
    if valid_passwd is False:
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    SESSION_NAME = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def destroy_logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - deletes the user session/logout
    """
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)

    return jsonify({}), 200
