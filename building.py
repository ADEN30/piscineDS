import matplotlib.pyplot as plt
import psycopg2 as psypg
from matplotlib.ticker import MultipleLocator
import numpy as np

#SQL

get_order_frequency = f"\
SELECT \
    frequency, \
    COUNT(*) AS customers \
FROM ( \
    SELECT \
        user_id, \
        COUNT(*) AS frequency \
    FROM customers \
    WHERE event_type = 'purchase' \
    GROUP BY user_id \
) AS sub \
GROUP BY frequency \
ORDER BY frequency;"

def main():
    conn = psypg.connect(
        dbname='piscineds',
        user='agallet',
        host='localhost',
        password='mysecretpassword',
        port='5432'
    )
        
    cursor = conn.cursor()

    cursor.execute(get_order_frequency)

    data = cursor.fetchall()


    data1 = [p[1] for p in data]
    data2 = [p[0] for p in data]

    figure, ax = plt.subplots()

    ax.bar(data2, data1, width=0.8, color='skyblue')
    plt.xlim(left=0, right=100)
    plt.xlabel('Nombre d\'achats par client (frequency)')
    plt.ylabel('Nombre de clients (customers)')
    plt.title('Répartition des clients selon leur fréquence d\'achat')
    plt.xticks(rotation=90)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # ax.xaxis.set_major_locator(MultipleLocator(10))


    plt.show()

if (__name__ == '__main__'):
    main()