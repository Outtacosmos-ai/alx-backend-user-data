#!/usr/bin/env python3
"""
Module for handling personal data and database operations
"""

import logging
import mysql.connector
import os
from typing import List

# PII fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    import re
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        repl = f'{field}={redaction}{separator}'
        message = re.sub(pattern, repl, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database
    """
    # Fetch environment variables
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Debug statements to check the environment variables
    print("Database Connection Details:")
    print("Username:", username)
    print("Password:", "*****" if password else "(empty)")
    print("Host:", host)
    print("Database Name:", db_name)

    if not db_name:
        raise ValueError("Environment variable PERSONAL_DATA_DB_NAME is not set")

    try:
        # Establish connection to the database
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        print("Connection to the database was successful.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        exit(1)  # Exit with error if connection fails


if __name__ == "__main__":
    try:
        # Get a database connection
        db = get_db()
        cursor = db.cursor()
        
        # Run a sample query
        cursor.execute("SELECT COUNT(*) FROM users;")
        for row in cursor:
            print("User count:", row[0])
            
        # Clean up
        cursor.close()
        db.close()
        print("Database connection closed.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
