#!/usr/bin/env python3
"""
Module for handling personal data
"""
import os
import mysql.connector


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    
    return db
