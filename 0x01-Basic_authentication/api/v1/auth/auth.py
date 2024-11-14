#!/usr/bin/env python3
"""
Auth class
"""

import re
from flask import request
from typing import TypeVar, List

User = TypeVar('User')


class Auth:
    """
    A class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if the given path requires authentication
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if re.match(f"^{excluded_path[:-1]}.*$", path):
                    return False
            elif path.rstrip('/') == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Returns the current user (None by default)
        """
        return None
