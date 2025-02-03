import sqlite3
import hashlib

DATABASE_FILE = 'north_sussex_judo.db'

def create_connection():
    """Creates a database connection and returns it."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

def execute_sql_file(conn, sql_file):
    """Executes SQL commands from a given file."""
    with open(sql_file, 'r') as f:
        sql = f.read()
    conn.executescript(sql)

def hash_password(password):
    """Hashes a password using SHA-256 for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Creates a new user with username and hashed password."""
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User created successfully.")
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating user:", e)
        conn.close()
        return False

def login(username, password):
    """Authenticates a user by checking username and password."""
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def fetch_weight_categories():
    """Fetches all weight categories."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_name FROM WeightCategories")
    categories = [row['category_name'] for row in cursor.fetchall()]
    conn.close()
    return categories

def fetch_training_plans():
    """Fetches all training plans."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plan_name FROM TrainingPlans")
    training_plans = [row['plan_name'] for row in cursor.fetchall()]
    conn.close()
    return training_plans

def add_athlete(name, training_plan, current_weight, competition_weight_category):
     """Adds a new athlete to the database."""
     conn = create_connection()
     cursor = conn.cursor()
     try:
         cursor.execute("INSERT INTO Athletes (name, training_plan, current_weight, competition_weight_category) VALUES (?, ?, ?, ?)", (name, training_plan, current_weight, competition_weight_category))
         conn.commit()
         print("Athlete added successfully.")
         conn.close()
         return True
     except sqlite3.Error as e:
         print("Error adding athlete:", e)
         conn.close()
         return False

def add_training_plan(plan_name, weekly_fee):
     """Adds a new training plan to the database."""
     conn = create_connection()
     cursor = conn.cursor()
     try:
         cursor.execute("INSERT INTO TrainingPlans (plan_name, weekly_fee) VALUES (?, ?)", (plan_name, weekly_fee))
         conn.commit()
         print("Training plan added successfully.")
         conn.close()
         return True
     except sqlite3.Error as e:
         print("Error adding training plan:", e)
         conn.close()
         return False

def add_competition(competition_name, entry_fee, date):
    """Adds a new competition to the database."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Competitions (competition_name, entry_fee, date) VALUES (?, ?, ?)", (competition_name, entry_fee, date))
        conn.commit()
        print("Competition added successfully.")
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error adding competition:", e)
        conn.close()
        return False

def fetch_athletes():
    """Fetches all athletes."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Athletes")
    athletes = cursor.fetchall()
    conn.close()
    return athletes

def fetch_competitions():
    """Fetches all competitions."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, competition_name FROM Competitions")
    competitions = cursor.fetchall()
    conn.close()
    return competitions


def add_athlete_to_competition(athlete_id, competition_id):
    """Adds an athlete to a competition."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO CompetitionAthletes (competition_id, athlete_id) VALUES (?, ?)", (competition_id, athlete_id))
        conn.commit()
        print("Athlete added to competition successfully.")
        conn.close()
        return True
    except sqlite3.Error as e:
         print("Error adding athlete to competition:", e)
         conn.close()
         return False

def add_private_coaching(athlete_id, hours):
    """Adds private coaching hours for an athlete."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO PrivateCoaching (athlete_id, coaching_hours) VALUES (?, ?)", (athlete_id, hours))
        conn.commit()
        print("Private coaching hours added successfully.")
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error adding private coaching hours:", e)
        conn.close()
        return False

def get_athlete_report_data(athlete_id):
    """Fetches data for athlete report."""
    conn = create_connection()
    cursor = conn.cursor()
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
    """,(athlete_id,))
    report = cursor.fetchone()
    if report:
       cursor.execute("SELECT upper_weight_limit FROM WeightCategories WHERE category_name = ?",(report['competition_weight_category'],))
       limit = cursor.fetchone()['upper_weight_limit']
       report = dict(report)
       report['limit'] = limit
    conn.close()
    return report

def check_users_exist():
    """Checks if any users exist in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return bool(users)


def check_tables_exist():
    conn = create_connection()
    cursor = conn.cursor()
    try:
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users';")
      result = cursor.fetchone()
      conn.close()
      return bool(result)
    except sqlite3.Error as e:
        print("Error checking tables:", e)
        conn.close()
        return False
    

def update_athlete(athlete_id, name, training_plan, current_weight, competition_weight_category):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE athletes 
            SET name = ?, training_plan = ?, current_weight = ?, competition_weight_category = ?
            WHERE id = ?
        """, (name, training_plan, current_weight, competition_weight_category, athlete_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating athlete: {e}")
        return False
    finally:
        conn.close()

def delete_athlete(athlete_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM athletes WHERE id = ?", (athlete_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting athlete: {e}")
        return False
    finally:
        conn.close()

def delete_training_plan(plan_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TrainingPlans WHERE plan_name = ?", (plan_name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting training plan: {e}")
        return False
    finally:
        conn.close()

def delete_competition(competition_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM competitions WHERE id = ?", (competition_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting competition: {e}")
        return False
    finally:
        conn.close()

def delete_report(athlete_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reports WHERE athlete_id = ?", (athlete_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting report: {e}")
        return False
    finally:
        conn.close()