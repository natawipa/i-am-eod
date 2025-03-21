# I AM EOD

"I AM EOD" is a bomb-defusal game where players must solve various modules under a time limit. The game challenges players with logic puzzles, quick decision-making, and accuracy to defuse the bomb before time runs out or too many mistakes are made.

## Features
- **Modules**: Includes multiple modules such as:
  - **Password Module**: Solve a sequence of stages by pressing the correct buttons.
  - **Wire Module**: Cut the correct wire based on the given rules.
- **Timer**: A countdown timer adds urgency to the gameplay.
- **Strikes**: Players are allowed a limited number of mistakes before the bomb explodes.
- **Dynamic Logging**: Logs gameplay data, including mistakes, time taken, and completion status.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/natawipa/i-am-eod.git
   cd i-am-eod
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## How to Play
1. Run the game:
   ```bash
   python main.py
   ```
2. **Gameplay**:
   - Solve the active module by interacting with it:
     - **Password Module**: Click the correct buttons in sequence.
     - **Wire Module**: Cut the correct wire based on the rules.
   - Avoid making too many mistakes (strikes) or running out of time.
3. **Win Condition**:
   - Successfully solve all modules before the timer runs out.
4. **Lose Condition**:
   - Run out of time or exceed the maximum allowed strikes.

## Bomb Defusal Instructions
For detailed instructions on how to solve each module, refer to the **Bomb Defusal Manual** included in this repository:  
**[Bomb Defusal Manual.pdf](./Bomb%20Defusal%20Manual.pdf)**