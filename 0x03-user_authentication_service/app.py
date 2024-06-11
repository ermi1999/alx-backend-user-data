#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def root() -> str:
    """root route for flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """users function for registering users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions():
    """creates a new session for user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def del_sessions() -> str:
    """deletes a session"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('root'))
    abort(403)


@app.route('/profile', strict_slashes=False)
def get_profile() -> str:
    """gets a profile with session id"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
