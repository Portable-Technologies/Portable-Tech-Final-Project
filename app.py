from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT"))

# Config values
image_url_s3 = os.getenv('BACKGROUND_IMAGE_URL')
group_name = os.getenv('GROUP_NAME')
group_slogan = os.getenv('GROUP_SLOGAN')


# AWS credentials from env
# session = boto3.session.Session(
#     region_name=os.getenv('AWS_REGION'),
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
#     aws_session_token=os.getenv('AWS_SESSION_TOKEN')
# )
s3 = boto3.client('s3')

# Extract bucket and key from the S3 URL
bucket = image_url_s3.replace("s3://", "").split('/')[0]
key = "/".join(image_url_s3.replace("s3://", "").split('/')[1:])

os.makedirs('static', exist_ok=True)

# Set local path for the image
local_image_path = os.path.join('static', os.path.basename(key))

# Download image from S3
s3.download_file(bucket, key, local_image_path)
print(f"Downloaded background image from {image_url_s3}")

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=local_image_path, group_name=group_name, group_slogan=group_slogan)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html',  image=local_image_path, group_name=group_name, group_slogan=group_slogan)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, image=local_image_path, group_name=group_name, group_slogan=group_slogan)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=local_image_path, group_name=group_name, group_slogan=group_slogan)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=local_image_path, group_name=group_name, group_slogan=group_slogan)
                           

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    app.run(host='0.0.0.0',port=81,debug=True)
