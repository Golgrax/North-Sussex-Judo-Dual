import pyodbc
import hashlib

DATABASE_CONFIG = {
    'server': '310-06\\SQLEXPRESS05',  
    'database': 'Marvek',         
    'username': 'your_username',  
    'password': 'your_password',  
}

def create_connection():
    """Creates a database connection and returns it."""
    conn_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']};"
    )
    try:
        conn = pyodbc.connect(conn_string)
        return conn
    except pyodbc.Error as e:
        print("Error connecting to the database:", e)
        return None

def execute_sql_file(conn, sql_file):
    """Executes SQL commands from a given file."""
    with open(sql_file, 'r') as f:
        sql = f.read()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except pyodbc.Error as e:
        print("Error executing SQL file:", e)

def hash_password(password):
    """Hashes a password using SHA-256 for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Creates a new user with username and hashed password."""
    conn = create_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO Users (username, password) 
            VALUES (?, ?)
        """, (username, hashed_password))
        conn.commit()
        print("User created successfully.")
        return True
    except pyodbc.Error as e:
        print("Error creating user:", e)
        return False
    finally:
        conn.close()

def login(username, password):
    """Authenticates a user by checking username and password."""
    conn = create_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("""
            SELECT * FROM Users 
            WHERE username = ? AND password = ?
        """, (username, hashed_password))
        user = cursor.fetchone()
        return user
    except pyodbc.Error as e:
        print("Error during login:", e)
        return None
    finally:
        conn.close()

def fetch_weight_categories():
    """Fetches all weight categories."""
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_name FROM WeightCategories")
        categories = [row.category_name for row in cursor.fetchall()]
        return categories
    except pyodbc.Error as e:
        print("Error fetching weight categories:", e)
        return []
    finally:
        conn.close()

def fetch_training_plans():
    """Fetches all training plans."""
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT plan_name FROM TrainingPlans")
        training_plans = [row.plan_name for row in cursor.fetchall()]
        return training_plans
    except pyodbc.Error as e:
        print("Error fetching training plans:", e)
        return []
    finally:
        conn.close()

def add_athlete(name, training_plan, current_weight, competition_weight_category):
    """Adds a new athlete to the database."""
    conn = create_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Athletes (name, training_plan, current_weight, competition_weight_category) 
            VALUES (?, ?, ?, ?)
        """, (name, training_plan, current_weight, competition_weight_category))
        conn.commit()
        print("Athlete added successfully.")
        return True
    except pyodbc.Error as e:
        print("Error adding athlete:", e)
        return False
    finally:
        conn.close()


def add_training_plan(plan_name, weekly_fee):
     """Adds a new training plan to the database."""
     conn = create_connection()
     if not conn:
       return False
     cursor = conn.cursor()
     try:
         cursor.execute("INSERT INTO TrainingPlans (plan_name, weekly_fee) VALUES (?, ?)", (plan_name, weekly_fee))
         conn.commit()
         print("Training plan added successfully.")
         conn.close()
         return True
     except pyodbc.Error as e:
         print("Error adding training plan:", e)
         conn.rollback()
         conn.close()
         return False

def add_competition(competition_name, entry_fee, date):
    """Adds a new competition to the database."""
    conn = create_connection()
    if not conn:
       return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Competitions (competition_name, entry_fee, date) VALUES (?, ?, ?)", (competition_name, entry_fee, date))
        conn.commit()
        print("Competition added successfully.")
        conn.close()
        return True
    except pyodbc.Error as e:
        print("Error adding competition:", e)
        conn.rollback()
        conn.close()
        return False

def fetch_athletes():
    """Fetches all athletes."""
    conn = create_connection()
    if not conn:
       return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Athletes")
    athletes = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
      athletes.append(dict(zip(columns,row)))
    conn.close()
    return athletes

def fetch_competitions():
    """Fetches all competitions."""
    conn = create_connection()
    if not conn:
      return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, competition_name FROM Competitions")
    competitions = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
      competitions.append(dict(zip(columns, row)))
    conn.close()
    return competitions


def add_athlete_to_competition(athlete_id, competition_id):
    """Adds an athlete to a competition."""
    conn = create_connection()
    if not conn:
       return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO CompetitionAthletes (competition_id, athlete_id) VALUES (?, ?)", (competition_id, athlete_id))
        conn.commit()
        print("Athlete added to competition successfully.")
        conn.close()
        return True
    except pyodbc.Error as e:
         print("Error adding athlete to competition:", e)
         conn.rollback()
         conn.close()
         return False

def add_private_coaching(athlete_id, hours):
    """Adds private coaching hours for an athlete."""
    conn = create_connection()
    if not conn:
       return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO PrivateCoaching (athlete_id, coaching_hours) VALUES (?, ?)", (athlete_id, hours))
        conn.commit()
        print("Private coaching hours added successfully.")
        conn.close()
        return True
    except pyodbc.Error as e:
        print("Error adding private coaching hours:", e)
        conn.rollback()
        conn.close()
        return False

def get_athlete_report_data(athlete_id):
    """Fetches data for athlete report."""
    conn = create_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                a.name,
                tp.weekly_fee,
                SUM(pc.coaching_hours) AS total_coaching_hours,
                COUNT(ca.competition_id) AS competition_count,
                c.entry_fee,
                a.current_weight,
                a.competition_weight_category
            FROM Athletes a
            LEFT JOIN TrainingPlans tp ON a.training_plan = tp.plan_name
            LEFT JOIN PrivateCoaching pc ON a.id = pc.athlete_id
            LEFT JOIN CompetitionAthletes ca ON a.id = ca.athlete_id
            LEFT JOIN Competitions c ON ca.competition_id = c.id
            WHERE a.id = ?
            GROUP BY a.name;
        """, (athlete_id,))
        report = cursor.fetchone()
        if report:
            cursor.execute("SELECT upper_weight_limit FROM WeightCategories WHERE category_name = ?", (report.competition_weight_category,))
            limit = cursor.fetchone().upper_weight_limit
            report = dict(report)
            report['limit'] = limit
        return report
    except pyodbc.Error as e:
        print("Error fetching athlete report data:", e)
        return None
    finally:
        conn.close()

def check_users_exist():
    """Checks if any users exist in the database."""
    conn = create_connection()
    if not conn:
       return False
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return bool(users)


def check_tables_exist():
    conn = create_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
      cursor.execute("SELECT name FROM sys.tables WHERE name = 'Users'")
      result = cursor.fetchone()
      conn.close()
      return bool(result)
    except pyodbc.Error as e:
        print("Error checking tables:", e)
        conn.close()
        return False
    

