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
        #origin.git.checkout("master")
        repo.remotes.origin.pull('master')
        
 
        
        
        #origin = repo.remotes.origin
        #repo.git.checkout("HEAD~1")
        #repo.remotes.origin.pull()    
        #origin.git.checkout("master")
        #origin.pull()
        #origin = repo.remotes.origin
        #repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        #origin.pull()
        
 
        
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
