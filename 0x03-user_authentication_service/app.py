#!/usr/bin/env python3
"""basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from flask.globals import session
from werkzeug.utils import redirect
from auth import Auth
import requests


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """ Root path
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password) is False:
        abort(401)

    session = AUTH.create_session(email)
    response = make_response("")
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Log out
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    destroy_session = AUTH.destroy_session(user.id)
    return.redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """response to the GET /profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)    


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """generate token and respond with a 200 HTTP status
    """
    try:
        email = request.form.get('email')
    except KeyError:
        abort(403)
    try:
        reset = AUTH.reset_password(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """Update password
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message":"Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
