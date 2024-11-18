from flask import Flask, request, jsonify, render_template, redirect, url_for
import user
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')  # This will render the index page after login

@app.route('/login', methods=['POST'])
def login():
    return user.login(request)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


@app.route('/home')
def home():
    return "Welcome to the home Page!"

if __name__ == '__main__':
   app.run(debug = True)