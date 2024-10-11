from flask import Flask
import redis
import os
import mysql.connector

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)

def get_db_connection():
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE')
    )
    print("Database connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route("/")
def home():
    count = r.incr("hits")

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed."

    cursor = conn.cursor()
    try:
        print(f"Inserting count: {count}")
        cursor.execute("INSERT INTO visits (count) VALUES (%s)", (count,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Insertion error: {err}")
        return "Error inserting count."
    finally:
        cursor.close()
        conn.close()

    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")











# from flask import Flask
# import redis

# app = Flask(__name__)

# r = redis.Redis(host="redis", port=6379)


# @app.route("/")
# def home():
#     count = r.incr("hits")
#     return f"This page has been visited {count} times."


# if __name__ == "__main__":
#     app.run(host="0.0.0.0")
