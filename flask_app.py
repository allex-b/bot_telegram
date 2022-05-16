from flask import Flask
from flask import request

#git update from webhooks
import git

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Flask APP, Telebot"


#git update
@app.route('/update_server', methods=['POST'])
def webhook_git():
    if request.method == 'POST':
        repo = git.Repo('./mysite')
        origin = repo.remotes.origin
        #repo.git.checkout("HEAD~1")
        #repo.remotes.origin.pull()
        #repo.git.checkout("master")


        origin.pull()


        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
