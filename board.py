from tkinter import *
from logic import push

root = Tk()


# general
def board_creation():
    label = Label(width=20, text="Game tic tac toe", font=('Arial', 20, 'bold'))

    # buttons
    restart_button = Button(width=5, height=1, font=('Arial', 28, 'bold'), bg='white',
                            text="Restart", command=lambda: [board_creation(), restart_button.grid_remove()])

    buttons = [
        Button(width=5, height=2, font=('Arial', 28, 'bold'), bg='grey',
               command=lambda hit=i: push(hit, buttons, label, restart_button))
        for i in range(9)]

    # buttons locations
    label.grid(row=0, column=0, columnspan=3)
    row = 1
    col = 0
    for i in range(9):
        buttons[i].grid(row=row, column=col)
        col += 1
        if col == 3:
            row += 1
            col = 0
