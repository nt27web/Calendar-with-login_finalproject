from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
# from create_event import create_event
# from delete_event import delete_event
# from update_event import update_event

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Calendar Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, event_name=result)


@app.route('/view/<int:event_id>', methods=['GET'])
def record_view(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', event=result[0])


@app.route('/edit/<int:event_id>', methods=['GET'])
def form_edit_get(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', event=result[0])


@app.route('/edit/<int:event_id>', methods=['POST'])
def form_update_post(event_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('title'), request.form.get('start_event'), request.form.get('end_event'), event_id)
    sql_update_query = """UPDATE events t SET t.title = %s, t.start_event = %s, t.end_event = %s
     WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/event_name/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Event Form')



@app.route('/event_name/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('title'), request.form.get('start_event'), request.form.get('end_event'))
    sql_insert_query = """INSERT INTO events (title,start_event,end_event) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    print(sql_insert_query)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:event_id>', methods=['POST'])
def form_delete_post(event_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM events WHERE id = %s """
    cursor.execute(sql_delete_query, event_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/event_name', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['GET'])
def api_retrieve(event_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['PUT'])
def api_edit(event_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['title'], content['start_event'], content['end_event'],
                 event_id)
    sql_update_query = """UPDATE events t SET t.title = %s, t.start_event = %s, t.end_event = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['title'], content['start_event'], content['end_event'])
    sql_insert_query = """INSERT INTO events (title,start_event,end_event) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['DELETE'])
def api_delete(event_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM events WHERE id = %s """
    cursor.execute(sql_delete_query, event_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
