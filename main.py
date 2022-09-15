
import http


try:
    from flask import Flask, Response, request, redirect, url_for, flash, send_file, render_template
    from werkzeug.utils import secure_filename
    import os
    import sqlite3
    from io import BytesIO
except:
    print("Some modules missing!")


UPLOAD_FOLDER = './certs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
DATABASE = 'certs.db'
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    tablerows = ""

    try:
        # Try to connect to db and fetch certs list
        cur.execute("SELECT * FROM certs")
        rows = cur.fetchall()
        for row in rows:
            tablerows += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + \
                "</td><td><a href=/cert/" + \
                str(row[0]) + ">" + row[4] + "</a></td></tr>"

    except:
        # If attempt failed, proceed to create db
        cur.execute('''CREATE TABLE certs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT NOT NULL, 
                            cert BLOB NOT NULL, 
                            filename TEXT NOT NULL, 
                            certname TEXT NOT NULL);''')
        conn.commit()

    cur.close()

    return render_template('index.html', rows=tablerows, errors=request.args.getlist("errors"))


@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name')
    certname = request.form.get('certname')
    file = request.files['file']
    errors = []
    if file is None or file.filename == "":
        errors.append("No file selected")
    if name == "":
        errors.append("Name is not provided.")
    if certname == "":
        errors.append("Certificate name is not provided.")
    
    if len(errors) > 0: 
        return redirect(url_for('index', errors=errors))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        insertBLOB(name, certname, file.filename, file)
        print("** File saved ** :  " + filename)
        if app.config.get("TESTING") == True:
            return Response(None, status=201, mimetype='application/json')
        return redirect(url_for('index', name=filename))


@app.route('/cert/<id>', methods=['GET'])
def downloadCERT(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM certs WHERE id = ' + id)

    row = cur.fetchone()
    return send_file(BytesIO(row[2]), download_name=row[3], as_attachment=True)


def insertBLOB(name, certname, filename, file):
    try:
        sqliteConnection = sqlite3.connect(DATABASE)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO certs
                                  (name, cert, certname, filename) VALUES (?, ?, ?, ?)"""

        cert = file.read()
        # Convert data into tuple format
        data_tuple = (name, cert, certname, filename)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


if __name__ == '__main__':
    # define the localhost ip and the port that is going to be used
    # in some future article, we are going to use an env variable instead a hardcoded port
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
