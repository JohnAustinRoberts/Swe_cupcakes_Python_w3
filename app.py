from flask import Flask, abort, redirect, session, url_for, g
from cupcake import cupcake
from user import user
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from urllib.parse import quote_plus, urlencode


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

app.register_blueprint(cupcake, url_prefix="/cupcakes")
app.register_blueprint(user, url_prefix="/users")

@app.route("/login")
def login():
    if not oauth.auth0:
      abort(500)
    
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    if not oauth.auth0:
      abort(500)
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    domain = env.get('AUTH0_DOMAIN')
    if not domain:
      abort(500)

    return redirect(
        "https://" + domain
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.before_request
def load_logged_in_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        g.user = user


@app.route("/")
def home():
    if g.user:
      userToShow = g.get('user')['userinfo']['name']
      return f"<h1>hello {userToShow}</h1>"
    else:
      return 'Hi! Please log in at /login'