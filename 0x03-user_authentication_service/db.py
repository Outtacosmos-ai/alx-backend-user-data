#!/usr/bin/env python3
"""DB module for handling database operations"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class for database operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The user's email address
            hashed_password (str): The user's hashed password

        Returns:
            User: The newly created User object
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception as e:
            self._session.rollback()  # Rollback in case of failure
            raise e

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database by arbitrary attributes

        Args:
            **kwargs: Arbitrary keyword arguments to filter by

        Returns:
            User: The found User object

        Raises:
            NoResultFound: If no results are found
            InvalidRequestError: If invalid query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            raise e
        except Exception as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes

        Args:
            user_id: The ID of the user to update
            **kwargs: The fields to update

        Raises:
            ValueError: If an invalid field is passed
            NoResultFound: If the user is not found
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Invalid field {key}")
                setattr(user, key, value)
            self._session.commit()
        except Exception as e:
            self._session.rollback()  # Rollback if update fails
            raise e
