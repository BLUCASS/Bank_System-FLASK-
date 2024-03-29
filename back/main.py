from flask import Flask, redirect, render_template, url_for, request, flash, make_response, jsonify
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
    return make_response(jsonify({'message': 'Redirect to the signin/login page'}), 200)



################# DEALING WITH THE USER #################
@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify({'message': 'Success'}), 200)

# SIGNUP PAGE
@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    data = request.json
    name = data["name"]
    password = data["password"]
    email = data["email"]
    user = UserManagement().create_user(name=name, email=email, password=password)
    if not user:
        return make_response(jsonify({'message':'Email address already exists. Please, go to the login page.'}), 500)
    login_user(user)
    return make_response(jsonify({'message': 'Redirect to the main_page'}), 200)

# SIGNIN/LOGIN PAGE
@app.route('/user/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    data = request.json
    email = data["email"]
    password = data["password"]
    user = UserManagement().login(email, password)
    if user:
        login_user(user)
        return make_response(jsonify({'message': 'Redirect to the main_paige'}), 200)
    return make_response(jsonify({'message': 'User or password do not match'}), 500)


# DELETE USER
@app.route('/user/delete', methods=['GET', 'DELETE'])
@login_required
def delete_user():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    UserManagement().delete_user(current_user.id)
    return make_response(jsonify({'message': 'Redirect to the signin/login page'}), 200)


# CHANGE USER'S PASSWORD
@app.route('/user/password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    data = request.json
    old_password = data["old_password"]
    new_password = data["new_password"]
    ok = UserManagement().change_password(old_password, new_password, current_user)
    if not ok: 
        return make_response(jsonify({'message': 'Passwords do not match'}), 500)
    return make_response(jsonify({'message': 'Password changed successfully'}), 200)


# CREATING THE MAIN PAGE FOR THE USER
@app.route('/main_page', methods=['GET'])
@login_required
def main_page():
    return make_response(jsonify({'message': 'Success'}), 200)



################# DEALING WITH THE ACCOUNT #################

# CREATING THE OPTION FOR THE USER TO CREATE AN ACCOUNT
@app.route('/create/account', methods=['GET'])
@login_required
def create():
    id = current_user.id
    created = AccountManagement().create_account(id)
    if not created:
        return make_response(jsonify({'message': 'Account not created.'}), 500)
    return make_response(jsonify({'message': 'Redirect to the view_balance page.'}), 200)

# GETTING THE USER'S BALANCE THROUGH A JSON FILE
@app.route('/account/balance', methods=['GET'])
@login_required
def view_balance():
    from flask import jsonify
    owner_id = current_user.id
    expenses = AccountManagement().get_balance(owner_id)
    expenses_json = jsonify(expenses)
    return make_response(expenses_json, 200)
    ####################################################
    # return expenses_json

# CREATING THE OPTION FOR THE USER TO WITHDRAW MONEY
@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    data = request.json
    owner_id = current_user.id
    reason = data["reason"]
    value = data["value"]
    
    ok = AccountManagement().withdraw_money(owner_id, reason, value)
    if ok:
        return make_response(jsonify({'message': 'Redirect to the view_balance page.'}), 200)
    return make_response(jsonify({'message': 'You do not have enough money. Please, make a deposit first.'}), 500)

# CREATING THE OPTION FOR THE USER TO DEPOSIT MONEY
@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'GET':
        return make_response(jsonify({'message': 'Success'}), 200)
    
    data = request.json
    owner_id = current_user.id
    reason = data["reason"]
    value = data["value"]
    ok = AccountManagement().deposit_money(owner_id, reason, value)
    if ok:
        return make_response(jsonify({'message': 'Redirect to the view_balance page.'}), 200)
    return make_response(jsonify({'message': 'An error has ocurred. Please, try again.'}), 500)



# RUNNING THE APP
if __name__ == '__main__':
    app.run(debug=True)