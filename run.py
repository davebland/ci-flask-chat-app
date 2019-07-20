import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "arandomstring")
messages = []

def add_message(username, message):
    """ Add messages to stack """
    now = datetime.now().strftime("%H:%M:%S")
    messages.append({
        "timestamp" : now,
        "from" : username,
        "message" : message
    })

@app.route('/', methods=["GET","POST"])
def index():
    """ Main page with user directions """
    if request.method == "POST":
        session["username"] = request.form["username"]
    
    if "username" in session:
        return redirect(url_for("user", username=session["username"]))
        
    return render_template('index.html')
    
@app.route('/chat/<username>', methods=["GET","POST"])
def user(username):
    """ User page with messages """
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        return redirect(url_for("user", username=session["username"]))
    return render_template('chat.html', username = username, chat_messages = messages)
    
@app.route('/chat/<username>/<message>')
def send_message(username, message):
    """ Take new message and add to chat """
    add_message(username, message)
    return redirect(url_for("user", username=session["username"]))
    
app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "5000")), debug=False)