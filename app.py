from flask import Flask
from cupcake import cupcake
from user import user
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.register_blueprint(cupcake, url_prefix="/cupcakes")
app.register_blueprint(user, url_prefix="/users")