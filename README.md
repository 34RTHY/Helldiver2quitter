# Helldiver2 Quitter
Ever had your game freeze up on you right when you were about to achieve something amazing? 😤 Fear not, Helldiver2 Quitter is here to save the day! 🚀

### How to Use
#### 1. Download and Open:

- Navigate to the dist folder and open Helldiver2quitter.exe. It will run silently in the background.
#### 2.When the Game Freezes:

- Simply press <strong>Ctrl + Del + Backspace</strong> and watch the magic happen! Your frozen game will be gracefully closed, and you can jump back in without a hitch.

### Features
- Simple to Use: Just run the executable and you're ready to go.
- Silent Operation: Runs in the background without disturbing your gameplay.
- Quick Response: Instantly closes the game with a key combination.
- Reliable: Ensures your system remains responsive even when the game isn't.

## Installation
#### 1.Clone the Repository:
    git clone https://github.com/YourUsername/Helldiver2Quitter.git
#### 2.Navigate to the Directory:
    cd Helldiver2Quitter
#### 3.Run the Executable:
>open Helldiver2quitter.exe

## Technical Details
- Language: Python
- Packaging Tool: PyInstaller
- Dependencies:
    - psutil
    - ctypes
    - keyboard
    - pywin32

## Building the Executable
If you want to build the executable yourself, follow these steps:
### 1.Install Dependencies:
    pip install psutil keyboard pywin32 pyinstaller
### 2.Run PyInstaller:
    pyinstaller --onefile main.py
