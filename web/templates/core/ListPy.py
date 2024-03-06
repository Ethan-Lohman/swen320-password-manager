from flask import Flask, jsonify
app = Flask(__name__)
from web import db

@app.route('Maketable')
def Maketable():
    password_list = db.get_password_list()
    return jsonify(password_list)

if __name__ == '__main__':
    app.run(debug=True)