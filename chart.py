import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2 as psypg

# Set data
event_type = 'purchase'
tables = ['2022_oct', '2022_nov','2022_dec','2023_jan', '2023_fev']
dead_line = '2023-02-01'

labelx0 = ""
labely0 = "number of customers"
labelx1 = ""
labely1 = "total sale in millions of ₳"
labelx2 = ""
labely2 = "average spend/customers in ₳"

#SQL
select_customer_number_event_type_by_day = f"SELECT DATE(event_time) AS purchase_date, COUNT(*) AS total_purchase FROM customers WHERE event_type='{event_type}' AND event_time < '{dead_line}' GROUP BY DATE(event_time) ORDER BY purchase_date ASC;"
select_count_table_event_type = f"SELECT event_time, COUNT(*) OVER AS total_purchase FROM customers WHERE event_type='{event_type}';"
select_all_sales = f"SELECT  DATE_TRUNC('month', event_time) AS month, SUM(price) AS total_price FROM  customers WHERE event_type = 'purchase' AND event_time < '{dead_line}' GROUP BY  DATE_TRUNC('month', event_time) ORDER BY  month ASC;"
money_spend_by_person_by_day = f"SELECT  DATE(event_time) AS purchase_date, SUM(price) AS total_spent, COUNT(DISTINCT user_id) AS total_user, COUNT(*) AS purchases FROM  customers WHERE  event_type = 'purchase' AND event_time < '2023-02-01' GROUP BY  DATE(event_time) ORDER BY  purchase_date"

def main():
    
    
    conn = psypg.connect(
        dbname='piscineds',
        user='agallet',
        host='localhost',
        password='mysecretpassword',
        port='5432'
    )
    
    cursor = conn.cursor()
    
    fig, axs = plt.subplots(1, 3, figsize=(20, 7))
    
    
    ##### GRAPH 1 #####
    
    cursor.execute(select_customer_number_event_type_by_day)
    result_data = cursor.fetchall() 
    
    #DATA for graph
    data = {'date': [], 'number_purchase': []}
    for value in result_data:
        data['date'].append(value[0])
        data['number_purchase'].append(value[1])
        
    #Set the graph 
    axs[0].plot(data['date'], data['number_purchase'], linewidth='0.8')
    
    axs[0].set_xlim(data['date'][0], data['date'][-1])
    
    axs[0].xaxis.set_major_locator(mdates.MonthLocator())
    
    axs[0].set_ylabel(labely0)
    
    date_format = mdates.DateFormatter('%b')
    axs[0].xaxis.set_major_formatter(date_format)
    
    #Color background of graph
    axs[0].set_facecolor("#D4D4D7")
    
    axs[0].grid(True, color='white')
    axs[0].set_axisbelow(True)
    axs[0].tick_params(axis='both', length=0)

    
    
    ##### GRAPH 2 #####

    cursor.execute(select_all_sales)
    result_data = cursor.fetchall()
    
    data.clear()
    data = {'date': [], 'cash': []}
    for value in result_data:
        data['date'].append(value[0])
        data['cash'].append(value[1] / float(1e6))
     
    axs[1].bar(data['date'], data['cash'], width=20, color="#9cb7d2ff", edgecolor='white', linewidth=1)
    axs[1].xaxis.set_major_locator(mdates.MonthLocator())
    axs[1].set_ylabel(labely1)
    
    date_format = mdates.DateFormatter('%b')
    axs[1].xaxis.set_major_formatter(date_format)
    
    axs[1].yaxis.grid(True, color='white')    # Active la grille horizontale (axe Y)
    axs[1].xaxis.grid(False)   # Désactive la grille verticale (axe X)
    axs[1].set_axisbelow(True)
    axs[1].set_facecolor("#D4D4D7")
    axs[1].tick_params(axis='both', length=0)
    
    

    
    ##### GRAPH 3 #####
    
    cursor.execute(money_spend_by_person_by_day)
    result_data = cursor.fetchall() 
    
    #DATA for graph
    data = {'date': [], 'average spend/customers': []}
    for value in result_data:
        data['date'].append(value[0])
        data['average spend/customers'].append(value[1] / value[2])
        
    #Set the graph
    axs[2].fill_between(data['date'], data['average spend/customers'], 0,  alpha=1, color="#9cb7d2ff")
    
    
    axs[2].set_xlim(data['date'][0], data['date'][-1])
    
    axs[2].set_ylabel(labely2)
    axs[2].xaxis.set_major_locator(mdates.MonthLocator())
    
    date_format = mdates.DateFormatter('%b')
    axs[2].xaxis.set_major_formatter(date_format)
    
    axs[2].set_ylim(bottom=0)
    
    #Color background of graph
    axs[2].set_facecolor("#D4D4D7")
    axs[2].grid(True, color='white')
    axs[2].set_axisbelow(True)
    axs[2].tick_params(axis='both', length=0)
    
    
    
    
    

    plt.show()
    
    
    
    
    
    
    

if __name__ == "__main__":
    main()
    