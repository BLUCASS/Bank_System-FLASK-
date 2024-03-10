from flask import Flask, redirect, render_template, url_for, request
from controller import UserManagement, AccountManagement, DbManagement


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/user/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/user/signup/send', methods=['POST'])
def send_signup():
    data = request.form
    UserManagement().create_user(data)
    return redirect(url_for("signup"))

@app.route('/user/delete', methods=['GET'])
def delete_user():
    return render_template('delete_user.html')

@app.route('/user/delete/send', methods=['POST'])
def send_delete():
    data = request.form
    UserManagement().delete_user(data)
    return redirect(url_for("delete_user"))

@app.route('/user/password', methods=['GET'])
def change_password():
    return render_template("change_password.html")

@app.route('/user/password/change', methods=['POST'])
def send_change_password():
    data = request.form
    UserManagement().change_password(data)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)