from flask import Flask, jsonify
from web import db

app = Flask(__name__)

@app.route('/Maketable')
def maketable():
    password_list = db.get_password_list()
    return jsonify(password_list)

if __name__ == '__main__':
    app.run(debug=True)
