from flask import Flask, render_template, request
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
            cur = conn.cursor()

            for statement in sql_statements:
                cur.execute(statement)

            conn.commit()
        
        conn.close()


    except sqlite3.OperationalError as error:
        print('Failed to create tables:', error)


@app.before_request
def initialize_database():
    create_table()


@app.route('/display_data', methods=['GET'])
def display_data():
    return render_template('display_data.html', data_display=database_display())


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    return render_template('add_data.html')


@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
    return render_template('delete_data.html', data_display=database_display())


@app.route('/edit_data', methods=['GET', 'POST'])
def edit_data():
    return render_template('edit_data.html', data_display=database_display())


@app.route('/', methods=['GET', 'POST'])
def index_page():
    # Safegaurd for form request
    if request.form != {}:
        form_type = request.form['form_type']
        #Add a user
        if form_type == 'add':
            database_add(request.form['user_name'])
        elif form_type == 'edit':
            database_edit(request.form['user_id'], request.form['user_name'])
        elif form_type == 'delete':
            database_delete(request.form['user_id'])
    return render_template('index.html')


def database_display(table = 'users'):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur2 = conn.cursor()

    # Gets all items from users
    cur.execute('select * from {0}'.format(table))

    table_data = cur.fetchall()

    # Gets only one item from users, used for names 
    cur2.execute('select * from users order by id limit 1')

    row_names = [description[0] for description in cur2.description]

    data_display = []
    for row in table_data:
        tmp = []
        for idx, data in enumerate(row):
            tmp.append('{0}: {1}'.format(row_names[idx], data))
        data_display.append(tmp)
    
    conn.commit()
    
    conn.close()

    return data_display


def database_add(data, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO {0} (name)
                VALUES ('{1}')   
                '''.format(table, data))

    conn.commit()
    
    conn.close()


def database_delete(id, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('DELETE FROM {0} WHERE id = {1} '.format(table, id))

    conn.commit()
    
    conn.close()


def database_edit(id, name, table = 'users'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('UPDATE {0} SET name=\'{1}\' WHERE id = {2}'.format(table, name, id))

    conn.commit()
    
    conn.close()


if __name__ == '__main__':
    app.run()
