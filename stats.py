import tkinter as tk
from tkinter import ttk
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import ast
from tkinter import scrolledtext


class Stats:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bomb Defusal Statistics")
        self.root.geometry("820x800")
        
        # Set seaborn style
        sns.set_style("whitegrid")
        
        # Load data
        self.game_data = self.load_csv('./logs/game.csv', ['game_id', 'number_of_mistake', 'is_solved', 'time_taken', 'mistake_rate', 'modules_completed', 'game_result'])
        self.password_data = self.load_csv('./logs/password.csv', ['game_id', 'attempts_times', 'most_mistake_stage', 'mistakes_per_stage', 'stages_completed', 'time_taken', 'is_solved'])
        self.wire_data = self.load_csv('./logs/wire.csv', ['game_id', 'attempts_times', 'wires_cut', 'cut_colors', 'wire_num', 'time_taken', 'is_solved'])

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs
        self.create_dashboard_tab()
        self.create_performance_tab()
        self.create_modules_tab()
        
        # Original data tabs (optional)
        self.create_table_tab(self.game_data, "Raw Game Data")
        self.create_table_tab(self.password_data, "Raw Password Data")
        self.create_table_tab(self.wire_data, "Raw Wire Data")

        self.root.mainloop()

    def load_csv(self, file_path, column_names=None):
        """Load and preprocess a CSV file."""
        try:
            data = pd.read_csv(file_path, names=column_names, header=None, comment='#')

            for column in ['mistakes_per_stage', 'cut_colors', 'wires_cut']:
                if column in data.columns:
                    def safe_eval(value):
                        try:
                            return ast.literal_eval(str(value))
                        except (ValueError, SyntaxError):
                            print(f"Warning: Failed to parse {column} value: {value}")
                            return [] if column in ['cut_colors', 'wires_cut'] else None
                    data[column] = data[column].apply(safe_eval)
            
            if 'is_solved' in data.columns:
                data['is_solved'] = data['is_solved'].astype(bool)
            return data
        except pd.errors.ParserError as e:
            print(f"Error loading {file_path}: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def create_dashboard_tab(self):
        """Create the overview dashboard tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dashboard")

        # Create a main container frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True)

        # Create a canvas with proper scroll region
        canvas = tk.Canvas(main_frame)
        canvas.pack(side='left', fill='both', expand=True)

        # Create vertical scrollbar
        scrollbar_y = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollbar_y.pack(side='right', fill='y')

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar_y.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create the scrollable frame INSIDE the canvas
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # Summary statistics frame
        summary_frame = ttk.LabelFrame(scrollable_frame, text="Summary Statistics")
        summary_frame.pack(fill='x', padx=10, pady=5)

        # Calculate stats
        total_games = len(self.game_data)
        success_rate = self.game_data['is_solved'].mean() * 100
        avg_time = self.game_data[self.game_data['is_solved']]['time_taken'].mean()
        most_common_failure = self.game_data[self.game_data['game_result'] != 'defused']['game_result'].value_counts().idxmax()
        wire_success_rate = self.wire_data[self.wire_data['attempts_times'] > 0]['is_solved'].mean() * 100
        password_success_rate = self.password_data['is_solved'].mean() * 100

        # Create summary table
        summary_text = f"""Total Games Played: {total_games}
                        Success Rate: {success_rate:.1f}%
                        Average Time (Success): {avg_time:.1f} sec
                        Most Common Failure: {most_common_failure}
                        Wire Module Success: {wire_success_rate:.1f}%
                        Password Module Success: {password_success_rate:.1f}%"""
        
        summary_label = ttk.Label(summary_frame, text=summary_text, justify='left')
        summary_label.pack(fill='x', padx=5, pady=5)

        # Graphs frame
        graphs_frame = ttk.LabelFrame(scrollable_frame, text="Game Graphs")
        graphs_frame.pack(fill='x', padx=10, pady=5)

        # Game completion pie chart
        pie_frame = ttk.Frame(graphs_frame)
        pie_frame.pack(fill='x', padx=5, pady=5)
        fig1 = plt.Figure(figsize=(7, 4))
        ax1 = fig1.add_subplot(111)
        completion_data = self.game_data['is_solved'].value_counts()
        ax1.pie(completion_data, labels=['Success', 'Failure'], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Game Completion Rate')
        canvas1 = FigureCanvasTkAgg(fig1, master=pie_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='x', padx=5, pady=5)

        # Failure reasons bar chart
        bar_frame = ttk.Frame(graphs_frame)
        bar_frame.pack(fill='x', padx=10, pady=5)

        fig2 = plt.Figure(figsize=(7, 7))
        ax2 = fig2.add_subplot(111)

        failure_data = self.game_data[~self.game_data['is_solved']]['game_result'].value_counts()
        failure_data.plot(kind='bar', ax=ax2)

        ax2.set_title('Failure Reasons')
        ax2.set_ylabel('Count')
        ax2.set_xlabel('Failure Type')

        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)

        canvas2 = FigureCanvasTkAgg(fig2, master=bar_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='x', padx=5, pady=5)

    def create_performance_tab(self):
        """Create the performance analysis tab with proper scrollbars."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Performance")

        # Create a main container frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True)

        # Create a canvas with proper scroll region
        canvas = tk.Canvas(main_frame)
        canvas.pack(side='left', fill='both', expand=True)

        # Create vertical scrollbar
        scrollbar_y = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollbar_y.pack(side='right', fill='y')

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar_y.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create the scrollable frame INSIDE the canvas
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # Time distribution frame
        time_frame = ttk.LabelFrame(scrollable_frame, text="Time Distribution")
        time_frame.pack(fill='x', padx=10, pady=5)

        # Boxplot
        fig1 = plt.Figure(figsize=(7, 4))
        ax1 = fig1.add_subplot(111)
        solved_games = self.game_data[self.game_data['is_solved']]  # Filter solved games
        sns.boxplot(x=solved_games['time_taken'], ax=ax1)
        ax1.set_title('Completion Time Distribution')
        ax1.set_xlabel('Time (seconds)')

        canvas1 = FigureCanvasTkAgg(fig1, master=time_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='x', padx=5, pady=5)

        # Histogram
        fig2 = plt.Figure(figsize=(7, 4))
        ax2 = fig2.add_subplot(111)
        sns.histplot(solved_games['time_taken'], bins=10, kde=True, ax=ax2)
        ax2.set_title('Completion Time Frequency')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Count')

        canvas2 = FigureCanvasTkAgg(fig2, master=time_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='x', padx=5, pady=5)

        # Module comparison
        mod_frame = ttk.LabelFrame(scrollable_frame, text="Module Comparison")
        mod_frame.pack(fill='x', padx=10, pady=5)

        fig3 = plt.Figure(figsize=(7, 7))
        ax3 = fig3.add_subplot(111)

        # Calculate average times
        wire_times = self.wire_data[self.wire_data['is_solved']]['time_taken'].dropna()
        pass_times = self.password_data[self.password_data['is_solved']]['time_taken'].dropna()

        data = pd.DataFrame({
            'Module': ['Wire'] * len(wire_times) + ['Password'] * len(pass_times),
            'Time': list(wire_times) + list(pass_times)
        })

        sns.barplot(x='Module', y='Time', data=data, ax=ax3, errorbar='sd')
        ax3.set_title('Average Module Completion Time')
        ax3.set_ylabel('Time (seconds)')

        canvas3 = FigureCanvasTkAgg(fig3, master=mod_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill='x', padx=5, pady=5)

    def create_modules_tab(self):
        """Create the module details tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Module Details")

        # Create a main container frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True)

        # Create a canvas with proper scroll region
        canvas = tk.Canvas(main_frame)
        canvas.pack(side='left', fill='both', expand=True)

        # Create vertical scrollbar
        scrollbar_y = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollbar_y.pack(side='right', fill='y')

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar_y.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create the scrollable frame INSIDE the canvas
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # Password analysis
        pass_frame = ttk.LabelFrame(scrollable_frame, text="Password Module Analysis")
        pass_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Mistake distribution by stage
        fig1 = plt.Figure(figsize=(7, 4))
        ax1 = fig1.add_subplot(121)

        # Process mistakes per stage
        all_mistakes = []
        for mistakes in self.password_data['mistakes_per_stage'].dropna():
            if isinstance(mistakes, list) and len(mistakes) >= 5:
                all_mistakes.append(mistakes[:5])
        if all_mistakes:    
            mistake_df = pd.DataFrame(all_mistakes, columns=[f'Stage {i+1}' for i in range(5)])
            sns.barplot(data=mistake_df, ax=ax1)
            ax1.set_title('Mistakes by Password Stage')
            ax1.set_ylabel('Mistake Count')
            ax1.set_xlabel('Password Stage')

        # Time vs mistakes scatter
        ax2 = fig1.add_subplot(122)
        time_vs_mistakes = []
        for idx, row in self.password_data.iterrows():
            if isinstance(row['mistakes_per_stage'], list) and not pd.isna(row['time_taken']):
                time_vs_mistakes.append({
                    'time': row['time_taken'],
                    'mistakes': sum(row['mistakes_per_stage'])
                })
        if time_vs_mistakes:
            scatter_df = pd.DataFrame(time_vs_mistakes)
            sns.regplot(x='time', y='mistakes', data=scatter_df, ax=ax2)
            ax2.set_title('Time vs Total Mistakes')
            ax2.set_xlabel('Time (seconds)')
            ax2.set_ylabel('Total Mistakes')
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=pass_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='x', expand=True)

        # Wire analysis
        wire_frame = ttk.LabelFrame(scrollable_frame, text="Wire Module Analysis")
        wire_frame.pack(fill='both', expand=True, padx=20, pady=5)
        fig2 = plt.Figure(figsize=(7, 4))
        ax3 = fig2.add_subplot(121)
        # Attempts vs success
        attempts_success = self.wire_data.groupby('attempts_times')['is_solved'].mean() 
        sns.lineplot(x=attempts_success.index, y=attempts_success.values, ax=ax3, marker='o')
        ax3.set_title('Success Rate by Attempt Count')
        ax3.set_xlabel('Number of Attempts')
        ax3.set_ylabel('Success Rate')
        ax3.set_ylim(0, 1.1)
        # Wire colors pie
        ax4 = fig2.add_subplot(122)
        all_colors = []
        for colors in self.wire_data['cut_colors'].dropna():
            if isinstance(colors, list):
                all_colors.extend(colors)
        if all_colors:
            color_counts = pd.Series(all_colors).value_counts()
            color_counts.plot.pie(ax=ax4, autopct='%1.1f%%')
            ax4.set_title('Cut Wire Colors Distribution')
            ax4.set_ylabel('')
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=wire_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='x', expand=True) 

    def create_table_tab(self, data, title):
        """Create a tab with raw data table."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        
        # Create scrollable text area
        text_area = scrolledtext.ScrolledText(tab, wrap=tk.NONE)
        text_area.pack(fill='both', expand=True)
        
        # Display dataframe as string
        text_area.insert(tk.INSERT, data.to_string())

if __name__ == "__main__":
    Stats()