import sqlite3  # Ensure this is imported

def create_db():
    con = sqlite3.connect(database="student_results.db")
    cur = con.cursor()

    # Drop existing tables (optional, for testing purposes)
    cur.execute("DROP TABLE IF EXISTS course")
    cur.execute("DROP TABLE IF EXISTS course_id_tracker")
    cur.execute("DROP TABLE IF EXISTS student")
    cur.execute("DROP TABLE IF EXISTS result")
    cur.execute("DROP TABLE IF EXISTS users")

    # Create course table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY, 
            name TEXT, 
            duration TEXT, 
            charges TEXT, 
            description TEXT
        )
    """)

    # Create course_id_tracker table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course_id_tracker (
            cid INTEGER PRIMARY KEY
        )
    """)

    # Create student table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)

    # Create result table (with new columns for total and percentage)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            subject TEXT,
            marks_ob TEXT,
            full_marks TEXT,
            per TEXT,
            total_obtained REAL,
            total_marks REAL,
            percentage REAL
        )
    """)

    # Create report table
    cur.execute("""
                CREATE TABLE IF NOT EXISTS report (
                    rid INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll TEXT NOT NULL,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    total_obtained REAL NOT NULL,
                    total_marks REAL NOT NULL,
                    percentage REAL NOT NULL
                )
            """)


    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    con.commit()
    con.close()

# Run the function to initialize your DB
create_db()