from flask import Flask

#msg="Hello World"
#print(msg)
#msg.lower()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ("<p>Hello Pexonian, trage hier deine Zertifizierungen ein! <br> Hello Pexonian, Please enter your certifications here! </p>") 
    

#render("./templates/upload.html")