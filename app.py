from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from urllib.parse import quote as url_quote

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

high_scores = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    player = request.form['player']
    score = int(request.form['score'])

    player_found = False
    for i, (p, s) in enumerate(high_scores):
        if p == player:
            if score > s:
                high_scores[i] = (player, score)
            player_found = True
            break
    
    if not player_found:
        high_scores.append((player, score))
    
    high_scores.sort(key=lambda x: x[1], reverse=True)

    socketio.emit('update_scores', {'high_scores': high_scores})

    return jsonify(high_scores=high_scores)

@socketio.on('connect')
def handle_connect():
    emit('update_scores', {'high_scores': high_scores})

if __name__ == '__main__':
    socketio.run(app, debug=True)
