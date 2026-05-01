import sqlite3
import os



def create_dummy_db():
    db_folder = './databases'
    db_path = os.path.join(db_folder, 'users.db')

    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
        print(f"Created folder: {db_folder}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop table if it exists to start fresh
    cursor.execute("DROP TABLE IF EXISTS ACCOUNTS")

    cursor.execute("""
        CREATE TABLE ACCOUNTS (
            account_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            date_of_birth TEXT,
            last_four_digits TEXT
        )
    """)

    # Dummy daata
    dummy_users = [
        (1, 'Jack Jones', '12/1/1999', '8902'),
        (2, 'Sarah Smith', '05/22/1985', '3341'),
        (12, 'Leo Miller', '11/11/1992', '7760')
    ]

    cursor.executemany("INSERT INTO ACCOUNTS VALUES (?, ?, ?, ?)", dummy_users)
    
    conn.commit()
    conn.close()
    print("Database 'users.db' created and populated successfully!")
    return True

if __name__ == "__main__":
    res = create_dummy_db()
    if not res:
        print("Unsuccesful")
    input("\nTask finished. Press Enter to close this window...")