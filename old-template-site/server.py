from flask import Flask
from flask import request

app = Flask(__name__,static_url_path='/static')

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/template', methods=['GET'])
def getTemplate():
    return app.send_static_file('dashboard.templ')

@app.route('/dashboard', methods=['GET'])
def getDashboard():
    return app.send_static_file('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
