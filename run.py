import os
from flask import Flask, redirect

app = Flask(__name__)
messages = []

def add_messages(username, message):
    """ Add messages to stack """
    messages.append("{}: {}".format(username, message))
    
def format_messages_for_display():
    """ Format the messages for nice display """
    return "<br>".join(messages)

@app.route('/')
def index():
    """ Main page with user directions """
    return "<p>To send a message use /<i>username</i>/<i>message</i></p>"
    
@app.route('/<username>')
def user(username):
    """ User page with messages """
    return "<h1>Hi {}, your messages:</h1>{}".format(username, format_messages_for_display())
    
@app.route('/<username>/<message>')
def send_message(username, message):
    """ Take new message and add to chat """
    add_messages(username, message)
    return redirect("/" + username)
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)