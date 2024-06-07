#!/usr/bin/env python3
"""Session auth"""
from .auth import Auth
import uuid
from flask import request
from models.user import User


class SessionAuth(Auth):
    """Session auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session for user"""
        if not user_id or type(user_id) is not str:
            return None
        _id = str(uuid.uuid4())
        self.user_id_by_session_id[f'{_id}'] = user_id
        return _id

    def destroy_session(self, request=None):
        """destroy session"""
        if not request:
            return False
        s_cookie = self.session_cookie(request)
        if not s_cookie:
            return False
        user_id = self.user_id_for_session_id(s_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[s_cookie]
        return True

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """get user id with session id"""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """get a user based on the session"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
