from tkinter import *
from tkinter import filedialog, messagebox
import os
import sys
import tkinter as tk
import random
import string

words = ["grapes", "lion", "bus", "dad", "sAunday"]

def newWindow():
    new_window = Tk()
    window.destroy()

def exitFile():
    sys.exit()

def saveFile(username, progress):
    filename = f"{username}.txt"
    with open(filename, "w") as file:
        file.write(str(progress))

def openFile(username):
    filename = f"{username}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            progress = int(file.read())
            return progress
    else:
        return 0

def create_table(rows, columns, words_list, correct_word):
    def cell_clicked(row, col):
        # Toggle highlighting of the clicked cell
        if cell_labels[row][col]["bg"] == "white":
            cell_labels[row][col]["bg"] = "yellow"
        else:
            cell_labels[row][col]["bg"] = "white"

    def submit_button_clicked():
        user_input = get_highlighted_word()
        if user_input == correct_word:
            messagebox.showinfo("Congratulations", f"Congratulations, {username}! You found the word {correct_word}.")
            root.destroy()
        else:
            messagebox.showinfo("Wrong Word", "Wrong word. Keep trying!")

    def get_highlighted_word():
        highlighted_cells = [(i, j) for i in range(rows) for j in range(columns) if cell_labels[i][j]["bg"] == "yellow"]
        highlighted_cells.sort()  # Sort the cells to get the correct order
        return ''.join(table_data[i][j] for i, j in highlighted_cells)

    root = tk.Tk()
    root.title("Word Search Table")

    # Create labels for each cell in the table
    table_data = [['' for _ in range(columns)] for _ in range(rows)]
    cell_labels = [[None for _ in range(columns)] for _ in range(rows)]

    # Choose a random direction for the correct word
    direction = random.choice([(0, 1), (1, 0), (1, 1), (-1, 1)])

    # Choose a starting position for the correct word
    start_row = random.randint(0, rows - 1)
    start_col = random.randint(0, columns - 1)

    # Ensure that the correct word fits in the chosen direction
    while not (
        start_row + (len(correct_word) - 1) * direction[0] < rows and
        start_col + (len(correct_word) - 1) * direction[1] < columns and
        start_row - (len(correct_word) - 1) * direction[0] >= 0 and
        start_col - (len(correct_word) - 1) * direction[1] >= 0
    ):
        start_row = random.randint(0, rows - 1)
        start_col = random.randint(0, columns - 1)

    # Place the correct word in the table
    for i in range(len(correct_word)):
        row, col = start_row + i * direction[0], start_col + i * direction[1]
        table_data[row][col] = correct_word[i]

    # Fill remaining spots with random lowercase letters
    for i in range(rows):
        for j in range(columns):
            if table_data[i][j] == '':
                table_data[i][j] = random.choice(string.ascii_lowercase)

    # Display the correct word
    print(f"Find the word: {correct_word}")

    # Create labels for each cell in the table
    for i in range(rows):
        for j in range(columns):
            label = tk.Label(root, text=table_data[i][j], borderwidth=1, relief="solid", width=7, height=4, bg="white")
            label.grid(row=i, column=j)
            label.bind("<Button-1>", lambda event, row=i, col=j: cell_clicked(row, col))
            cell_labels[i][j] = label

    # Add a submit button
    submit_button = tk.Button(root, text="Submit", command=submit_button_clicked)
    submit_button.grid(row=rows, columnspan=columns)

    root.mainloop()

def start_game():
    # Let the computer choose a random word for the user to find
    correct_word = random.choice(words)

    # Get the username
    global username
    username = FirstNameEntry.get()

    # Call the function to create the table with words and random lowercase letters
    create_table(8, 8, words, correct_word)

window = Tk()
window.geometry("300x300")
window.title("Word Search Game")
window.config(background="white")

titlelabel = Label(window, text="Enter your info").grid(row=0, column=0, columnspan=2)
FirstNameLabel = Label(window, text="First name: ", width=20).grid(row=1, column=0)
FirstNameEntry = Entry(window)
FirstNameEntry.grid(row=1, column=1)

LastNameLabel = Label(window, text="Last name: ", width=20).grid(row=2, column=0)
LastNameEntry = Entry(window)
LastNameEntry.grid(row=2, column=1)

# Removed the first "Submit" button
startButton = Button(window, text="Start", command=start_game, bg="blue", fg="white").grid(row=3, column=0, columnspan=2)

menubar = Menu(window)
window.config(menu=menubar)

FileMenu = Menu(menubar)
menubar.add_cascade(label="File", menu=FileMenu)
FileMenu.add_command(label="New", command=newWindow)
FileMenu.add_command(label="Save", command=lambda: saveFile(FirstNameEntry.get(), 0))
FileMenu.add_command(label="Open", command=lambda: openFile(FirstNameEntry.get()))
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=exitFile)

window.mainloop()
