from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tic-tac-secret'  # For session storage


def init_board():
    return [["" for _ in range(3)] for _ in range(3)]


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)


@app.route("/", methods=["GET", "POST"])
def index():
    if "board" not in session:
        session["board"] = init_board()
        session["turn"] = "X"
        session["winner"] = None
        session["draw"] = False

    board = session["board"]
    turn = session["turn"]
    winner = session["winner"]
    draw = session["draw"]

    if request.method == "POST":
        row = int(request.form["row"])
        col = int(request.form["col"])
        if board[row][col] == "" and winner is None:
            board[row][col] = turn
            if check_winner(board, turn):
                winner = turn
            elif is_draw(board):
                draw = True
            else:
                turn = "O" if turn == "X" else "X"

            session["board"] = board
            session["turn"] = turn
            session["winner"] = winner
            session["draw"] = draw

        return redirect(url_for("index"))

    return render_template("index.html", board=board, turn=turn, winner=winner, draw=draw)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

