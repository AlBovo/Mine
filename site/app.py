#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, redirect, session
from apscheduler.schedulers.background import BackgroundScheduler
from time import time
from datetime import timedelta
from functools import wraps
import uuid, random, json, re, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', str(uuid.uuid4()))
SIZE = os.getenv('SIZE', 16)
TOTAL_MINES = (SIZE*SIZE) // 8
COLORS = {
    '0' : 'orange',
    '1' : 'purple',
    '2' : 'forestgreen',
    '3' : 'red',
    '4' : 'orangered',
    '5' : 'violet',
    '6' : 'deeppink',
    '7' : 'magenta',
    '8' : 'green',
    'B' : 'black',
    'X' : ''
}

try:
    scoardboard = json.loads(open('scoreboard.json', 'r').read())
    assert type(scoardboard) == list
except:
    scoardboard = []

matches = {}

def save_scoardboard():
    print("Saving scoreboard...")
    open("scoreboard.json", "w").write(json.dumps(scoardboard))

    copy = []
    for user in matches:
        if int(time()) - matches[user][3] >= 600: # clean matches after 10 minutes of inactivity
            copy.append(user)

    for user in copy:
        matches.pop(user)
    
scheduler = BackgroundScheduler()
scheduler.add_job(save_scoardboard, 'interval', minutes=10)

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

def discover_if_empty(user: str, x: int, y: int):
    discovered = matches[user][1]
    matrix = matches[user][0]
    if discovered[x][y] not in ['X', 'B']:
        return 
    if matrix[x][y] == 0:
        discovered[x][y] = str(matrix[x][y])
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
        discovered[x][y] = str(matrix[x][y])
        matches[user][2] += 1
    
def get_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'session' not in session:
            token = str(uuid.uuid4())
            matches[token] = [
                generator_matrix(), # matrix
                [['X' for e in range(SIZE)] for i in range(SIZE)], # discovered
                0, # total discovered
                int(time()), # last activity
                int(time())] # start time
            session['session'] = token
            return redirect('/')
        return f(session['session'], *args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
@get_token
def index(token):
    matches[token][3] = int(time())
    return render_template('index.html', matrix=matches[token][1], colors=COLORS)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/scoreboard', methods=['GET'])
def show_scoreboard():
    table = []
    for i in scoardboard:
        t = str(timedelta(seconds=i[0]))
        table.append([t, i[1]])
    return render_template('scoreboard.html', scoreboard=table)

@app.route('/add_user', methods=['GET'])
def add_user():
    return render_template('add_user.html')

@app.route('/api/<int:x>/<int:y>', methods=['POST'])
@get_token
def api(user: str, x: int, y: int):
    # if x.isdigit() and y.isdigit():
    #     x = int(x)
    #     y = int(y)
    # else:
    #     return jsonify({'message': 'Invalid coordinates'}), 401
    
    matrix = matches[user][0].copy()
    discovered = matches[user][1]
    matches[user][3] = int(time())

    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        return jsonify({'message': 'Invalid coordinates'}), 401
    
    if matrix[x][y] == -1:
        for i in range(SIZE):
            for j in range(SIZE):
                if matrix[i][j] == -1:
                    discovered[i][j] = 'B'
                else:
                    discovered[i][j] = str(matrix[i][j])
        return jsonify({'message': 'You lost'}), 202

    if discovered[x][y] not in ['X', 'B']:
        return jsonify({'message': 'Already discovered'}), 401
    
    if matrix[x][y] == 0:
        discover_if_empty(user, x, y)
    else:
        discovered[x][y] = str(matches[user][0][x][y])
        matches[user][2] += 1
    
    if matches[user][2] == (SIZE*SIZE)-TOTAL_MINES:
        matches[user][3] = int(time()) - matches[user][3]
        return jsonify({'message': 'You won'}), 203
    
    
    return jsonify({'message': 'OK'}), 200

@app.route('/api/addflag/<x>/<y>', methods=['POST'])
@get_token
def add_flag(user: str, x: str, y: str):
    if x.isdigit() and y.isdigit():
        x = int(x)
        y = int(y)
    else:
        return jsonify({'message': 'Invalid coordinates'}), 401

    matches[user][3] = int(time())
    user = str(user)
    discovered = matches[user][1]

    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        return jsonify({'message': 'Invalid coordinates'}), 401
    
    if discovered[x][y] != 'X':
        return jsonify({'message': 'Already discovered'}), 401
    
    discovered[x][y] = 'B'
    return jsonify({'message': 'OK'}), 200

@app.route('/api/clear', methods=['POST'])
@get_token
def clear(user: str):
    try:
        matches.pop(user)
        matches[user] = [
            generator_matrix(), # matrix
            [['X' for e in range(SIZE)] for i in range(SIZE)], # discovered
            0, # total discovered
            int(time()), # last activity
            int(time())] # start time
        # i regenerate the matrix
        return jsonify({'message': 'OK'}), 200
    except:
        return jsonify({'message': 'Invalid session cookie'}), 401

@app.route('/api/scoreboard', methods=['POST'])
@get_token
def scoreboard(user: str):
    if matches[user][2] != (SIZE*SIZE)-TOTAL_MINES:
        return render_template('add_user.html', error='You must win the game to submit your score')
    
    username = str(request.form['username']).strip()
    print(username)
    if not username:
        return render_template('add_user.html', error='You must insert a username')

    if len(re.findall(r'[a-zA-Z0-9_\-]', username)) < len(username):
        return render_template('add_user.html', error='Invalid username')

    points = int(time()) - matches[user][4]
    matches[user][4] = int(time())
    scoardboard.append([points, username])

    scoardboard.sort(key=lambda x: x[0])
    return redirect('/scoreboard')

@app.route('/api/show', methods=['POST'])
@get_token
def show(user: str):
    matrix = matches[user][0]
    discovered = matches[user][1]
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == -1:
                discovered[i][j] = 'B'
            else:
                discovered[i][j] = str(matrix[i][j])
    return redirect('/')