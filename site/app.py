#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, make_response, redirect
from functools import wraps
import uuid, jwt, random

app = Flask(__name__)
SECRET_KEY = str(uuid.uuid4())
SIZE = 16
TOTAL_MINES = (SIZE*SIZE) // 8
COLORS = {
    '0' : 'orange',
    '1' : 'purple',
    '2' : 'green',
    '3' : 'red',
    '4' : 'yellow',
    '5' : 'lightblue',
    '6' : 'cyan',
    '7' : 'magenta',
    '8' : 'white',
    'X' : ''
}
matches = {}

def generator_matrix() -> list[list[int]]:
    matrix = [[0 for e in range(SIZE)] for i in range(SIZE)]
    mines = []
    while len(mines) < TOTAL_MINES:
        x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        if matrix[x][y] == 0:
            matrix[x][y] = -1
            mines.append((x, y))
            
    for _ in mines:
        x, y = _
        if x > 0 and matrix[x-1][y] != -1:
            matrix[x-1][y] += 1
        if x < SIZE-1 and matrix[x+1][y] != -1:
            matrix[x+1][y] += 1
        if y > 0 and matrix[x][y-1] != -1:
            matrix[x][y-1] += 1
        if y < SIZE-1 and matrix[x][y+1] != -1:
            matrix[x][y+1] += 1
        
        if x > 0 and y > 0 and matrix[x-1][y-1] != -1:
            matrix[x-1][y-1] += 1
        if x < SIZE-1 and y < SIZE-1 and matrix[x+1][y+1] != -1:
            matrix[x+1][y+1] += 1
        if x > 0 and y < SIZE-1 and matrix[x-1][y+1] != -1:
            matrix[x-1][y+1] += 1
        if x < SIZE-1 and y > 0 and matrix[x+1][y-1] != -1:
            matrix[x+1][y-1] += 1

    return matrix

def viewed_matrix(user: str) -> list[list[str]]:
    final_matrix = [['X' for e in range(SIZE)] for i in range(SIZE)]

    for i in range(SIZE):
        for e in range(SIZE):
            if matches[user][1][i][e]:
                final_matrix[i][e] = str(matches[user][0][i][e])
    return final_matrix

def discover_if_empty(user: str, x: int, y: int):
    discovered = matches[user][1]
    matrix = matches[user][0]
    if discovered[x][y]:
        return 
    if matrix[x][y] == 0:
        discovered[x][y] = True # discovered
        matches[user][2] += 1
        if x > 0:
            discover_if_empty(user, x-1, y)
        if x < SIZE-1:
            discover_if_empty(user, x+1, y)
        if y > 0:
            discover_if_empty(user, x, y-1)
        if y < SIZE-1:
            discover_if_empty(user, x, y+1)
        
        if x > 0 and y > 0:
            discover_if_empty(user, x-1, y-1)
        if x < SIZE-1 and y < SIZE-1:
            discover_if_empty(user, x+1, y+1)
        if x > 0 and y < SIZE-1:
            discover_if_empty(user, x-1, y+1)
        if x < SIZE-1 and y > 0:
            discover_if_empty(user, x+1, y-1)

    elif matrix[x][y] != -1:
        discovered[x][y] = True
        matches[user][2] += 1
    

def get_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies['session']
        if not token:
            return jsonify({'message': 'Invalid session cookie'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid session cookie'}), 401
        return f(data["userID"], *args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def index():
    try:
        token = request.cookies['session']
        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["userID"]
        except:
            raise Exception
        return render_template('index.html', matrix=viewed_matrix(user), len=SIZE, colors=COLORS)
    except:
        token = str(uuid.uuid4())
        jwtEnc = jwt.encode({'userID': token}, SECRET_KEY, algorithm='HS256')
        response = make_response(render_template('index.html', matrix=[['X' for e in range(SIZE)] for i in range(SIZE)], len=SIZE, colors=COLORS))
        matches[token] = [generator_matrix(), [[False for e in range(SIZE)] for i in range(SIZE)], 0] # matrix, discovered, total_discovered
        response.set_cookie('session', jwtEnc)
        return response

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/api/<x>/<y>', methods=['POST'])
@get_token
def api(user, x, y):
    try:
        x = int(x)
        y = int(y)
    except:
        return jsonify({'message': 'Invalid coordinates'}), 401

    user = str(user)
    matrix = matches[user][0].copy()
    discovered = matches[user][1]

    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        return jsonify({'message': 'Invalid coordinates'}), 401
    
    if matrix[x][y] == -1:
        matches.pop(user)
        return jsonify({'message': 'You lost'}), 202

    if discovered[x][y]:
        return jsonify({'message': 'Already discovered'}), 401
    
    if matrix[x][y] == 0:
        discover_if_empty(user, x, y)
    else:
        discovered[x][y] = True
        matches[user][2] += 1
    
    if matches[user][2] == (SIZE*SIZE)-TOTAL_MINES:
        matches.pop(user)
        return jsonify({'message': 'You won'}), 203

    return jsonify({'message': 'OK'}), 200

if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)