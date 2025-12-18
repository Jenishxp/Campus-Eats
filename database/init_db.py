from database.connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        sql_commands = f.read().split(";")

    for command in sql_commands:
        command = command.strip()
        if command:
            cursor.execute(command)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
