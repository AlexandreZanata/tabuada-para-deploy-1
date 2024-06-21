from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir acesso de outros dispositivos na mesma rede

# Adicione 'async_mode' como 'threading'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Lista para armazenar os maiores placares de cada jogador como tuplas (player, score)
high_scores = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    player = request.form['player']
    score = int(request.form['score'])

    player_found = False
    # Verifica se o jogador já existe na lista de high_scores
    for i, (p, s) in enumerate(high_scores):
        if p == player:
            # Atualiza a pontuação se o novo placar for maior
            if score > s:
                high_scores[i] = (player, score)
            player_found = True
            break
    
    # Se o jogador não foi encontrado na lista, adiciona como um novo jogador
    if not player_found:
        high_scores.append((player, score))
    
    # Ordena high_scores em ordem decrescente pelo score
    high_scores.sort(key=lambda x: x[1], reverse=True)

    # Emite a atualização de high_scores para todos os clientes conectados
    socketio.emit('update_scores', {'high_scores': high_scores})

    return jsonify(high_scores=high_scores)

@socketio.on('connect')
def handle_connect():
    # Envia a lista atualizada de high_scores quando um cliente se conecta
    emit('update_scores', {'high_scores': high_scores})

if __name__ == '__main__':
    socketio.run(app, debug=True)
