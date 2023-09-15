
from flask import Flask, render_template, request
from snowflake import connector
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    cur = cnx.cursor().execute("Select Name, count(*) from ADDRESSES group by NAME;")
    data4charts=pd.DataFrame(cur.fetchall(), columns=['NAME','vote'])
    data4chartsJSON = data4charts.to_json(orient='records')
    return render_template('charts.html', data4chartsJSON=data4chartsJSON)

@app.route('/Submit')
def submitpage():
    return render_template('submit.html')

@app.route('/HardData')
def hardData():
    dfhtml = updateRows().to_html()
    return render_template('index.html', dfhtml=dfhtml)

@app.route('/thanks4submit', methods=["POST"])
def thanks4submit():
    address = request.form.get("cname")
    name = request.form.get("uname")
    insertRow(address, name)
    return render_template('thanks4submit.html',
                           colorname=address,
                           username=name)
    
#snowflake
cnx = connector.connect(
    account= os.environ.get('REGION'),
    user= os.environ.get('USERNAME'),
    password= os.environ.get('PASSWORD'),
    warehouse='COMPUTE_WH',
    database='DEMO_DB',
    schema='PUBLIC',
    role='ACCOUNTADMIN'
)


def insertRow(address, name):
    cur = cnx.cursor()
    updateString = "INSERT INTO ADDRESSES(ADDRESS, NAME) VALUES ('{}', '{}')".format(address, name)
    print(updateString)
    cur.execute(updateString)

def updateRows():
    cur = cnx.cursor()
    cur.execute("SELECT * FROM ADDRESSES")
    rows = pd.DataFrame(cur.fetchall(),columns=['ADDRESS', 'NAME'])
    return rows

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
