#!/usr/bin/env python3
"""Basic auth
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64
        """
        if not base64_authorization_header or type(
                base64_authorization_header) is not str:
            return None
        try:
            result = base64.b64decode(
                    base64_authorization_header, validate=True)
            return result.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header)is not str or
                ":" not in decoded_base64_authorization_header):
            return (None, None)
        header = decoded_base64_authorization_header.split(':')
        return (header[0], header[1])
