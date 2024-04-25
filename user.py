from flask import Blueprint, g, redirect, url_for
from functools import wraps

user = Blueprint('user', __name__)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

@user.get('/')
@login_required
def findProtectedUser(): 
  userToPrint = g.get('user')['userinfo']['name']
  return f'Oh my goodness! It is {userToPrint}'