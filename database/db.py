import os
import mysql.connector
from dotenv import load_dotenv

from .constants import TABLE_CREATE_QUERY_MAP, DROP_TABLES

load_dotenv()


def get_connection():
    """
    Get the database connection.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection or None: A MySQL database connection or None if there was an error.
    """
    try:
        return mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
        )
    except Exception as e:
        print(f"Error creating database connection: {str(e)}")
        return None


connection = get_connection()


def execute_create_table_queries(queries):
    """
    Execute create table queries.

    Args:
        queries (list): A list of SQL CREATE TABLE queries to be executed.

    Returns:
        None
    """
    try:
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error executing queries: {str(e)}")


def execute_select_query(query, values=None):
    """
    Execute a SELECT query.

    Args:
        query (str): The SQL SELECT query.
        values (tuple, optional): Values to be used as query parameters. Default is None.

    Returns:
        list or None: A list of query results or None if there was an error.
    """
    if connection is not None:
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            connection.close()
            return None


def setup_db():
    """
    Set up the database with fresh tables.

    Returns:
        None
    """
    drop_tables(DROP_TABLES)
    execute_create_table_queries(TABLE_CREATE_QUERY_MAP)


def drop_tables(table_names):
    """
    Drop tables.

    Args:
        table_names (list): A list of table names to be dropped.

    Returns:
        None
    """
    try:
        cursor = connection.cursor()
        for table_name in table_names:
            drop_query = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_query)
        connection.commit()
        print("Tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {str(e)}")


def execute_insert_query(query, values):
    """
    Execute an INSERT query.

    Args:
        query (str): The SQL INSERT query.
        values (tuple): Values to be inserted into the database.

    Returns:
        None
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"Error executing INSERT query: {str(e)}")


def email_exists(email):
    """
    Check if an email exists in the database.

    Args:
        email (str): The email to check.

    Returns:
        bool: True if the email exists, False if not.
    """
    try:
        if connection is not None:
            cursor = connection.cursor()
            select_query = "SELECT * FROM User WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            return bool(result)  # True if email exists, False if not
    except Exception as e:
        print(f"Error checking email existence: {str(e)}")
    return False


def execute_update_query(query, values):
    """
    Execute an UPDATE query.

    Args:
        query (str): The SQL UPDATE query.
        values (tuple): Values to be updated in the database.

    Returns:
        None
    """
    try:
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            print("UPDATE query executed successfully.")
    except Exception as e:
        print(f"Error executing UPDATE query: {str(e)}")


def execute_delete_query(query, values):
    """
    Execute a DELETE query.

    Args:
        query (str): The SQL DELETE query.
        values (tuple): Values to be deleted from the database.

    Returns:
        None
    """
    try:
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            print("DELETE query executed successfully.")
    except Exception as e:
        print(f"Error executing DELETE query: {str(e)}")
