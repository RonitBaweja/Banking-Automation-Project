import sqlite3 #to interact with SQLite databases using python.

con_obj = sqlite3.connect(database='bank.sqlite') #creates a connection object to
#a database named bank.sqlite, if doesn't exist a new one is created.

cur_obj = con_obj.cursor() #creates a cursor object to run SQLite queries.

try:
    #Create a table named users to store all the user info including ACN,password,
    #name,mob,email,current balance,adhar number,account open date respectively.
    cur_obj.execute('''create table users(
                    users_acno integer primary key autoincrement,
                    users_pass text NOT NULL,
                    users_name text NOT NULL,
                    users_mob text NOT NULL UNIQUE,
                    users_email text NOT NULL UNIQUE,
                    users_bal float NOT NULL,
                    users_adhar text NOT NULL UNIQUE,
                    users_opendate text NOT NULL)'''
                    )


    #Creates a txn table to keep a track on transaction details.
    cur_obj.execute('''create table txn(
                    txn_id integer primary key autoincrement,
                    txn_acno integer NOT NULL,
                    txn_type text NOT NULL,
                    txn_date text NOT NULL,
                    txn_amt float NOT NULL,
                    txn_updatebal float NOT NULL)''')
    print('Tables Successfully created')

except:     #except block is used to handle any potential errors like 'table already exists'.
    print('Tables already exist')

con_obj.close()