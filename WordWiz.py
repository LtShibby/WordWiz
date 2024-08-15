import random
import tkinter as tk
from tkinter import messagebox
import time
import requests

def fetch_random_word(word_length):
    """
    Fetch a random word of a specified length from an external API.

    Args:
        word_length (int): The length of the word to fetch.

    Returns:
        str: A random word of the specified length, or None if an error occurs.
    """
    try:
        response = requests.get(f"https://random-word-api.herokuapp.com/word?number=1&length={word_length}")
        response.raise_for_status()  # Raise an error for bad responses
        word = response.json()[0]  # Extract the word from the JSON response
        return word
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch word: {e}")  # Show error message
        return None

def get_feedback(guess, word):
    """
    Compare the user's guess to the target word and provide feedback.

    Args:
        guess (str): The user's guessed word.
        word (str): The target word.

    Returns:
        list: A list of tuples containing feedback for each letter in the guess.
              Each tuple contains a color and the letter.
    """
    feedback = []
    for i in range(len(guess)):
        if guess[i] == word[i]:
            feedback.append(('green', guess[i]))  # Correct letter and position
        elif guess[i] in word:
            feedback.append(('yellow', guess[i]))  # Correct letter, wrong position
        else:
            feedback.append(('white', guess[i]))  # Incorrect letter
    return feedback

def start_game(word_length, provide_first_letter, unlimited_attempts):
    """
    Start the WordWiz game with the specified settings.

    Args:
        word_length (int): The length of the word to guess.
        provide_first_letter (bool): Whether to provide the first letter of the word.
        unlimited_attempts (bool): Whether the player has unlimited attempts.
    """
    word = fetch_random_word(word_length)  # Fetch a random word
    if not word:
        return  # Exit if word fetching failed

    attempts = 6 if not unlimited_attempts else float('inf')  # Set attempts
    previous_guesses = set()  # Track previous guesses
    start_time = time.time()  # Record the start time
    hints_used = set()  # Track used hints
    previous_attempts = []  # List to keep track of previous attempts
    incorrect_guesses = set()  # Set to keep track of incorrect letters

    def check_guess(event=None):
        """
        Check the user's guess against the target word and update the game state.

        Args:
            event: The event that triggered this function (optional).
        """
        nonlocal attempts
        guess = entry.get().lower()  # Get the user's guess
        if len(guess) != word_length:
            messagebox.showerror("Error", f"Please enter a {word_length}-letter word.")
            return
        if guess in previous_guesses:
            messagebox.showerror("Error", "You've already guessed that word.")
            return

        previous_guesses.add(guess)  # Add guess to previous guesses
        feedback = get_feedback(guess, word)  # Get feedback for the guess
        previous_attempts.append((guess, feedback))  # Store the guess and its feedback

        # Update incorrect guesses
        if all(letter not in word for letter in guess):
            incorrect_guesses.update(set(guess))  # Add incorrect letters to the set

        # Limit to the last 5 attempts
        if len(previous_attempts) > 5:
            previous_attempts.pop(0)  # Remove the oldest attempt

        # Clear the feedback frame and display the last 5 attempts
        for widget in feedback_frame.winfo_children():
            widget.destroy()  # Clear previous feedback

        for attempt, feedback in previous_attempts:
            attempt_frame = tk.Frame(feedback_frame)
            attempt_frame.pack(side="top", pady=2)

            for i, (color, letter) in enumerate(feedback):
                label = tk.Label(attempt_frame, text=letter, width=4, height=2, relief="solid", font=("Helvetica", 18), bg=color)
                label.pack(side="left", padx=2)

        # Display incorrect guesses
        incorrect_guesses_label.config(text=f"Incorrect letters: {', '.join(sorted(incorrect_guesses))}")

        entry.delete(0, tk.END)  # Clear the entry field
        entry.focus()  # Focus back on the entry field

        if guess == word:
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            messagebox.showinfo("Congratulations", f"You've guessed the word in {elapsed_time:.2f} seconds!")
            if messagebox.askyesno("Play Again", "Do you want to play again?"):
                root.destroy()
                start_screen()  # Restart the game
            else:
                root.destroy()  # Exit the game
        else:
            if not unlimited_attempts:
                attempts -= 1  # Decrease attempts
                attempts_label.config(text=f"Attempts remaining: {attempts}")
                if attempts == 0:
                    messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The word was: {word}")
                    if messagebox.askyesno("Play Again", "Do you want to play again?"):
                        root.destroy()
                        start_screen()  # Restart the game
                    else:
                        root.destroy()  # Exit the game

    def give_hint():
        """
        Provide a hint by revealing a letter at a random position that hasn't been guessed correctly yet.
        """
        available_positions = [i for i in range(word_length) if i not in hints_used and all(guess[i] != word[i] for guess in previous_guesses)]
        if available_positions:
            hint_position = random.choice(available_positions)  # Choose a random position for the hint
            hints_used.add(hint_position)  # Mark this position as used
            hint_label.config(text=f"Hint: The letter at position {hint_position + 1} is '{word[hint_position]}'")
        else:
            hint_label.config(text="No more hints available.")  # No hints left

    # Set up the main game window
    root = tk.Tk()
    root.title("WordWiz Game")

    # Welcome message and instructions
    tk.Label(root, text="Welcome to WordWiz!").pack(pady=10)
    tk.Label(root, text=f"You have {attempts if attempts != float('inf') else 'unlimited'} attempts to guess the {word_length}-letter word.").pack(pady=5)

    if provide_first_letter:
        tk.Label(root, text=f"The first letter is: {word[0]}").pack(pady=5)

    entry = tk.Entry(root, font=("Helvetica", 18))  # Entry field for user guesses
    entry.pack(pady=5)
    entry.bind("<Return>", check_guess)  # Bind Enter key to check_guess
    entry.focus()  # Focus on the entry field

    tk.Button(root, text="Submit", command=check_guess).pack(pady=5)  # Submit button
    tk.Button(root, text="Hint", command=give_hint).pack(pady=5)  # Hint button

    feedback_frame = tk.Frame(root)  # Frame for displaying feedback
    feedback_frame.pack(pady=10)

    attempts_label = tk.Label(root, text=f"Attempts remaining: {attempts if attempts != float('inf') else 'Unlimited'}")
    attempts_label.pack(pady=5)  # Label for attempts remaining

    hint_label = tk.Label(root, text="Hint: ")  # Label for hints
    hint_label.pack(pady=5)

    # Add a label to display incorrect guesses
    incorrect_guesses_label = tk.Label(root, text="Incorrect letters: ")
    incorrect_guesses_label.pack(pady=5)

    # Start the main event loop
    root.mainloop()

def start_screen():
    """
    Display the settings screen for the game, allowing the user to configure game options.
    """
    def start():
        word_length = int(word_length_var.get())  # Get the word length from user input
        provide_first_letter = first_letter_var.get()  # Get the first letter option
        unlimited_attempts = unlimited_attempts_var.get()  # Get the unlimited attempts option
        settings_root.destroy()  # Close the settings window
        start_game(word_length, provide_first_letter, unlimited_attempts)  # Start the game with selected options

    # Set up the settings window
    settings_root = tk.Tk()
    settings_root.title("WordWiz Game Settings")

    tk.Label(settings_root, text="WordWiz Game Settings").pack(pady=10)  # Title label

    tk.Label(settings_root, text="Choose the number of letters in the word:").pack(pady=5)  # Instructions
    word_length_var = tk.StringVar(value="5")  # Default word length
    tk.Entry(settings_root, textvariable=word_length_var).pack(pady=5)  # Entry for word length

    first_letter_var = tk.BooleanVar()  # Checkbox for providing the first letter
    tk.Checkbutton(settings_root, text="Provide the first letter of the word", variable=first_letter_var).pack(pady=5)

    unlimited_attempts_var = tk.BooleanVar()  # Checkbox for unlimited attempts
    tk.Checkbutton(settings_root, text="Unlimited attempts", variable=unlimited_attempts_var).pack(pady=5)

    tk.Button(settings_root, text="Start Game", command=start).pack(pady=10)  # Start game button

    settings_root.mainloop()  # Start the settings window event loop

if __name__ == "__main__":
    start_screen()  # Start the game by displaying the settings screen