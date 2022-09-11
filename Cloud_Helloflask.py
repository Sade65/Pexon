from flask import Flask, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os
import sqlite3
from io import BytesIO

#msg="Hello World"
#print(msg)
#msg.lower()

UPLOAD_FOLDER = './certs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# @app.route("/")
# def hello_world():
#     return ("<p>Hello Pexonian, trage hier deine Zertifizierungen ein! <br> Hello Pexonian, Please enter your certifications here! </p>") 
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            insertBLOB(request.form.get('name'),request.form.get('certname'),file.filename, file)
            print("File saved!")
            return redirect(url_for('upload_file', name=filename))
    else:
        conn = sqlite3.connect('SQLite_Python.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM certs")

        rows = cur.fetchall()
        tablerows = ""
        for row in rows:
            tablerows += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td><td><a href=/cert/" + str(row[0]) + ">" + row[4] + "</a></td></tr>"

    
        return '''
            <!doctype html> 
            <div class="bd-example" align="middle">
            <img src="'''+ url_for('static', filename='images/pexonlogo.png') + '''" align="middle" />
            </div>
            <title>Upload new File</title>
            <h1>Upload new File</h1>

            <p>Hello Pexonian, trage hier deine Zertifizierungen ein! <br> Hello Pexonian, Please enter your certifications here! </p>
            <form method=post enctype=multipart/form-data>
                <input type=text name=name placeholder="Emp. Full name"></br></br>
                <input type=text name=certname placeholder="Emp. Cert name"></br></br>
                <input type=file name=file>
                <input type=submit value=Upload>
                <button type="submit" class="btn btn-primary">Upload certificate</button>
            </form>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Cert</th>
                </tr>'''+ tablerows + '''
            </table>
            '''


#render("./templates/upload.html")

# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData

@app.route('/cert/<id>', methods=['GET'])
def downloadCERT(id):
    conn = sqlite3.connect('SQLite_Python.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM certs WHERE id = ' + id )

    row = cur.fetchone()
    return send_file(BytesIO(row[2]), download_name=row[3], as_attachment=True)


def insertBLOB(name,certname, filename, file):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
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