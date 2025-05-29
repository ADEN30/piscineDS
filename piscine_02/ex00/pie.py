import matplotlib.pyplot as plt
# import pandas as pd
import psycopg2 as psypg

# Table, Column and data
table = 'customers'
column = 'event_type'
type_of_events = ['view', 'cart', 'remove_from_cart', 'purchase']

# ORDER SQL
select_customer_all = f'SELECT * FROM public.{table};'
select_customer_event_type = f'SELECT %s FROM public.{table} WHERE {column}=%s;'



def main():
    
    data_in_pourcentage = []
    data_number = []
    size_all_table = 0

    conn = psypg.connect(
        dbname='piscineds',
        user='agallet',
        host='localhost',
        password='mysecretpassword',
        port='5432'
    )
        
    cursor = conn.cursor()

    for type_event in type_of_events:
        cursor.execute(select_customer_event_type, (type_event, type_event))
        data = cursor.fetchall()
        data_size = data.__len__()
        size_all_table += size_all_table + data_size
        data_number.append(data_size)
        
    for value in data_number:
        data_in_pourcentage.append(round((value / size_all_table) * 100, 1))

    fig, ax = plt.subplots()
    ax.pie(data_in_pourcentage, labels=type_of_events, autopct='%1.1f%%')
    plt.show()

if __name__ == "__main__":
    main()

