from flask import Flask, request, json, make_response, render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_email_verifier import EmailVerifier
from json import dumps, loads
import os


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' #os.environ['MYSQL_ROOT_PASSWORD']
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)
# Initialize the extension
app.config['EMAIL_VERIFIER_KEY'] = 'at_d2rnczuTQlRMWTq5qElyv5fr4nwYi'
verifier = EmailVerifier(app)


@app.route('/', methods=['GET'])
def login_form() -> str:
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login_submit() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (request.form.get('login_name'), request.form.get('password'))
    login_query = """SELECT count(*) user_count FROM app_users where email = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchone()
    if int(int(result['user_count'])) > 0:
        return render_template('calendar_home.html', title='Home')
    else:
        return render_template('login.html', title='Login')


@app.route('/reset-password', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html', title='Reset Password')


@app.route('/reset-password-submit', methods=['POST'])
def reset_password_submit() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['login_name'], content['password'])
    login_query = """SELECT count(1) FROM app_users where email = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    if int(json_result) > int(0):
        return render_template('index.html', title='Home')
    else:
        return render_template('login.html', title='Login')


@app.route('/signup', methods=['GET'])
def form_sign_up():
    return render_template('signup.html', title='Sign Up')


@app.route('/sign-up-submit', methods=['POST'])
def sign_up_submit() -> str:
    cursor = mysql.get_db().cursor()
    status_id = 1; # 1 for Active during create
    inputData = (request.form.get('first_name'), request.form.get('last_name')
                    , request.form.get('email_id'), request.form.get('password')
                    , request.form.get('phone'), status_id)
    sign_up_query = """INSERT INTO app_users (first_name,last_name,email,password,phone, status_id) VALUES (%s,%s,%s,%s,%s,%s) """
    cursor.execute(sign_up_query, inputData)
    mysql.get_db().commit()
    return render_template('login.html', title='Login')


@app.route('/email/<email>')
def email(email):
    # Retrieve an info for the given email address
    email_address_info = verifier.verify(email)
    if email_address_info is not None:
        data = dumps(loads(email_address_info.json_string), indent=4)
        resp = make_response(data, 200)
        resp.headers['Content-Type'] = 'application/json'
    else:
        resp = make_response('None', 404)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)