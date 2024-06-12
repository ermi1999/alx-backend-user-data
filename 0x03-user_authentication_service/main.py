#!/usr/bin/env python3
"""Integration test"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """integration test for user registration"""
    payload = {"email": email, "password": password}
    expected = {"email": email, "message": "user created"}
    response = requests.post(f'{URL}/users', data=payload)
    assert response.status_code == 200
    assert response.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """Test for logging in with wrong password
    """
    payload = {'email': email, 'password': password}
    res = requests.post(f'{URL}/sessions', data=payload)

    assert res.status_code == 401


def profile_unlogged() -> None:
    """Test user's profile unlogged
    """
    cookies = {'session_id': ""}
    response = requests.get(f'{URL}/profile', cookies=cookies)

    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Test for logging in
    """
    payload = {'email': email, 'password': password}
    response = requests.post(f'{URL}/sessions', data=payload)
    expected = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == expected

    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """Validate user's profile logged in
    """
    cookies = {'session_id': session_id}
    response = requests.get(f'{URL}/profile', cookies=cookies)
    expected = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == expected


def log_out(session_id: str) -> None:
    """Validate log out route handler
    """
    cookies = {'session_id': session_id}
    response = requests.delete(f'{URL}/sessions', cookies=cookies)
    expected = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == expected


def reset_password_token(email: str) -> str:
    """Validate reset password token
    """
    payload = {'email': email}
    response = requests.post(f'{URL}/reset_password', data=payload)

    token = response.json().get('reset_token')
    expected = {"email": email, "reset_token": token}

    assert response.status_code == 200
    assert response.json() == expected

    return token


def update_password(email: str,
                    reset_token: str,
                    new_password: str) -> None:
    """Test update password
    """

    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    response = requests.put(f'{URL}/reset_password', data=payload)
    expected = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == expected


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
