from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def create_table():
    sql_statements = [
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name NOT NULL
        )
        '''
    ]

    try: 
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            for statement in sql_statements:
                cursor.execute(statement)

            conn.commit()
        
        conn.close()


    except sqlite3.OperationalError as error:
        print('Failed to create tables:', error)


@app.before_request
def initialize_database():
    create_table()


@app.route('/')
def index_page(name=None):
    return render_template('index.html', users=name)


if __name__ == '__main__':
    app.run()