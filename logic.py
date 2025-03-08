import random
import time


def create_game_state():
    global game, game_left, turn, not_lose_combo
    game = ['None'] * 9  # Create a 9-cell game grid
    game_left = list(range(9))  # Create a list of available cells for the next move
    turn = 0  # turn counter
    not_lose_combo = []


def restart_game(restart_button):
    create_game_state()
    restart_button.grid(row=4, column=0, columnspan=3, sticky='we')


create_game_state()
win_cords_all = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def check_win():
    global game, win_cords_all
    for coord in win_cords_all:
        if game[coord[0]] == game[coord[1]] == game[coord[2]] and game[coord[0]] is not None:
            return game[coord[0]]
    return False


def ai(center_is, buttons, label, restart_button):
    global ai_hit, coord

    if center_is is False and turn == 0:  # If it's the first turn and the center cell is not occupied, choose a random cell
        ai_hit = random.choice([0, 2, 6, 8])
    elif center_is is True and turn == 0:  # If it's the first turn and the center cell is occupied, choose the center cell
        ai_hit = 4

    if turn > 0:  # Check each winning coordinate set
        for coord in win_cords_all:
            combo = game[coord[0]] + game[coord[1]] + game[coord[2]]
            if combo.count('O') == 2 and combo.count('None') == 1:
                ai_hit = coord[combo.index('None')]
                break
            else:
                not_lose_combo.append((combo, coord))
        else:
            for combo, coord in not_lose_combo:
                if combo.count('X') == 2 and combo.count('None') == 1:
                    ai_hit = coord[combo.index('None')]
                    break

        if ai_hit not in game_left and len(game_left) > 1:  # If the mirrored cell isn't available, choose a random cell
            ai_hit = random.choice(game_left)

    # Update the game grid and button state
    game[ai_hit] = 'O'
    time.sleep(0.05)
    buttons[ai_hit].config(text='0', bg='white', state='disabled')
    if len(game_left) > 1:
        game_left.remove(ai_hit)
    else:
        label['text'] = "Game Over!"
        restart_game(restart_button)


def push(human_hit, buttons, label, restart_button):
    global game, game_left, turn

    def game_over(text):
        for i in game_left:
            buttons[i].config(state='disabled')
        label['text'] = f"{text}"

    game[human_hit] = 'X'
    buttons[human_hit].config(text='X', bg='white', state='disabled')
    game_left.remove(human_hit)

    win = check_win()
    if win == 'X':
        game_over("You Won!")
        restart_game(restart_button)
    else:
        if human_hit == 4:  # If the human chose the center cell, update the game grid and call AI to hit
            ai(False, buttons, label, restart_button)
        else:  # If the human chose a non-center cell, call AI to hit with the correct center_is flag
            ai(True, buttons, label, restart_button)

        win = check_win()
        if win == 'O':
            game_over("You Lose!")
            restart_game(restart_button)
        else:
            turn += 1
