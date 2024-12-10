from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'


def create_table():
    # All SQL Queries for createing all tables
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
            cur = conn.cursor()

            # Runs all create statements
            for statement in sql_statements:
                cur.execute(statement)
            
            # Commits the data to sql
            conn.commit()   
        
        # Closes the connection to the database 
        conn.close()

    # Error handeling incase table was not created
    except sqlite3.OperationalError as error:
        # WARNING Does not give docker or the user this infomration
        print('Failed to create tables:', error)


# Set up database tables
@app.before_request
def initialize_database():
    create_table()


# Handles incoming requests from display_data
@app.route('/display_data', methods=['GET'])
def display_data():
    return render_template('display_data.html', data_display=database_display())


# Handles incoming requests from add_data
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    return render_template('add_data.html')


# Handles incoming requests from delete_data
@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
    return render_template('delete_data.html', data_display=database_display())


# Handles incoming requests from edit_data
@app.route('/edit_data', methods=['GET', 'POST'])
def edit_data():
    return render_template('edit_data.html', data_display=database_display())


# Handles incoming requests from Index
@app.route('/', methods=['GET', 'POST'])
def index_page():
    # Safegaurd for form request
    if request.form != {}:
        form_type = request.form['form_type']
        # Add a user
        if form_type == 'add':
            database_add(request.form['user_name'])
        # Edit a user
        elif form_type == 'edit':
            database_edit(request.form['user_id'], request.form['user_name'])
        # Delete a user
        elif form_type == 'delete':
            database_delete(request.form['user_id'])
    return render_template('index.html')


# Returns a list of all the data in a table dynamically
# Table titles are included
def database_display(table = 'users'):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur2 = conn.cursor()

    # Gets all items from table
    cur.execute('select * from {0}'.format(table))

    table_data = cur.fetchall()

    # Gets only one rows from tables, used to get tabele titles 
    cur2.execute('select * from {0} order by id limit 1'.format(table))

    row_names = [description[0] for description in cur2.description]

    # Puts the table titles and data in one list
    data_display = []
    for row in table_data:
        tmp = []
        for idx, data in enumerate(row):
            tmp.append('{0}: {1}'.format(row_names[idx], data))
        data_display.append(tmp)
    
    conn.commit()
    
    conn.close()

    return data_display

# Add desired data to first colum, only works for table users
def database_add(data, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO {0} (name)
                VALUES ('{1}')   
                '''.format(table, data))

    conn.commit()
    
    conn.close()


# Delete specified row based in table id, works dynamically
def database_delete(id, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('DELETE FROM {0} WHERE id = {1} '.format(table, id))

    conn.commit()
    
    conn.close()

# Edit specifited item in a table, only works for users
def database_edit(id, name, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('UPDATE {0} SET name=\'{1}\' WHERE id = {2}'.format(table, name, id))

    conn.commit()
    
    conn.close()


if __name__ == '__main__':
    app.run()
