#!/usr/bin/env python3
"""
Main file for testing DB methods
"""

from db import DB
from user import User

my_db = DB()

# Test adding users
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)  # Should print 1

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)  # Should print 2
