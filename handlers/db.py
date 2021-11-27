import sys
import sqlite3
import traceback
from sqlite3 import Error
import importlib
from strings import text

config = importlib.import_module('configs.'+sys.argv[0].split('.')[0])


def connect():
    '''Connect to SQLite database and return connection and cursor instances'''

    try:
        db = sqlite3.connect(f'databases/{config.SYMBOL}.db')

        # Change row factory of connection to dictionary
        db.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)])

        cursor = db.cursor()

        # ? Create Tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        referred_by INTEGER DEFAULT NULL,
                        balance INTEGER DEFAULT(0),
                        twitter VARCHAR(300),
                        email VARCHAR(300),
                        wallet VARCHAR(300),
                        step VARCHAR(100) DEFAULT('home'),
                        status VARCHAR(100) DEFAULT('registering'),
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS settings
                    (
                        withdraw_status VARCHAR(50) DEFAULT('close'),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );''')

        db.commit()
        return db, cursor

    except Error as error:
        print("SQLite Error:")
        print(error)
        print('SQLite TraceBack:')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def insert(table, columns, values):
    '''Insert a new record in the database'''

    db, cursor = connect()
    result = cursor.execute(
        f'INSERT INTO {table} ({columns}) VALUES ({values})')
    result = cursor.fetchall()

    db.commit()
    db.close()
    return result


def select(columns, table, where=None):
    '''ُSelect records from the database'''

    db, cursor = connect()

    if(where):
        result = cursor.execute(
            f'SELECT {columns} FROM {table} WHERE {where}')
        result = cursor.fetchall()
    else:
        result = cursor.execute(
            f'SELECT {columns} FROM {table}')
        result = cursor.fetchall()

    db.close()
    if(result == []):
        return None
    else:
        return result


def update(table, columns_values, where=None):
    '''Update database records'''

    db, cursor = connect()
    if(where):
        result = cursor.execute(
            f'UPDATE {table} SET {columns_values} WHERE {where}')
        result = cursor.fetchall()
    else:
        result = cursor.execute(
            f'UPDATE {table} SET {columns_values}')
        result = cursor.fetchall()

    db.commit()
    db.close()
    return result


def delete(table, where=None):
    '''Delete database records'''

    # Delete
    db, cursor = connect()
    if(where):
        result = cursor.execute(
            f'DELETE FROM {table} WHERE {where}')
        result = cursor.fetchall()
    else:
        result = cursor.execute(
            f'DELETE FROM {table}')
        result = cursor.fetchall()

    db.commit()
    db.close()
    return result


def sql(sql):
    '''Run SQL Command'''

    db, cursor = connect()
    result = cursor.execute(sql)
    result = cursor.fetchall()

    db.commit()
    db.close()

    return result


def create_setting():
    '''Create new empty setting record.'''
    insert('settings', 'withdraw_status', "'close'")
    r = select('*', 'settings')
    return r[0]


def create_user(chat_id, name, referred_by=None):
    '''Store new user information in the database and return the created record.'''

    r = select('*', 'users', f'id={chat_id}')
    name = name.replace("'", "")
    if(r == None):
        if(referred_by):
            insert('users', 'id,referred_by,name,step',
                   f"{chat_id},{referred_by},'{name}','home'")
        else:
            insert('users', 'id,name,step', f"'{chat_id}','{name}','home'")
        r = select('*', 'users', f'id={chat_id}')
    return r[0]


def set_step(chat_id, step):
    '''Sets the user step'''
    return update('users',
                  f"step='{step}'",
                  f"id='{chat_id}'")


def get_step(chat_id):
    '''Returns the user step'''
    return select('step',
                  'users',
                  f"id={chat_id}")[0]['step']


def get_user_referrals(chat_id):
    rf = select('id,name', 'users', f"referred_by={chat_id} and status='active'")

    # List referrals of this user
    if(rf):
        count = len(rf)
        referrals = ''
        for u in rf:
            referrals = referrals + \
                f"<a href='tg://user?id={u['id']}'>{u['name']}</a>\n"
    else:
        count = 0
        referrals = text.no_referrals

    return referrals, count
