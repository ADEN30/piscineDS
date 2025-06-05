import matplotlib.pyplot as plt
import psycopg2 as psypg
import numpy as np
# import pandas as pd

#SQL

get_all_purchase = f"SELECT price FROM customers WHERE event_type='purchase'"
get_baskets_avg = f"WITH purchases AS ( \
    SELECT user_id, price, event_time \
    FROM customers \
    WHERE event_type = 'purchase' \
), \
baskets AS ( \
    SELECT user_id, event_time, SUM(price) AS basket_total \
    FROM purchases \
    GROUP BY user_id, event_time \
) \
SELECT user_id, AVG(basket_total) AS average_basket_price \
FROM baskets \
GROUP BY user_id;"
def main():
    conn = psypg.connect(
        dbname='piscineds',
        user='agallet',
        host='localhost',
        password='mysecretpassword',
        port='5432'
    )
        
    cursor = conn.cursor()

    cursor.execute(get_all_purchase)

    purchases = cursor.fetchall()

    purchases = [p[0] for p in purchases]

    number = purchases.__len__()
    std = np.std(purchases)
    mean = np.mean(purchases)
    min = np.min(purchases)
    q1 = np.quantile(purchases, 0.25)
    q2 = np.quantile(purchases, 0.50)
    q3 = np.quantile(purchases, 0.75)
    max = np.max(purchases)


    print(f"Count: {number}\n\
mean: {mean}\n\
std: {std}\n\
min: {min}\n\
25%: {q1}\n\
50%: {q2}\n\
75%: {q3}\n\
max: {max}")
    


    figure, axs = plt.subplots(1, 3, figsize=(20, 8))

    box = axs[0].boxplot(x=[purchases], vert=False, widths=(0.15 * (max - min)), showfliers=True, showcaps=True, showmeans=True, meanline=True, meanprops=dict(color="green", linestyle='-', linewidth=1.5), medianprops=dict(color="#393941", linewidth=4), showbox=False)

    # Épaisseur des caps (traits horizontaux aux extrémités)
    for cap in box['caps']:
        cap.set_linewidth(2)

    axs[0].set_yticks([])
    axs[0].set_yticklabels([])

    axs[0].set_xlabel('price')
    axs[0].xaxis.grid(True, color="white")
    axs[0].yaxis.grid(False)
    axs[0].set_facecolor("#D4D4D7")





    box = axs[1].boxplot(x=[purchases], vert=False, widths=0.5, whis=2, patch_artist=True, showfliers=False, showcaps=True, showmeans=False, meanline=True, meanprops=dict(color="green", linestyle='-', linewidth=1.5), medianprops=dict(color="#393941", linewidth=4), showbox=True)

    # Épaisseur des caps (traits horizontaux aux extrémités)
    for cap in box['caps']:
        cap.set_linewidth(2)
    
    for b in box['boxes']:
        b.set(facecolor='green')

    axs[1].set_yticks([])
    axs[1].set_yticklabels([])


    axs[1].set_xlabel('price')
    axs[1].xaxis.grid(True, color="white")
    axs[1].yaxis.grid(False)
    axs[1].set_facecolor("#D4D4D7")



    cursor.execute(get_baskets_avg)

    purchases_avg = cursor.fetchall()

    purchases_avg = [p[1] for p in purchases_avg]

    number = purchases_avg.__len__()
    std = np.std(purchases_avg)
    mean = np.mean(purchases_avg)
    min = np.min(purchases_avg)
    q1 = np.quantile(purchases_avg, 0.25)
    q2 = np.quantile(purchases_avg, 0.50)
    q3 = np.quantile(purchases_avg, 0.75)
    max = np.max(purchases_avg)

    print(f"Count: {number}\n\
mean: {mean}\n\
std: {std}\n\
min: {min}\n\
25%: {q1}\n\
50%: {q2}\n\
75%: {q3}\n\
max: {max}")
    
    box = axs[2].boxplot(x=[purchases_avg], vert=False, widths=0.5, whis=1, patch_artist=True, notch=False, showfliers=True, showcaps=True, showmeans=False, meanline=True, meanprops=dict(color="green", linestyle='-', linewidth=1.5), medianprops=dict(color="#393941", linewidth=4), showbox=True)

    # Épaisseur des caps (traits horizontaux aux extrémités)
    for cap in box['caps']:
        cap.set_linewidth(2)
    
    for b in box['boxes']:
        b.set(facecolor="#94BFE2")

    axs[2].set_yticks([])
    axs[2].set_yticklabels([])


    # axs[2].set_xlabel('price')
    axs[2].xaxis.grid(True, color="white")
    axs[2].yaxis.grid(False)
    axs[2].set_facecolor("#D4D4D7")

    plt.xlim(left=-20, right=100)

    # plt.show()
    plt.savefig("mustache.png")  # Enregistre sans afficher

if (__name__  == '__main__'):
    main()