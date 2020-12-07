from flask import Flask, request, json
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)


@app.route('/', methods=['POST'])
def login_form() -> str:
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login_submit() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['login_name'], content['password'])
    login_query = """SELECT count(1) FROM app_users where login_name = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    if int(json_result) > 0:
        return render_template('index.html', title='Home')
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
    login_query = """SELECT count(1) FROM app_users where login_name = %s and password = %s """
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
    content = request.json
    inputData = (content['login_name'], content['password'])
    login_query = """SELECT count(1) FROM app_users where login_name = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    if int(json_result) > int(0):
        return render_template('index.html', title='Home')
    else:
        return render_template('login.html', title='Login')




"""

@app.route('/calendar', methods=['GET'])
def index():
    user = {'username': 'Cities Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)
    
@app.route('/edit/<int:Id>', methods=['POST'])
def form_update_post(Id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('LatD'), request.form.get('LatM'), request.form.get('LatS'), request.form.get('NS')
                 , request.form.get('LonD'), request.form.get('LonM'), request.form.get('LonS'), request.form.get('EW')
                 , request.form.get('City'), request.form.get('State'), Id)
    sql_update_query = 'UPDATE tblCities t 
                            SET t.LatD = %s, t.LatM = %s, t.LatS = %s, t.NS = %s
                            , t.LonD = %s, t.LonM = %s, t.LonS = %s, t.EW = %s
                            , t.City = %s, t.State = %s
                            WHERE t.Id = %s'
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('LatD'), request.form.get('LatM'), request.form.get('LatS'), request.form.get('NS')
                 , request.form.get('LonD'), request.form.get('LonM'), request.form.get('LonS'), request.form.get('EW')
                 , request.form.get('City'), request.form.get('State'))
    sql_insert_query = 'INSERT INTO tblCities (LatD,LatM,LatS,NS,LonD,LonM,LonS,EW,City,State) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)