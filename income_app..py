from flask import Flask, render_template, request, jsonify, session
import mysql.connector as c
import smtplib
import pandas as pd
# solve the problem of uix degsion of graph in  python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# creating app
app = Flask(__name__)
app.secret_key = '2130'

# Open the create page to user
@app.route('/')
def index_page():
    return render_template('create_account.html')

# Creating the login page
@app.route('/login')
def user_login():
    return render_template('index.html')

# creating the database and table for user 
@app.route('/create_database',methods=['POST'])
def create_database():
   
    try:
        # sending email to user for database and table
        user_id = request.form.get('user-id')
        email_id = request.form.get('user-gmail')

        con = c.connect(host='localhost',user='root',password='2130')
        cursour = con.cursor()
        q1 = 'create database {}'.format(user_id)
        q2 = 'use {}'.format(user_id)
        q3 = 'CREATE TABLE income_track (id INT PRIMARY KEY AUTO_INCREMENT,date_of_expenses DATETIME,area_of_expenses VARCHAR(100),amount_expenses_₹ varchar(10))'
        cursour.execute(q1)
        cursour.execute(q2)
        cursour.execute(q3)
        con.commit()
        con.close()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('sp.info.creation@gmail.com','ojfy tjcz sdzm evzn')
        server.sendmail('sp.info.creation@gmail.com','{}'.format(email_id),'Dear user \n we welcome you yo SP Creation Income track system. This system is designed to help you efficient and track your income data with ease.\n Database Details : \n Database name : {} \n Table name: income_track and check the structure in website \n if you have any question or need assistance,feel free to contact us at sp.info.contact@gmail.com \n Best regards \n SP Creation'.format(user_id))
       
        return render_template('index.html')
    except:
        return "{} with this name database exist and enter valid email id {}".format(user_id,email_id)
    
# crating login to user there database
@app.route('/user_data',methods=['POST'])
def user_info():
    try:
        user_id = request.form.get('user-id')
        con = c.connect(host='localhost',user='root',password='2130',database='{}'.format(user_id))
        return render_template('user_data.html')   
        
    except:
        return 'your user id-: {} not register with us '.format(user_id)


# to show the user data
@app.route('/show_data',methods=['POST'])
def show_data():
    data_base_name = request.form.get('database-name')
    table_name = request.form.get('show-table-name')
    con = c.connect(host='localhost',user='root',password='2130',database='{}'.format(data_base_name))
    cursour = con.cursor()
    q1 = 'select * from {}'.format(table_name)
    cursour.execute(q1)
    table_data =cursour.fetchall()
    column_names = [desc[0] for desc in cursour.description]
    # Render the data in an HTML template
    return render_template('show_data.html', table_name=table_name, column_names=column_names, table_data=table_data)

    
# insert data to table
@app.route('/insert_data', methods=['POST'])
def insert_data():
    data_base_name = request.form.get('database-name')
    table_data = request.form.get('insert-table-name')
    product = request.form.get('area_of_expenses')
    amount = request.form.get('amount_expenses')

    # Establish database connection
    con = c.connect(host='localhost', user='root', password='2130', database=data_base_name)
    cursour = con.cursor()

    # Parameterized SQL query to prevent SQL injection
    q1 = f"""
    INSERT INTO {table_data} (date_of_expenses, area_of_expenses, amount_expenses_₹)
    VALUES (current_timestamp(), %s, %s)
    """

    try:
        # Execute query with parameters
        cursour.execute(q1, (product, amount))
        con.commit()
        return "Data is successfully submitted!"
    except Exception as e:
        # Handle any SQL errors
        con.rollback()
        return f"An error occurred: {str(e)}"
    finally:
        # Always close the connection
        cursour.close()
        con.close()


# creating the analyes tab 
@app.route('/analyses', methods=['POST'])
def analyses_data():
    try:
        database_name = request.form.get('database-name')
        table_name = request.form.get('analyze-table-name')
        con = c.connect(host='localhost',user='root',password='2130',database='{}'.format(database_name))
        cursour = con.cursor()
        q1 = 'select area_of_expenses,amount_expenses_₹ from {};'.format(table_name)
        cursour.execute(q1)
        data = cursour.fetchall()
        new_frame = pd.DataFrame(data)
        x_data = new_frame[0]
        y_data = new_frame[1]
        # creating bar graph
        plt.bar(x=x_data,height=y_data,color=['red','green','blue'])
        plt.title('amount paid to each item')
        plt.xlabel('area_of_expenses')
        plt.ylabel('amount_expenses_₹')
        plt.savefig('D:\\new_project\\static\\images\\bar.jpg')
        plt.close()

        q2 = f'''
            SELECT CONCAT(DAY(date_of_expenses), ' ', 'date') as date, 
                SUM(amount_expenses_₹) 
            FROM {table_name}
            GROUP BY date;
        '''    
        cursour.execute(q2)
        data2 = cursour.fetchall()
        new_data2 = pd.DataFrame(data2)
        lable = new_data2[0]
        pei_data = new_data2[1]
        plt.pie(x=pei_data,labels=lable)
        plt.title('amount paid for each day')
        plt.legend(lable)
        plt.savefig("D:\\new_project\\static\\images\\pie.jpg")
        plt.close()

        q3 = f'''
            SELECT CONCAT(DAY(date_of_expenses), ' ', 'date') as date, 
                count(*)
            FROM {table_name}
            GROUP BY date;
        '''
        cursour.execute(q3)
        data3 = cursour.fetchall()
        data3_frame = pd.DataFrame(data=data3)
        x = data3_frame[0]
        y= data3_frame[1]
        plt.bar(x=x,height=y)
        plt.title('count of transactions per day')
        plt.xlabel('day of month')
        plt.ylabel('count of transactions per day')
        plt.savefig('D:\\new_project\\static\\images\\bar2.jpg')
        plt.close()


        q3 = f'''
            select area_of_expenses,amount_expenses_₹ from {table_name} order by amount_expenses_₹ desc;
        '''
        cursour.execute(q3)
        data4 = cursour.fetchall()
        new_data4 = pd.DataFrame(data4)
        x_data4 = new_data4[0]
        y_data4 = new_data4[1]
        plt.bar(x=x_data4,height=y_data4)
        plt.xlabel('area_of_expenes')
        plt.ylabel('amount')
        plt.savefig('D:\\new_project\\static\\images\\bar3.jpg')
        plt.close()

        q4=f'''
        select ( amount_expenses_₹ / (select sum(amount_expenses_₹) from income_track)) * 100 ,area_of_expenses
        from {table_name};
        '''
        cursour.execute(q4)
        data5=cursour.fetchall()
        new_data5 = pd.DataFrame(data5)
        x5_data = new_data5[0]
        lable5 = new_data5[1]
        plt.pie(x=x5_data,labels=lable5)
        plt.title('total amount persent paid to each item')
        plt.legend(lable5)
        plt.savefig('D:\\new_project\\static\\images\\pie2.jpg')

        con.close()
        return render_template('analyses.html')
    except:
        return "enter the valid data or problem at server end"


# deleting graphs
@app.route('/close')
def close_graph():
    graph_name = ['bar.jpg','pie.jpg','bar2.jpg','bar3.jpg','pie2.jpg']    
    for i in range(len(graph_name)):
        os.remove(f'''D:\\new_project\\static\\images\\{graph_name[i]}''')
    
    return render_template('user_data.html')

#show the table stucture to user
@app.route('/show_table',methods=['POST'])
def show_structure():
    data_base_name = request.form.get('database-name')
    table_name = request.form.get('table-name-show')
    con = c.connect(host='localhost',user='root',password='2130',database='{}'.format(data_base_name))
    cursour = con.cursor()
    q1 = 'desc {}'.format(table_name)
    cursour.execute(q1)
    data =cursour.fetchall()
    column_names = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
    con.close()
    return render_template(
        'table_structure.html', 
        table_name=table_name,
        column_names=column_names,
        table_data=data
    )

#creating the logout from income track
@app.route('/logout')
def logout():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
