from flask import Blueprint, request, abort
from authMiddleware import require_basic_auth, require_jwt_token
import json, bcrypt, os, datetime, jwt

user = Blueprint('user', __name__)

@user.errorhandler(400)
def user_invalid_input(e):
   return 'Invalid data', 400

@user.errorhandler(409)
def user_already_exists(e):
   return 'User already exists', 409

@user.post('/')
def registerUser():
    with open("userData.json", "r") as f:
        data = json.load(f)

    reqData = request.get_json()

    if not 'email' in reqData or not 'password' in reqData:
      abort(400)
    
    if reqData['email'] in data: 
      abort(409)
    data[reqData['email']] = bcrypt.hashpw(reqData['password'].encode('utf-8'), bcrypt.gensalt()).decode()

    with open("userData.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
    
    outfile.close()
    
    return reqData

@user.get('/login')
@require_basic_auth
def loginUser(user):
  with open("userData.json", "r") as f:
    data = json.load(f)
  
  if not user:
    abort(401)
  
  email = list(user.keys())[0]

  if email not in data:
     abort(404)

  if not bcrypt.checkpw(user[email].encode('utf-8'), 
                    data[email].encode('utf-8')):
    abort(401)

  payload = {'email': email, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=24)}
  secret = os.getenv('JWT_SECRET')
  if not secret: 
    abort(404)
  encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
  return encoded_jwt

@user.get('/')
@require_jwt_token
def findProtectedUser(user):
  
  if not user:
    abort(401)
  
  return user