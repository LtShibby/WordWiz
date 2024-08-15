# WordWiz Game

WordWiz is a simple word-guessing game built using Python and Tkinter. Players attempt to guess a randomly selected word within a limited number of attempts, receiving feedback on their guesses.

## Features

- Fetches random words from an external API.
- Provides feedback on each guess:
  - Green for correct letters in the correct position.
  - Yellow for correct letters in the wrong position.
  - White for incorrect letters.
- Option to provide the first letter of the word.
- Option for unlimited attempts.
- Displays incorrect letters guessed by the player.
- Hints available to reveal letters at random positions.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)
- Requests library (install via pip if not available)

## Installation

1. Clone the repository or download the source code.
2. Install the required libraries if not already installed:

   ```bash
   pip install requests
   ```

3. Run the game:

   ```bash
   python WordWiz.py
   ```

## Usage

1. Upon starting the game, a settings window will appear.
2. Choose the number of letters in the word, whether to provide the first letter, and if you want unlimited attempts.
3. Click "Start Game" to begin.
4. Enter your guesses in the provided entry field and press Enter or click "Submit".
5. Use the "Hint" button to reveal a letter if needed.
6. The game will provide feedback on your guesses and display incorrect letters.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the creators of the Random Word API for providing the word data.
- Thanks to the Python and Tkinter communities for their resources and support.
