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


################# DEALING WITH LOGIN/LOGOUT #################
# CREATING THE CACHE FOR THE LOGGED USER
@login_manager.user_loader
def load_user(user_id):
    user = DbManagement().get_user(int(user_id))
    return user

# EXPIRING THE USER'S SESSION
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("signin"))



################# DEALING WITH THE USER #################
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# SIGNUP PAGE
@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    data = request.json
    name = data["name"]
    password = data["password"]
    email = data["email"]
    user = UserManagement().create_user(name=name, email=email, password=password)
    if not user:
        flash("Email address already exists. Please, go to the login page.")
        return redirect(url_for("signup"))
    login_user(user)
    return redirect(url_for("main_page"))

# SIGNIN/LOGIN PAGE
@app.route('/user/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    
    data = request.json
    email = data["email"]
    password = data["password"]
    user = UserManagement().login(email, password)
    if user:
        login_user(user)
        return redirect(url_for("main_page"))
    flash('User or password do not match')
    return redirect(url_for("main_page"))

# DELETE USER
@app.route('/user/delete', methods=['GET', 'DELETE'])
@login_required
def delete_user():
    if request.method == 'GET':
        return render_template('delete_user.html')
    
    UserManagement().delete_user(current_user.id)
    return redirect(url_for("signin"))

# CHANGE USER'S PASSWORD
@app.route('/user/password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template("change_password.html")
    
    data = request.json
    old_password = data["old_password"]
    new_password = data["new_password"]
    ok = UserManagement().change_password(old_password, new_password, current_user)
    if not ok: 
        flash('Password do not match')
        return render_template("change_password.html")
    flash("Password changed successfully")
    return redirect(url_for("index"))

# CREATING THE MAIN PAGE FOR THE USER
@app.route('/main_page', methods=['GET'])
@login_required
def main_page():
    return render_template("main_page.html")



################# DEALING WITH THE ACCOUNT #################

# CREATING THE OPTION FOR THE USER TO CREATE AN ACCOUNT
@app.route('/create/account', methods=['GET'])
@login_required
def create():
    id = current_user.id
    created = AccountManagement().create_account(id)
    if not created:
        flash('Account not created.')
        return redirect(url_for("main_page"))
    return redirect(url_for('view_balance'))

# GETTING THE USER'S BALANCE THROUGH A JSON FILE
@app.route('/account/balance', methods=['GET'])
@login_required
def view_balance():
    from flask import jsonify
    owner_id = current_user.id
    expenses = AccountManagement().get_balance(owner_id)
    expenses_json = jsonify(expenses)
    return expenses_json

# CREATING THE OPTION FOR THE USER TO WITHDRAW MONEY
@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'GET':
        return render_template('withdraw.html')
    
    data = request.json
    owner_id = current_user.id
    reason = data["reason"]
    value = data["value"]
    
    ok = AccountManagement().withdraw_money(owner_id, reason, value)
    if ok:
        return redirect(url_for('view_balance'))
    flash('You do not have enough money. Please, make a deposit first.')
    return redirect(url_for('view_balance'))

# CREATING THE OPTION FOR THE USER TO DEPOSIT MONEY
@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'GET':
        return render_template('deposit.html')
    
    data = request.json
    owner_id = current_user.id
    reason = data["reason"]
    value = data["value"]
    ok = AccountManagement().deposit_money(owner_id, reason, value)
    if ok:
        return redirect(url_for('view_balance'))
    flash('An error has ocurred. Please, try again.')
    return redirect(url_for('view_balance'))



# RUNNING THE APP
if __name__ == '__main__':
    app.run(debug=True)