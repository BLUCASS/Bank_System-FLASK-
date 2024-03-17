from flask import Flask, redirect, render_template, url_for, request, flash
from controller import UserManagement, AccountManagement, DbManagement
from keys import secret_key
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# LOGIN STUFF
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin' # This is the page it will redirect all the unauthorized users

# CREATING THE METHOD TO LOG THE USER IN
@login_manager.user_loader
def load_user(user_id):
    user = DbManagement().get_user(int(user_id))
    return user

# THIS IS THE HOME PAGE
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# SIGNUP PAGE
@app.route('/user/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# SIGNUP PAGE POST
@app.route('/user/signup/send', methods=['POST'])
def send_signup():
    data = request.form
    if not UserManagement().create_user(data): flash("Email address already exists.")
    return redirect(url_for("signup"))

# DELETE USER
@app.route('/user/delete', methods=['GET'])
def delete_user():
    return render_template('delete_user.html')

# DELETE USER POST
@app.route('/user/delete/send', methods=['POST'])
def send_delete():
    data = request.form
    UserManagement().delete_user(data)
    return redirect(url_for("delete_user"))

# CHANGE USER'S PASSWORD
@app.route('/user/password', methods=['GET'])
def change_password():
    return render_template("change_password.html")

# CHANGE USER'S PASSWORD POST
@app.route('/user/password/change', methods=['POST'])
def send_change_password():
    data = request.form
    UserManagement().change_password(data)
    return redirect(url_for("index"))

# SIGIN/LOGIN PAGE
@app.route('/user/signin', methods=['GET'])
def signin():
    return render_template("signin.html")

# SIGIN/LOGIN PAGE POST
@app.route('/user/signin/send', methods=['POST'])
def send_signin():
    email = request.form.get("email")
    pwd = request.form.get("password")
    user = UserManagement().login(email, pwd)
    if user:
        login_user(user)
        return redirect(url_for("main_page"))
    flash('User or password do not match')
    return redirect(url_for("signin"))

# EXPIRING THE USER'S SESSION
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("signin"))

# CREATING THE MAIN PAGE FOR THE USER
@app.route('/main_page', methods=['GET'])
@login_required
def main_page():
    return render_template("main_page.html")

@app.route('/create/account/send', methods=['GET'])
@login_required
def send_create():
    id = current_user.id
    return redirect(url_for("main_page"))

@app.route('/account/balance', methods=['GET'])
@login_required
def view_balance():
    owner_id = current_user.id
    expenses = AccountManagement().get_balance(owner_id)
    if expenses: return render_template('account.html', expenses=expenses)
    return redirect(url_for('main_page'))

@app.route('/withdraw', methods=['GET'])
@login_required
def withdraw():
    return render_template('withdraw.html')

@app.route('/withdraw/send', methods=['POST'])
@login_required
def send_withdraw():
    owner_id = current_user.id
    reason = request.form.get("reason")
    value = request.form.get("value")

    if AccountManagement().withdraw_money(owner_id, reason, value):
        return redirect(url_for('view_balance'))
    flash('You do not have enough money. Please, make a deposit first.')
    return redirect(url_for('view_balance'))

@app.route('/deposit', methods=['GET'])
@login_required
def deposit():
    return render_template('deposit.html')

@app.route('/deposit/send', methods=['POST'])
@login_required
def send_deposit():
    owner_id = current_user.id
    reason = request.form.get("reason")
    value = request.form.get("value")

    if AccountManagement().deposit_money(owner_id, reason, value):
        return redirect(url_for('view_balance'))
    flash('An error has ocurred. Please, try again.')
    return redirect(url_for('view_balance'))


# RUNNING THE APP
if __name__ == '__main__':
    app.run(debug=True)