from connection import get_connection
from schema import SCHEMA


def initialize_database():

    conn = get_connection()

    conn.executescript(SCHEMA)

    conn.commit()

    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":

    initialize_database()