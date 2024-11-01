from flask import Flask, render_template, request, redirect, url_for, session
from auth import Auth
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
authentication = Auth(app)

@app.route("/")
def displayHomePage():
    return render_template("home.html")




@app.route("/login", methods=['GET', 'POST'])
def displayLoginPage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authentication.validate_login(email=email, password=password)
        if user:
            session['user_id'] = user.id
            return redirect(url_for('displayDashboardPage'))
    return render_template("login.html")




@app.route("/register", methods=['GET', 'POST'])
def displayRegisterPage():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if not authentication.isEmailTaken(email=email):
            authentication.register_user(name=name, email=email, password=password)
            user = authentication.validate_login(email=email, password=password)
            session['user_id'] = user.id
            return redirect(url_for('displayDashboardPage'))
    return render_template('register.html')




@app.route('/dashboard', methods=['GET', 'POST'])
def displayDashboardPage():
    if 'user_id' not in session:
        return redirect(url_for('displayLoginPage'))
    user_id = session['user_id']
    if request.method == 'POST':
        entry_text = request.form['entry_text']
        if entry_text:
            authentication.add_entry(user_id=user_id, entry_text=entry_text, entry_date=datetime.utcnow())
    entries = authentication.get_user_entries(user_id=user_id)
    return render_template('dashboard.html', entries=entries)



@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if 'user_id' in session:
        authentication.delete_entry(entry_id)
    return redirect(url_for('displayDashboardPage'))




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('displayHomePage'))



if __name__ == '__main__':
    app.run()
