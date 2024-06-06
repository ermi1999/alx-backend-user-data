#!/usr/bin/env python3
"""Session auth"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Session auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session for user"""
        if not user_id or type(user_id) not str:
            return None
        _id = str(uuid.uuid4())
        self.user_id_by_session_id[f'{_id}'] = user_id
        return _id
