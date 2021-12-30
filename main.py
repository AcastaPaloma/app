from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid
import random

app = Flask(__name__)

UPLOADED_FILE_DIR_PATH = os.path.join(os.path.dirname(__file__), "static", "uploaded-images")
UPLOADED_ICON_FILE_DIR_PATH = os.path.join(os.path.dirname(__file__), "static", "discord_server_icons")
DATA_BASE_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database2.sqlite')

def check_to_create_table():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Artpieces ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, artist_name TEXT NOT NULL, image_name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL, image_filename TEXT NOT NULL, artpiece_type TEXT NOT NULL)')

    connection.close()


def check_to_create_table_discord_server_info():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Servers ( id INTEGER PRIMARY KEY, server_name TEXT, server_charact TEXT, link_to_server TEXT, server_icon_filename TEXT, server_description TEXT)')

    connection.close()

def check_to_create_table_account_info():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Accounts ( id INTEGER PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)')

    connection.close()

check_to_create_table()
check_to_create_table_discord_server_info()
check_to_create_table_account_info()

@app.route('/')
def home():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Artpieces WHERE artpiece_type='Painting'")
    records_of_painting = cur.fetchall()
    connection.commit()

    list_of_id = []

    for element in records_of_painting:
        list_of_id.append(element[0])

    wanted_ids = (random.sample(list_of_id, 4))
    tupled_wanted_ids = tuple(wanted_ids)
    questionmarks = '?' * len(tupled_wanted_ids)

    formatted_query = 'SELECT * FROM Artpieces WHERE id IN({})'.format(', '.join(questionmarks))
    query_args = []
    query_args.extend(tupled_wanted_ids)

    cur.execute(formatted_query, query_args)
    returned_paintings = cur.fetchall()

    # -----------------------------------------------------------------------------------------------------------

    cur.execute("SELECT * FROM Artpieces WHERE artpiece_type='Drawing'")
    records_of_drawing = cur.fetchall()
    connection.commit()

    list_of_id2 = []

    for element in records_of_drawing:
        list_of_id2.append(element[0])

    wanted_ids2 = (random.sample(list_of_id2, 4))
    tupled_wanted_ids2 = tuple(wanted_ids2)
    questionmarks2 = '?' * len(tupled_wanted_ids)

    formatted_query2 = 'SELECT * FROM Artpieces WHERE id IN({})'.format(', '.join(questionmarks2))
    query_args2 = []
    query_args2.extend(tupled_wanted_ids2)

    cur.execute(formatted_query2, query_args2)
    returned_drawings = cur.fetchall()

    # -----------------------------------------------------------------------------------------------------------

    cur.execute("SELECT * FROM Artpieces WHERE artpiece_type='Digital art'")
    records_of_digital_art = cur.fetchall()
    connection.commit()

    list_of_id3 = []

    for element in records_of_digital_art:
        list_of_id3.append(element[0])

    wanted_ids3 = (random.sample(list_of_id3, 4))
    tupled_wanted_ids3 = tuple(wanted_ids3)
    questionmarks3 = '?' * len(tupled_wanted_ids3)

    formatted_query3 = 'SELECT * FROM Artpieces WHERE id IN({})'.format(', '.join(questionmarks3))
    query_args3 = []
    query_args3.extend(tupled_wanted_ids3)

    cur.execute(formatted_query3, query_args3)
    returned_digital_art = cur.fetchall()

    # -----------------------------------------------------------------------------------------------------------

    cur.execute("SELECT * FROM Artpieces WHERE artpiece_type='Sculpture'")
    records_of_sculpture = cur.fetchall()
    connection.commit()

    list_of_id4 = []

    for element in records_of_sculpture:
        list_of_id4.append(element[0])

    wanted_ids4 = (random.sample(list_of_id4, 4))
    tupled_wanted_ids4 = tuple(wanted_ids4)
    questionmarks4 = '?' * len(tupled_wanted_ids4)

    formatted_query4 = 'SELECT * FROM Artpieces WHERE id IN({})'.format(', '.join(questionmarks4))
    query_args4 = []
    query_args4.extend(tupled_wanted_ids4)

    cur.execute(formatted_query4, query_args4)
    returned_sculptures = cur.fetchall()

    connection.commit()
    connection.close()

    return render_template('home.html', records_of_painting=records_of_painting
                           , records_of_drawing=records_of_drawing
                           , records_of_digital_art=records_of_digital_art
                           , returned_paintings=returned_paintings
                           , records_of_sculpture=records_of_sculpture
                           , returned_drawings=returned_drawings
                           , returned_digital_art=returned_digital_art
                           , returned_sculptures=returned_sculptures
                           )

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')


@app.route('/search')
def search():
    return render_template('search_for_art.html', records='')


@app.route('/search_results', methods=["POST"])
def search_results():
    requested_search = request.values.get("search_input")

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "SELECT * FROM Artpieces WHERE name Like ? OR artist_name Like ? OR image_name Like ? OR artpiece_type Like ? OR email like ?",
        (requested_search, requested_search, requested_search, requested_search, requested_search))
    records = cur.fetchall()

    connection.commit()
    connection.close()
    return render_template('search_for_art.html',
                           records=records)


@app.route("/details_of_art", methods=["POST", "GET"])
def art_details():
    requested_name = request.values.get('name')
    requested_artist_name = request.values.get('artist_name')
    requested_image_name = request.values.get('image_name')
    requested_email = request.values.get('email')
    requested_message = request.values.get('message')
    requested_image_filename = request.values.get('image_filename')
    requested_artpiece_type = request.values.get('image_filename')

    return render_template('details_of_art.html',
                           requested_name=requested_name,
                           requested_image_name=requested_image_name,
                           requested_artist_name=requested_artist_name,
                           requested_email=requested_email,
                           requested_message=requested_message,
                           requested_image_filename=requested_image_filename,
                           requested_artpiece_type=requested_artpiece_type)


@app.route('/about')
def about():
    return render_template('page2.html')


@app.route("/process", methods=["POST"])
def process():
    username = request.values.get("username")
    artist_name = request.values.get("artist")
    title = request.values.get('title')
    email = request.values.get('email')
    message = request.values.get('message')
    type = request.form["options"]

    image_file = request.files['image']
    my_filename = secure_filename(image_file.filename)

    my_file_path = os.path.join(UPLOADED_FILE_DIR_PATH, my_filename)
    image_file.save(my_file_path)

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Artpieces(name, artist_name, image_name, email, message, image_filename, artpiece_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (username, artist_name, title, email, message, my_filename, type))
    connection.commit()
    connection.close()
    return render_template("uploading_success.html",
                           username=username,
                           image_address="/static/uploaded-images/" + my_filename,
                           email=email,
                           message=message)

@app.route('/action_page')
def action_page():
    username = request.values.get('username')
    email = request.values.get('email')
    password = request.values.get('psw')

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Accounts (username, email, password) VALUES (?, ?, ?)",
        (username, email, password))
    connection.commit()
    connection.close()

    return render_template('successful_account_creation.html')



@app.route('/social')
def servers():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Servers ")
    server_records = cur.fetchall()

    connection.commit()
    connection.close()

    listed_server_records = [list(ele) for ele in server_records]

    return render_template('social.html', server_records=listed_server_records)


@app.route('/server_uploading')
def server_uploading():
    return render_template('secret_server_upload_page_discord_1280.html')


@app.route("/server_uploading_process", methods=["POST"])
def secret_upload():
    requested_server_name = request.values.get("server_name")
    requested_server_charact = request.values.get("server_charact")
    requested_link_to_server = request.values.get("link_to_server")
    requested_server_description = request.values.get("server_description")

    requested_icon_image_file = request.files['server_icon_filename']
    my_icon_filename = secure_filename(requested_icon_image_file.filename)

    my_icon_file_path = os.path.join(UPLOADED_ICON_FILE_DIR_PATH, my_icon_filename)
    requested_icon_image_file.save(my_icon_file_path)

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Servers (server_name, server_charact, link_to_server, server_icon_filename, server_description) VALUES (?, ?, ?, ?, ?)",
        (requested_server_name, requested_server_charact, requested_link_to_server, my_icon_filename,
         requested_server_description))
    connection.commit()
    connection.close()

    return render_template('uploading_icon_success.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5000, debug=True)