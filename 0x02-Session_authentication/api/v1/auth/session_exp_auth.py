#!/usr/bin/env python3
"""Session expiration"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """session auth"""
    def __init__(self):
        """initializer"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        if not session_id:
            return None
        session_d = self.user_id_by_session_id.get(session_id)
        if not session_d:
            return None
        if self.session_duration <= 0:
            return session_d.get('user_id')
        created_at = session_d.get('created_at')

        if not created_at:
            return None
        expired_date = created_at + timedelta(seconds=self.session_duration)

        if expired_date < datetime.now():
            return None
        return session_d.get('user_id')
