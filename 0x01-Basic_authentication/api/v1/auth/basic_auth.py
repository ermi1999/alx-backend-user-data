#!/usr/bin/env python3
"""Basic auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Baic auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts authorization header.
        """
        if not authorization_header or type(authorization_header) is not str:
            return None

        basic = authorization_header[:6]
        if basic != "Basic ":
            return None
        return authorization_header[6:]
