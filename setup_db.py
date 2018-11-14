import sqlite3


def main():
    conn = sqlite3.connect('data.sqlite')

    c = conn.cursor()

    # # Create table
    # c.execute('''CREATE TABLE kayak_two_cities
    #              (id INTEGER PRIMARY KEY AUTOINCREMENT, start_a text, end_a text, end_b text, price real, url text, date_a date, date_b date, date_query date)''')


    # Create table
    c.execute('''CREATE TABLE kayak_one_city
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, start text, end text, price real, url text, date_a date, date_b date, date_query date)''')

    # # Insert a row of data
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    #
    # # Save (commit) the changes
    # conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

if __name__ == "__main__":
    main()
