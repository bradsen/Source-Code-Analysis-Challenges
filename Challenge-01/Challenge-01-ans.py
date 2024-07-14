from flask import Flask, request, redirect, url_for
from urllib.parse import urlparse
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def is_authenticated_user():
    # This function checks if the user is authenticated and is omitted for brevity

   return True
   #pass

@app.route('/')
def home():
    #If user is not authenticated
    if not is_authenticated_user():
        logging.info('Unauthorized access attempt.')
        return redirect(url_for('login'))
    redirect_url = request.args.get('redirect_url')

    if redirect_url:
        logging.info(f'Redirecting to: {redirect_url}')
        return redirect(redirect_url)

    return 'Welcome to the homepage!'

#How to mitigate open direct vulnerability
#1.Remove parameter
'''
@app.route('/')
def home():
    if not is_authenticated_user():
        logging.info('Unauthorized access attempt.')
        return redirect(url_for('login')) 

    return redirect('/profile')
'''

#2.Implement Allowlist
'''
@app.route('/')
def home():
    if not is_authenticated_user():
        logging.info('Unauthorized access attempt.')
        return redirect(url_for('login')) #Redirect user to the login page
    redirect_url = request.args.get('redirect_url')
    allowlist = ['http://127.0.0.1:5000/profile', 'http://127.0.0.1:5000/contactdetails']
    
    if redirect_url in allowlist:
        logging.info(f'Redirecting to: {redirect_url}')
        return redirect(redirect_url)

    return 'Welcome to the home page!'

'''
#3.Implement Fixed Domain
'''
@app.route('/')
def home():
    if not is_authenticated_user():
        logging.info('Unauthorized access attempt.')
        return redirect(url_for('login')) #Redirect user to the login page
    redirect_url = request.args.get('redirect_url')

    allowed_domain = '127.0.0.1:5000'

    parsed_url = urlparse(redirect_url)
    
    # Check if the parsed URL belongs to the allowed domain
    if parsed_url.scheme == 'http' and parsed_url.netloc == allowed_domain:
        logging.info(f'Redirecting to: {redirect_url}')
        return redirect(redirect_url)

    return 'Welcome to the home page!'
'''


@app.route('/login')
def login():
    # Simulated login page
    return 'Login Page - User authentication goes here.'


@app.route('/profile')
def profile():
    # Simulated profile page
    return 'This is your profile page'

@app.route('/aboutme')
def aboutme():
    # Simulated about me page
    return 'This is about me page'


if __name__ == '__main__':
    app.run(debug=False)
