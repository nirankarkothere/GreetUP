import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("600x700")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(False, False)
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.lower_bound = 1
        self.upper_bound = 100
        self.difficulty = "Medium"
        self.game_active = False
        self.high_score = self.load_high_score()
        
        # Initialize GUI
        self.create_widgets()
        self.new_game()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#34495E', height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 NUMBER GUESSING GAME 🎮",
            font=('Arial', 24, 'bold'),
            bg='#34495E',
            fg='#F1C40F'
        )
        title_label.pack(expand=True)
        
        # Score Frame
        score_frame = tk.Frame(self.root, bg='#2C3E50')
        score_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # High Score
        self.high_score_label = tk.Label(
            score_frame,
            text=f"🏆 High Score: {self.high_score}",
            font=('Arial', 14, 'bold'),
            bg='#2C3E50',
            fg='#F1C40F'
        )
        self.high_score_label.pack(side='left')
        
        # Attempts
        self.attempts_label = tk.Label(
            score_frame,
            text="Attempts: 0",
            font=('Arial', 14),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        self.attempts_label.pack(side='right')
        
        # Game Info Frame
        info_frame = tk.Frame(self.root, bg='#34495E', height=150)
        info_frame.pack(fill='x', padx=20, pady=(0, 20))
        info_frame.pack_propagate(False)
        
        # Range Display
        self.range_label = tk.Label(
            info_frame,
            text="Guess the number between 1 and 100",
            font=('Arial', 16),
            bg='#34495E',
            fg='#ECF0F1'
        )
        self.range_label.pack(pady=(20, 10))
        
        # Hint Display
        self.hint_label = tk.Label(
            info_frame,
            text="",
            font=('Arial', 14, 'italic'),
            bg='#34495E',
            fg='#F39C12'
        )
        self.hint_label.pack()
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='#2C3E50')
        input_frame.pack(pady=20)
        
        # Guess Entry
        self.guess_entry = tk.Entry(
            input_frame,
            font=('Arial', 24),
            width=10,
            justify='center',
            bg='#ECF0F1',
            fg='#2C3E50',
            bd=5,
            relief='groove'
        )
        self.guess_entry.pack(side='left', padx=(0, 10))
        self.guess_entry.bind('<Return>', lambda e: self.make_guess())
        
        # Guess Button
        self.guess_btn = tk.Button(
            input_frame,
            text="GUESS",
            font=('Arial', 16, 'bold'),
            bg='#27AE60',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.make_guess
        )
        self.guess_btn.pack(side='right')
        
        # Feedback Frame
        feedback_frame = tk.Frame(self.root, bg='#34495E', height=100)
        feedback_frame.pack(fill='x', padx=20, pady=(0, 20))
        feedback_frame.pack_propagate(False)
        
        self.feedback_label = tk.Label(
            feedback_frame,
            text="",
            font=('Arial', 14),
            bg='#34495E',
            fg='#ECF0F1',
            wraplength=500
        )
        self.feedback_label.pack(expand=True)
        
        # Difficulty Frame
        diff_frame = tk.Frame(self.root, bg='#2C3E50')
        diff_frame.pack(pady=(0, 20))
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Arial', 12),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(side='left', padx=(0, 10))
        
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulties = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard"), ("Expert", "Expert")]
        
        for text, value in difficulties:
            rb = tk.Radiobutton(
                diff_frame,
                text=text,
                value=value,
                variable=self.difficulty_var,
                bg='#2C3E50',
                fg='#ECF0F1',
                selectcolor='#2C3E50',
                activebackground='#2C3E50',
                command=self.change_difficulty
            )
            rb.pack(side='left', padx=5)
        
        # Control Buttons Frame
        control_frame = tk.Frame(self.root, bg='#2C3E50')
        control_frame.pack(pady=20)
        
        # New Game Button
        self.new_game_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=('Arial', 12, 'bold'),
            bg='#3498DB',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.new_game
        )
        self.new_game_btn.pack(side='left', padx=5)
        
        # Hint Button
        self.hint_btn = tk.Button(
            control_frame,
            text="💡 Hint",
            font=('Arial', 12, 'bold'),
            bg='#F39C12',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.give_hint
        )
        self.hint_btn.pack(side='left', padx=5)
        
        # Show Answer Button
        self.show_answer_btn = tk.Button(
            control_frame,
            text="🔍 Show Answer",
            font=('Arial', 12, 'bold'),
            bg='#E74C3C',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.show_answer
        )
        self.show_answer_btn.pack(side='left', padx=5)
        
        # Previous guesses Frame
        prev_frame = tk.Frame(self.root, bg='#34495E')
        prev_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        tk.Label(
            prev_frame,
            text="Previous Guesses:",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack(pady=(10, 5))
        
        # Listbox for previous guesses
        list_frame = tk.Frame(prev_frame, bg='#34495E')
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.guesses_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='#ECF0F1',
            fg='#2C3E50',
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.guesses_listbox.pack(fill='both', expand=True)
        
        scrollbar.config(command=self.guesses_listbox.yview)
        
        # Bind hover effects
        self.guess_btn.bind('<Enter>', lambda e: self.guess_btn.configure(bg='#229954'))
        self.guess_btn.bind('<Leave>', lambda e: self.guess_btn.configure(bg='#27AE60'))
        self.new_game_btn.bind('<Enter>', lambda e: self.new_game_btn.configure(bg='#2875A7'))
        self.new_game_btn.bind('<Leave>', lambda e: self.new_game_btn.configure(bg='#3498DB'))
        self.hint_btn.bind('<Enter>', lambda e: self.hint_btn.configure(bg='#E67E22'))
        self.hint_btn.bind('<Leave>', lambda e: self.hint_btn.configure(bg='#F39C12'))
        self.show_answer_btn.bind('<Enter>', lambda e: self.show_answer_btn.configure(bg='#C0392B'))
        self.show_answer_btn.bind('<Leave>', lambda e: self.show_answer_btn.configure(bg='#E74C3C'))
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists("highscore.json"):
                with open("highscore.json", 'r') as file:
                    data = json.load(file)
                    return data.get('high_score', float('inf'))
        except:
            pass
        return float('inf')
    
    def save_high_score(self, score):
        """Save high score to file"""
        try:
            with open("highscore.json", 'w') as file:
                json.dump({'high_score': score}, file)
        except:
            pass
    
    def change_difficulty(self):
        """Change game difficulty"""
        self.difficulty = self.difficulty_var.get()
        self.new_game()
    
    def set_difficulty_parameters(self):
        """Set game parameters based on difficulty"""
        difficulties = {
            "Easy": (1, 50, 10, "green"),
            "Medium": (1, 100, 7, "yellow"),
            "Hard": (1, 200, 5, "orange"),
            "Expert": (1, 500, 3, "red")
        }
        
        self.lower_bound, self.upper_bound, self.max_attempts, color = difficulties[self.difficulty]
        self.range_label.config(
            text=f"Guess the number between {self.lower_bound} and {self.upper_bound}",
            fg=color
        )
    
    def new_game(self):
        """Start a new game"""
        self.set_difficulty_parameters()
        self.secret_number = random.randint(self.lower_bound, self.upper_bound)
        self.attempts = 0
        self.game_active = True
        
        # Clear and enable guess entry
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state='normal')
        self.guess_btn.config(state='normal')
        self.guess_entry.focus()
        
        # Clear feedback
        self.feedback_label.config(text="")
        self.hint_label.config(text="")
        
        # Clear previous guesses listbox
        self.guesses_listbox.delete(0, tk.END)
        
        # Update attempts display
        self.update_attempts_display()
        
    def update_attempts_display(self):
        """Update attempts counter"""
        if self.game_active:
            remaining = self.max_attempts - self.attempts
            if remaining >= 0:
                self.attempts_label.config(
                    text=f"Attempts: {self.attempts}/{self.max_attempts} (Remaining: {remaining})"
                )
            else:
                self.attempts_label.config(
                    text=f"Attempts: {self.attempts}/{self.max_attempts} (Game Over!)"
                )
        else:
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
    
    def make_guess(self):
        """Process user's guess"""
        if not self.game_active:
            messagebox.showinfo("Game Over", "Please start a new game!")
            return
        
        # Get guess
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            self.guess_entry.delete(0, tk.END)
            return
        
        # Check range
        if guess < self.lower_bound or guess > self.upper_bound:
            messagebox.showwarning(
                "Out of Range", 
                f"Please enter a number between {self.lower_bound} and {self.upper_bound}!"
            )
            self.guess_entry.delete(0, tk.END)
            return
        
        self.attempts += 1
        
        # Add to previous guesses
        self.guesses_listbox.insert(0, f"Guess #{self.attempts}: {guess}")
        self.guesses_listbox.itemconfig(0, fg=self.get_guess_color(guess))
        
        # Check guess
        if guess == self.secret_number:
            self.game_won()
        elif self.attempts >= self.max_attempts:
            self.game_lost()
        else:
            self.give_feedback(guess)
        
        # Clear entry
        self.guess_entry.delete(0, tk.END)
        self.update_attempts_display()
    
    def get_guess_color(self, guess):
        """Get color for guess based on proximity"""
        difference = abs(guess - self.secret_number)
        if difference <= 5:
            return '#27AE60'  # Green (very close)
        elif difference <= 15:
            return '#F39C12'  # Orange (close)
        elif difference <= 30:
            return '#E67E22'  # Orange-red (far)
        else:
            return '#E74C3C'  # Red (very far)
    
    def give_feedback(self, guess):
        """Give feedback on the guess"""
        difference = guess - self.secret_number
        
        if difference > 0:
            feedback = "📈 Too high! Try a lower number."
        else:
            feedback = "📉 Too low! Try a higher number."
        
        # Add proximity hint
        if abs(difference) <= 5:
            feedback += " 🔥 You're burning up!"
        elif abs(difference) <= 10:
            feedback += " 🌡️ You're getting warm!"
        elif abs(difference) <= 20:
            feedback += " ❄️ You're cold."
        else:
            feedback += " 🧊 You're freezing cold!"
        
        self.feedback_label.config(text=feedback)
    
    def game_won(self):
        """Handle winning the game"""
        self.game_active = False
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        
        # Calculate score
        score = int(1000 / self.attempts * (self.max_attempts / self.attempts))
        
        # Check high score
        if self.attempts < self.high_score:
            self.high_score = self.attempts
            self.high_score_label.config(text=f"🏆 High Score: {self.high_score}")
            self.save_high_score(self.high_score)
            high_score_msg = " 🎉 NEW HIGH SCORE! 🎉"
        else:
            high_score_msg = ""
        
        messagebox.showinfo(
            "🎉 YOU WIN! 🎉",
            f"Congratulations!\n\n"
            f"You guessed the number {self.secret_number} in {self.attempts} attempts!\n"
            f"Score: {score}{high_score_msg}"
        )
        
        self.feedback_label.config(
            text=f"🎊 WINNER! You found the number in {self.attempts} attempts! 🎊",
            fg='#F1C40F'
        )
    
    def game_lost(self):
        """Handle losing the game"""
        self.game_active = False
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        
        messagebox.showinfo(
            "😢 Game Over",
            f"Sorry! You've used all {self.max_attempts} attempts.\n"
            f"The number was: {self.secret_number}\n\n"
            f"Try again with a new game!"
        )
        
        self.feedback_label.config(
            text=f"😢 GAME OVER! The number was {self.secret_number}",
            fg='#E74C3C'
        )
    
    def give_hint(self):
        """Give a hint to the player"""
        if not self.game_active:
            messagebox.showinfo("No Active Game", "Please start a new game first!")
            return
        
        hints = [
            f"The number is {'even' if self.secret_number % 2 == 0 else 'odd'}.",
            f"The number is {'greater than' if self.secret_number > (self.upper_bound + self.lower_bound)/2 else 'less than'} {int((self.upper_bound + self.lower_bound)/2)}.",
            f"The sum of digits is {sum(int(d) for d in str(self.secret_number))}.",
            f"The number {'is' if self.secret_number % 3 == 0 else 'is not'} divisible by 3.",
            f"The number {'is' if self.secret_number % 5 == 0 else 'is not'} divisible by 5.",
            f"The number is between {self.secret_number - 10} and {self.secret_number + 10}."
        ]
        
        hint = random.choice(hints)
        self.hint_label.config(text=f"💡 Hint: {hint}")
    
    def show_answer(self):
        """Show the correct answer"""
        if messagebox.askyesno("Show Answer", 
                               f"Are you sure you want to see the answer?\n"
                               f"The number is {self.secret_number}"):
            self.game_active = False
            self.guess_entry.config(state='disabled')
            self.guess_btn.config(state='disabled')
            
            messagebox.showinfo(
                "Answer Revealed",
                f"The secret number was: {self.secret_number}\n\n"
                f"Start a new game to play again!"
            )
            
            self.feedback_label.config(
                text=f"The number was {self.secret_number}. Better luck next time!",
                fg='#E74C3C'
            )

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Number Guessing Game")
        self.splash.geometry("500x400")
        self.splash.configure(bg='#2C3E50')
        self.splash.overrideredirect(True)
        
        # Center the splash screen
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.splash.winfo_screenheight() // 2) - (400 // 2)
        self.splash.geometry(f'+{x}+{y}')
        
        # Create splash content
        title_label = tk.Label(
            self.splash,
            text="🎮 NUMBER\nGUESSING GAME 🎮",
            font=('Arial', 32, 'bold'),
            bg='#2C3E50',
            fg='#F1C40F'
        )
        title_label.pack(expand=True)
        
        loading_label = tk.Label(
            self.splash,
            text="Loading...",
            font=('Arial', 14),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        loading_label.pack(pady=20)
        
        # Progress bar
        progress = ttk.Progressbar(
            self.splash,
            mode='indeterminate',
            length=300
        )
        progress.pack(pady=20)
        progress.start(10)
        
        # Close splash after 2 seconds
        self.splash.after(2000, self.close_splash)
        self.splash.mainloop()
    
    def close_splash(self):
        self.splash.destroy()

def main():
    # Show splash screen
    splash = SplashScreen()
    
    # Create main window
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()