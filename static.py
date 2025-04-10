import ast
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Statistics(tk.Frame):
    def __init__(self, parent=None):
        if parent is None:
            self.root = tk.Tk()
            self.root.title("Bomb Defusal Game Statistics")
            self.root.geometry("800x600")
            self.is_root_created = True
            parent = self.root
        else:
            self.root = parent

        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Load all CSV data once
        self.game_data = self.load_csv('./logs/game.csv', ['game_id', 'number_of_mistake', 'is_solved', 'time_taken', 'mistake_rate', 'modules_completed'])
        self.password_data = self.load_csv('./logs/password.csv', ['game_id', 'attempts_times', 'most_mistake_stage', 'mistakes_per_stage', 'stages_completed', 'time_taken', 'is_solved'])
        self.wire_data = self.load_csv('./logs/wire.csv', ['game_id', 'attempts_times', 'wires_cut', 'cut_colors', 'time_taken', 'is_solved'])

        self.create_widgets()

    def create_widgets(self):
        # Create a LabelFrame for dropdown and actions
        self.frame_controls = ttk.LabelFrame(self, text="Statistics Options")
        self.frame_controls.grid(row=1, column=0, sticky="news", padx=10, pady=10)

        # Add a dropdown menu (combobox) for selecting the chart type
        self.chart_selector = ttk.Combobox(self.frame_controls, state="readonly")
        self.chart_selector['values'] = (
            'Time Taken to Defuse the Bomb',
            'Number of Mistakes Made',
            'Success Rate',
            'Most Commonly Cut Wire (Wire Module)',
            'Module Time Consumption (%)',
            'Most Mistake Stage (Password Module)'
        )
        self.chart_selector.current(0)  # Set default selection
        self.chart_selector.grid(row=0, column=0, padx=10, pady=5)

        # Add a button to display the selected chart
        ttk.Button(self.frame_controls, text="Show Chart", command=self.show_selected_chart).grid(row=0, column=1, padx=10, pady=5)

        # Add an exit button
        ttk.Button(self.frame_controls, text="Quit", command=self.quit_app).grid(row=0, column=2, columnspan=2, padx=10, pady=5)

        # Create a Matplotlib figure and plotting axes
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot()

        # Create a canvas to host the figure and place it into the main window
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0, sticky="news", padx=10, pady=10)

    def load_csv(self, file_path, column_names):
        """Load and preprocess a CSV file."""
        try:
            data = pd.read_csv(file_path, header=0, names=column_names)
            if 'mistakes_per_stage' in data.columns:
                # Convert mistakes_per_stage from string to list
                data['mistakes_per_stage'] = data['mistakes_per_stage'].apply(ast.literal_eval)
            if 'cut_colors' in data.columns:
                # Convert cut_colors from string to list
                data['cut_colors'] = data['cut_colors'].apply(ast.literal_eval)
            return data
        except FileNotFoundError:
            self.show_error(f"Error: '{file_path}' file not found.")
            return None
        except Exception as e:
            self.show_error(f"Error loading '{file_path}': {str(e)}")
            return None

    def quit_app(self):
        """Quit the application."""
        if self.is_root_created:
            self.root.destroy()

    def show_selected_chart(self):
        """Display the chart based on the selected option in the dropdown."""
        selected_chart = self.chart_selector.get()
        if selected_chart == 'Time Taken to Defuse the Bomb':
            self.show_time_taken_histogram()
        elif selected_chart == 'Number of Mistakes Made':
            self.show_number_of_mistakes_chart()
        elif selected_chart == 'Success Rate':
            self.show_success_rate_chart()
        elif selected_chart == 'Most Commonly Cut Wire (Wire Module)':
            self.show_most_commonly_cut_wire_chart()
        elif selected_chart == 'Module Time Consumption (%)':
            self.show_module_time_consumption_chart()
        elif selected_chart == 'Most Mistake Stage (Password Module)':
            self.show_most_mistake_stage_chart()

    def show_error(self, message):
        """Display an error message in a popup window."""
        error_window = tk.Toplevel(self)
        error_window.title("Error")
        ttk.Label(error_window, text=message).pack(padx=10, pady=10)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=5)
        error_window.transient(self)
        error_window.grab_set()
        error_window.focus_set()
        error_window.wait_window()

    def show_time_taken_histogram(self):
        """Chart: Time Taken to Defuse the Bomb (Bar Chart)."""
        self.ax.clear()

        # Filter successful games
        successful_games = self.game_data[self.game_data['is_solved'] == True]

        # Plot bar chart with game_id on the x-axis and time_taken on the y-axis
        self.ax.bar(
            successful_games['game_id'],
            successful_games['time_taken'],
            color='#AEC6CF',  # Pastel blue
            edgecolor='black'
        )
        self.ax.set_title('Time Taken to Defuse the Bomb (Successful Games)')
        self.ax.set_xlabel('Game ID')
        self.ax.set_ylabel('Time Taken (seconds)')
        self.ax.set_xticks(successful_games['game_id'])  # Ensure all game IDs are shown on the x-axis
        self.fig_canvas.draw()

    def show_number_of_mistakes_chart(self):
        """Chart: Number of Mistakes Made (Bar Chart)."""
        self.ax.clear()
        mistakes = self.game_data['number_of_mistake'].value_counts()
        mistakes.plot(kind='bar', ax=self.ax, color='#FFB347')  # Pastel orange
        self.ax.set_title('Number of Mistakes Made')
        self.ax.set_xlabel('Mistakes')
        self.ax.set_ylabel('Frequency')
        self.fig_canvas.draw()

    def show_success_rate_chart(self):
        """Chart: Success Rate (Pie Chart)."""
        self.ax.clear()
        success_counts = self.game_data['is_solved'].value_counts()
        labels = ['Solved', 'Failed']
        self.ax.pie(success_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#77DD77', '#FF6961'])  # Pastel green and red
        self.ax.set_title('Success Rate')
        self.fig_canvas.draw()

    def show_most_commonly_cut_wire_chart(self):
        """Chart: Most Commonly Cut Wire (Pie Chart)."""
        self.ax.clear()
        all_colors = [color for sublist in self.wire_data['cut_colors'].dropna() for color in sublist]
        color_counts = pd.Series(all_colors).value_counts()
        pastel_colors = ['#FFB347', '#AEC6CF', '#FDFD96', '#77DD77', '#FF6961']  # Pastel orange, blue, yellow, green, red
        color_counts.plot(kind='pie', ax=self.ax, autopct='%1.1f%%', startangle=90, colors=pastel_colors[:len(color_counts)])
        self.ax.set_title('Most Commonly Cut Wire')
        self.ax.set_ylabel('')  # Hide y-axis label
        self.fig_canvas.draw()

    def show_module_time_consumption_chart(self):
        """Chart: Average Module Time Consumption (Pie Chart)."""
        self.ax.clear()

        # Filter successful games
        successful_games = self.game_data[self.game_data['is_solved'] == True]

        # Initialize totals for the two modules
        module_time_totals = {'Password Module': 0, 'Wire Module': 0}

        # Iterate through successful games
        for _, game in successful_games.iterrows():
            game_id = game['game_id']

            # Get time taken for the password module
            password_time = self.password_data[self.password_data['game_id'] == game_id]['time_taken'].sum()

            # Get time taken for the wire module
            wire_time = self.wire_data[self.wire_data['game_id'] == game_id]['time_taken'].sum()

            # Accumulate time for each module
            module_time_totals['Password Module'] += password_time
            module_time_totals['Wire Module'] += wire_time

        # Calculate average time consumption percentages
        total_time_all_modules = sum(module_time_totals.values())
        if total_time_all_modules > 0:
            module_percentages = {module: (time / total_time_all_modules) * 100 for module, time in module_time_totals.items()}
        else:
            module_percentages = {'Password Module': 0, 'Wire Module': 0}

        # Plot the pie chart with pastel colors
        pastel_colors = ['#AEC6CF', '#FFB347']  # Pastel blue and pastel orange
        self.ax.pie(
            module_percentages.values(),
            labels=module_percentages.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=pastel_colors
        )
        self.ax.set_title('Average Module Time Consumption (%)')
        self.ax.set_ylabel('')  # Hide y-axis label
        self.fig_canvas.draw()

    def show_most_mistake_stage_chart(self):
        """Chart: Most Mistake Stage (Pie Chart)."""
        self.ax.clear()

        # Sum mistakes for each stage across all games
        stage_totals = [0, 0, 0, 0, 0]  # Initialize totals for 5 stages
        for stages in self.password_data['mistakes_per_stage'].dropna():
            for i, mistakes in enumerate(stages):
                stage_totals[i] += mistakes

        # Calculate percentages for each stage
        total_mistakes = sum(stage_totals)
        if total_mistakes > 0:
            stage_percentages = [(mistakes / total_mistakes) * 100 for mistakes in stage_totals]
        else:
            stage_percentages = [0] * 5  # Handle case with no mistakes

        # Plot the pie chart with pastel colors
        pastel_colors = ['#FFB347', '#AEC6CF', '#FDFD96', '#77DD77', '#FF6961']  # Pastel orange, blue, yellow, green, red
        stage_labels = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5']
        self.ax.pie(
            stage_percentages,
            labels=stage_labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=pastel_colors
        )
        self.ax.set_title('Most Mistake Stage (Password Module)')
        self.ax.set_ylabel('')  # Hide y-axis label
        self.fig_canvas.draw()

    def run(self):
        """Run the Tkinter main loop."""
        if self.is_root_created:
            self.root.mainloop()
        else:
            print("Root window not created.")