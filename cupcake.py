from flask import Blueprint, request, jsonify
from cryptography.fernet import Fernet
from user import login_required
import json
import os

fern = Fernet(os.getenv('ENCRYPTION_KEY', 'none'))
cupcake = Blueprint('cupcake', __name__)

def decrypt_instructions(cupcake):
    cupcake['instructions'] = fern.decrypt(cupcake['instructions']).decode()
    return cupcake

@cupcake.get('/')
@login_required
def fetchAllCupcakes():
    with open("seedData.json", "r") as f:
        data = json.load(f)
        flavor = request.args.get('flavor')
        if flavor:
            return list(map(decrypt_instructions, filter(lambda cupcake: cupcake['flavor'] == flavor, data)))
        
        return list(map(decrypt_instructions, data))

@cupcake.get('/<int:cupcake_id>')
@login_required
def fetchCupcake(cupcake_id):
    with open("seedData.json", "r") as f:
        data = json.load(f)
    
    resulting_cupcake = [
        cupcake for cupcake in data
        if cupcake['id'] == cupcake_id
    ]
    
    if len(resulting_cupcake) == 0:
        response = jsonify({'message': 'Cupcake not found'})
        response.status_code = 404
        return response

    resulting_cupcake[0]['instructions'] = fern.decrypt(resulting_cupcake[0]['instructions']).decode()

    return resulting_cupcake[0]
    

@cupcake.post('/')
@login_required
def addCupcake():
    with open("seedData.json", "r") as f:
        data = json.load(f)
    
    reqData = request.get_json()

    reqData['id'] = data[len(data) - 1]['id'] + 1
    reqData['instructions'] = fern.encrypt(bytes(reqData['instructions'], encoding='utf-8')).decode()

    data.append(reqData)
    
    with open("seedData.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
    
    return reqData
