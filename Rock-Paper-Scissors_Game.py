import tkinter as tk
from tkinter import PhotoImage
import random

# Initialize scores
user_score = 0
computer_score = 0

# Function to get the winner based on the rules
def determine_winner(user_choice, computer_choice):
    global user_score, computer_score
    if user_choice == computer_choice:
        result.set(f"It's a Tie! You both chose {user_choice}.")
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        user_score += 1
        result.set(f"You Win! {user_choice} beats {computer_choice}.")
    else:
        computer_score += 1
        result.set(f"You Lose! {computer_choice} beats {user_choice}.")
    
    # Update scores
    score_label.config(text=f"Your Score: {user_score}  |  Computer Score: {computer_score}")

# Function to handle the user's choice
def user_choice(choice):
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)  # Random choice for the computer
    user_choice_label.config(image=images[choice])  # Display user's image choice
    computer_choice_label.config(image=images[computer_choice])  # Display computer's image choice
    determine_winner(choice, computer_choice)

# Function to ask the user if they want to play again
def play_again():
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    score_label.config(text=f"Your Score: {user_score}  |  Computer Score: {computer_score}")
    result.set("Choose Rock, Paper, or Scissors to start!")
    user_choice_label.config(image=none_image)
    computer_choice_label.config(image=none_image)

# Create the main window
window = tk.Tk()
window.title("Rock Paper Scissors Game")
window.geometry("500x600")
window.config(bg="#E0F7FA")

# Load images for Rock, Paper, Scissors
rock_image = PhotoImage(file="rock.png")  # Add the path to your image file
paper_image = PhotoImage(file="paper.png")
scissors_image = PhotoImage(file="scissor.png")
none_image = PhotoImage()  # Empty image for when nothing is selected

# Map choices to images
images = {
    "Rock": rock_image,
    "Paper": paper_image,
    "Scissors": scissors_image
}

# Create a label for displaying the game result
result = tk.StringVar()
result.set("Choose Rock, Paper, or Scissors to start!")
result_label = tk.Label(window, textvariable=result, font=("Arial", 16), bg="#E0F7FA", fg="#00796B")
result_label.pack(pady=20)

# Create labels for the user's and computer's choices (with images)
user_choice_label = tk.Label(window, image=none_image, bg="#E0F7FA")
user_choice_label.pack(pady=10)

computer_choice_label = tk.Label(window, image=none_image, bg="#E0F7FA")
computer_choice_label.pack(pady=10)

# Create buttons for Rock, Paper, and Scissors choices
rock_button = tk.Button(window, text="Rock", width=20, height=2, font=("Arial", 14), command=lambda: user_choice("Rock"), bg="#00796B", fg="white")
rock_button.pack(pady=5)

paper_button = tk.Button(window, text="Paper", width=20, height=2, font=("Arial", 14), command=lambda: user_choice("Paper"), bg="#00796B", fg="white")
paper_button.pack(pady=5)

scissors_button = tk.Button(window, text="Scissors", width=20, height=2, font=("Arial", 14), command=lambda: user_choice("Scissors"), bg="#00796B", fg="white")
scissors_button.pack(pady=5)

# Label to display scores
score_label = tk.Label(window, text=f"Your Score: {user_score}  |  Computer Score: {computer_score}", font=("Arial", 14), bg="#E0F7FA", fg="#00796B")
score_label.pack(pady=20)

# Button to play again
play_again_button = tk.Button(window, text="Play Again", width=20, height=2, font=("Arial", 14), command=play_again, bg="#FF5722", fg="white")
play_again_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
