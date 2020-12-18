
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_email_verifier import EmailVerifier
from json import dumps, loads

from flask import *
from flask_mail import *
from random import *

from datetime import *
from itsdangerous import URLSafeTimedSerializer


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

mail_settings = {
    "MAIL_SERVER" : 'smtp.gmail.com',
    "MAIL_PORT" : 465,
    "MAIL_USERNAME" : 'nt27gradprojects@gmail.com',
    "MAIL_PASSWORD" : 'Project@2020',
    "MAIL_USE_TLS" : False,
    "MAIL_USE_SSL" : True
}
app.config.update(mail_settings)
mail = Mail(app)

otp = randint(000000,999999)

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'


@app.route('/', methods=['GET'])
def login_form() -> str:
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login_submit() -> str:
    cursor = mysql.get_db().cursor()
    email = request.form.get('login_name')
    password = request.form.get('password')
    input_data = (email, password)
    login_query = """SELECT count(*) user_count FROM app_users where email = %s and password = %s and confirmed = 1 """
    cursor.execute(login_query, input_data)
    result = cursor.fetchone()
    if int(int(result['user_count'])) > 0:
        return render_template('events_list.html', title='Home')
    else:
        return render_template('login.html', title='Login')


@app.route('/signup', methods=['GET'])
def form_sign_up():
    return render_template('signup.html', title='Sign Up')


@app.route('/signup', methods=['POST'])
def sign_up_submit() -> str:
    cursor = mysql.get_db().cursor()
    email = request.form.get('email_id')
    input_data = (request.form.get('first_name'), request.form.get('last_name')
                    , email, request.form.get('password')
                    , request.form.get('phone'))
    sign_up_query = """INSERT INTO app_users (first_name,last_name,email,password,phone,status_id,confirmed,created_on) 
                            VALUES ( %s, %s, %s, %s, %s, 1, 0, CURRENT_TIMESTAMP) """
    cursor.execute(sign_up_query, input_data)
    mysql.get_db().commit()
    # added to verify email address
    return verify(email)
    #return redirect(url_for('/'))
    #generate_confirmation_token(request.form.get('email_id'))
    #flash('Sign Up Successful!. Confirmation email sent. Please follow the instructions in that email', 'success')
    #return "<h3>Sign Up Successful!. Confirmation email sent. Please follow the instructions in that email</h3>"
    #return render_template('login.html', title='Login')


#@app.route('/confirm-email',methods = ["POST"])
def verify(email):
    # email = request.form["email"]
    #msg = Message('OTP',sender = app.config['MAIL_USERNAME'], recipients = [email])
    msg = Message(subject="Hello",
                  sender=app.config.get("MAIL_USERNAME"),
                  recipients=[email],  # replace with your email for testing
                  body=str(otp)
                  )
    mail.send(msg)
    return render_template('verify.html')


@app.route('/verify-email',methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        #flash('Email verified successfully', 'success')
        """sign_up_query = 'UPDATE app_users set confirmed=1 and confirmed_on=CURRENT_TIMESTAMP'
        cursor = mysql.get_db().cursor()
        cursor.execute(sign_up_query)
        mysql.get_db().commit()"""
        return render_template("login.html")
    else:
        return "<h3>Failure, OTP does not match</h3>"




@app.route('/validate-email/<email>')
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


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    cursor = mysql.get_db().cursor()

    user_query = """SELECT count(1) FROM app_users where email = %s """
    cursor.execute(user_query, email)
    user = cursor.fetchall()
    confirmed = user['confirmed']
    if confirmed == 1:
        flash('Account already confirmed. Please login.', 'success')
    else:
        confirmed = 1 # 1 for true
        confirmed_on = datetime.now()
        user_update_query = """UPDATE user set confirmed=%s and confirmed_on=%s where login_name=%s"""
        input = (confirmed, confirmed_on, email)
        cursor.execute(user_update_query, input)
        mysql.get_db().session.commit()
        flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('/'))


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

@app.route('/reset-password', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html', title='Reset Password')


@app.route('/reset-password', methods=['POST'])
def reset_password_submit() -> str:
    cursor = mysql.get_db().cursor()
    #content = request.json
    inputData = (request.form.get('login_name'), request.form.get('password'))
    login_query = """SELECT count(1) FROM app_users where email = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    if int(json_result) > int(0):

        return render_template('index.html', title='Home')
    else:
        return render_template('login.html', title='Login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)