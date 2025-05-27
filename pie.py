import matplotlib as mtlp 
import pandas as pd
import psycopg2 as psypg


def main():
    conn = psypg.connect(
        dbname='piscineds',
        user='agallet',
        host='localhost',
        password='mysecretpassword',
        port='5432'
    )
        
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items;')

    print(type(cursor.fetchmany(20)))


if __name__ == "__main__":
    main()

