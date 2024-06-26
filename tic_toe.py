from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Game state
board = [['', '', ''], ['', '', ''], ['', '', '']]
current_player = 'X'

def check_winner():
    # Check rows, columns and diagonals
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]

    # Check for draw
    for row in board:
        for cell in row:
            if cell == '':
                return None

    return 'Draw'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    data = request.json
    row = data['row']
    col = data['col']
    
    if board[row][col] == '':
        board[row][col] = current_player
        winner = check_winner()
        
        if winner:
            response = {'board': board, 'winner': winner}
            # Reset the board
            board = [['', '', ''], ['', '', ''], ['', '', '']]
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            response = {'board': board, 'winner': None}

        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)
