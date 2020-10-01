from flask import Flask
app = Flask(__name__)




@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/new')
def new():
    return 'Hello, Brave New World!'




if __name__ == "__main__":
    app.run(debug=True)