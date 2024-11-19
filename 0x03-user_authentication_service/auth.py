def valid_login(self, email: str, password: str) -> bool:
    """Validate login credentials.

    Args:
        email: User's email.
        password: User's password.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    try:
        user = self._db.find_user_by(email=email)
        hashed_pw = user.hashed_password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
    except NoResultFound:
        return False


def update_password(self, reset_token: str, password: str) -> None:
    """Update user's password.

    Args:
        reset_token: Password reset token.
        password: New password.

    Raises:
        ValueError: If reset token is invalid.
    """
    try:
        user = self._db.find_user_by(reset_token=reset_token)
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )
    except NoResultFound:
        raise ValueError
