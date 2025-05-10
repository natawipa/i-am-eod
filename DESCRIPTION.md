# I AM EOD

## 1. Project Overview

In "I AM EOD," players take on the role of an Explosive Ordnance Disposal (EOD) specialist tasked with defusing a bomb before it detonates. The bomb consists of two modules that must be solved under a strict time limit. Players must use logic, quick decision-making, and accuracy to successfully defuse the bomb.

**Mechanics:**

**Modules:**

- **Password Module:** Solve a sequence of stages by pressing the correct buttons based on displayed numbers and rules.
- **Wire Module:** Identify and cut the correct wire based on the given rules.

**Gameplay Rules:**

- Players are allowed up to two mistakes; the bomb detonates on the third mistake.
- The game must be completed within a 3-minute time limit.
- A bomb defusal manual provides the logic for solving each module, but the correct solution depends on the specific details observed during gameplay.

**Functionality:**

- **Real-Time Gameplay:** Players interact with modules in real time.
- **Visual Feedback:** Displays timer, strikes, and module-specific elements.
- **Performance Tracking:** Logs gameplay data, including mistakes, time taken, and completion status.

---

## 2. Project Review

**Existing Project:**

- The game "Keep Talking and Nobody Explodes" is a popular bomb-defusal simulation that emphasizes teamwork, communication, and problem-solving.

**Improvements:**

- **Simplified Modules:** Focuses on easier-to-understand mechanics to ensure accessibility while maintaining a challenge.
- **Solo-Friendly:** Designed for solo play but encourages collaboration with friends for a more engaging experience.
- **Dynamic Logging:** Tracks player performance for detailed analysis.

---

## 3. Programming Development

### 3.1 Game Concept

**Objectives:**

- **Defuse the Bomb:** Solve all modules before the timer runs out.
- **Avoid Mistakes:** Prevent the bomb from detonating by minimizing errors.
- **Analyze Performance:** Review gameplay statistics to improve skills.

**Key Features:**

- **Password Module:** Solve a sequence of stages by pressing the correct buttons.
- **Wire Module:** Cut the correct wire based on the rules.
- **Timer:** Adds urgency to the gameplay.
- **Strikes:** Tracks mistakes; the bomb detonates on the third strike.
- **Statistics Viewer:** Provides detailed visualizations of gameplay data.

---

### 3.2 Object-Oriented Programming Implementation

1. **Game**

   - Manages the overall game loop, rendering, and event handling.
   - Tracks the game state (e.g., running, in-menu, game-over).

2. **Bomb**

   - Represents the bomb and its modules.
   - Tracks strikes, timer, and game ID.
   - Handles module transitions and logging.

3. **Module (Base Class)**

   - Represents a generic module with shared attributes (e.g., `is_solved`, `start_time`).
   - Extended by specific modules such as `PasswordModule` and `WireModule`.

4. **PasswordModule**

   - Implements the password-solving module.
   - Tracks stages, mistakes, and solutions.

5. **WireModule**

   - Implements the wire-cutting module.
   - Tracks wire colors, cut indices, and mistakes.

6. **Drawer**

   - Handles rendering of game elements (e.g., menu, bomb, modules).
   - Provides visual feedback for player actions.

7. **Sound**

   - Manages background music and sound effects.

8. **Stats**
   - Implements the statistics viewer using `tkinter` and `matplotlib`.
   - Loads gameplay logs and generates visualizations.

---

### 3.3 Algorithms Involved

1. **Rule-Based Logic:**

   - Each module follows specific rules that dictate the correct solution. (Refer to the Bomb Defusal Manual for detailed rules.)

2. **Randomization:**

   - Bomb configurations, including passwords and wire colors, are randomized in each game to ensure replayability.

3. **Decision Trees:**
   - Used to determine outcomes based on player choices (e.g., whether the bomb is successfully defused or detonates).

---

## 4. Statistical Data (Prop Stats)

### 4.1 Data Features

**Game Completion Rate:**

- Measures overall player success rate.
- Helps identify game difficulty balance.

**Mistake Distribution by Stage (Password Module):**

- Identifies which password stages are most challenging.

**Time Taken to Defuse Bomb:**

- Measures engagement and skill level.

**Attempts vs Success in Wire Module:**

- Shows the learning curve for wire-cutting.

### 4.2 Data Recording Method

Data is stored in CSV files for easy analysis. Example structure:

| Game ID | Mistakes | Time Taken | Modules Completed | Game Result |
| ------- | -------- | ---------- | ----------------- | ----------- |
| 1       | 2        | 120        | 2                 | Defused     |

---

### 4.3 Data Analysis Report

| Feature Name                       | Graph Objective                         | Graph Type   | X-axis          | Y-axis           |
| ---------------------------------- | --------------------------------------- | ------------ | --------------- | ---------------- |
| Game Completion Rate               | Show success vs failure proportions     | Pie Chart    | Success/Failure | Percentage       |
| Time Taken vs Mistake Rate         | Correlate mistakes with time taken      | Scatter Plot | Time (seconds)  | Mistakes         |
| Most Common Failure Reasons        | Highlight primary failure causes        | Bar Chart    | Failure Reasons | Frequency        |
| Mistake Distribution by Stage      | Identify challenging stages in Password | Stacked Bar  | Stages          | Mistake Counts   |
| Module Completion Time             | Compare time taken for each module      | Boxplot      | Module Type     | Time (seconds)   |
| Time Taken to Defuse Bomb          | Show time distribution                  | Histogram    | Time (seconds)  | Frequency        |
| Attempts vs Success in Wire Module | Analyze success rate by attempts        | Line Graph   | Attempts        | Success Rate (%) |

---

## 5. YouTube

A gameplay video will be added soon.
