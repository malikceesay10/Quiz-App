import tkinter as tk
import random

questions = [
    {
        "frage": "Welche Programmiersprache wird häufig für Data Science verwendet?",
        "optionen": ["Java", "Python", "C#", "Ruby"],
        "antwort": "Python"
    },
    {
        "frage": "Was ist GitHub?",
        "optionen": ["Ein Betriebssystem", "Ein Texteditor", "Ein Code-Hosting-Dienst", "Eine Programmiersprache"],
        "antwort": "Ein Code-Hosting-Dienst"
    },
    {
        "frage": "Was bedeutet HTML?",
        "optionen": ["High Tech Markup Language", "Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlinks Text Memory Language"],
        "antwort": "Hyper Text Markup Language"
    },
    {
        "frage": "Welches ist kein SQL Join?",
        "optionen": ["INNER JOIN", "LEFT JOIN", "CENTER JOIN", "FULL JOIN"],
        "antwort": "CENTER JOIN"
    }
]

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Anwendung")
        self.score = 0
        self.qn = 0
        self.correct = 0
        self.time_left = 10
        random.shuffle(questions)
        self.questions = questions
        self.create_start_screen()

    def create_start_screen(self):
        # Create and pack start frame
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack(expand=True, fill='both', pady=50)
        
        # Title
        title = tk.Label(self.start_frame, 
                        text="Wirtschaftsinformatik Quiz", 
                        font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Welcome message
        msg = tk.Label(self.start_frame,
                      text="Testen Sie Ihr Wissen!\n\nBeantworten Sie Multiple-Choice Fragen\ninnerhalb von 10 Sekunden.",
                      font=("Arial", 14),
                      justify="center")
        msg.pack(pady=30)
        
        # Start button
        start_btn = tk.Button(self.start_frame,
                             text="Quiz Starten",
                             command=self.start_quiz,
                             font=("Arial", 14, "bold"),
                             width=15,
                             height=2)
        start_btn.pack(pady=30)

    def start_quiz(self):
        # Hide start screen
        self.start_frame.destroy()
        
        # Create quiz widgets
        self.create_widgets()
        self.display_question()
        self.start_timer()

    def create_widgets(self):
        # Timer label
        self.timer_label = tk.Label(self.master, text="Zeit: 10", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        # Question label
        self.question_label = tk.Label(self.master, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)
        
        # Frame for 2x2 grid
        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack(pady=10)
        
        self.var = tk.IntVar()
        self.options = []
        
        # Create 2x2 grid of options
        for i in range(4):
            row = i // 2
            col = i % 2
            rb = tk.Radiobutton(self.options_frame, text="", variable=self.var, value=i, font=("Arial", 12))
            rb.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            self.options.append(rb)
            
        self.submit_button = tk.Button(self.master, text="Antworten", command=self.check_answer)
        self.submit_button.pack(pady=20)
        
        self.result_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.result_label.pack()

        # Create frame for next button (right-aligned)
        self.next_button_frame = tk.Frame(self.master)
        self.next_button_frame.pack(fill='x', padx=20)
        
        # Next question button (initially hidden)
        self.next_button = tk.Button(self.next_button_frame, 
                                   text="Nächste Frage", 
                                   command=self.next_question,
                                   font=("Arial", 12))
        self.next_button.pack(side='right', pady=10)
        self.next_button.pack_forget()  # Hide initially

    def start_timer(self):
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Zeit: {self.time_left}")
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.check_answer(timeout=True)

    def display_question(self):
        self.time_left = 10
        q = self.questions[self.qn]
        self.question_label.config(text=q["frage"])
        self.var.set(-1)
        for idx, option in enumerate(q["optionen"]):
            self.options[idx].config(text=option, fg="black", selectcolor="white")
        self.result_label.config(text="")

    def check_answer(self, timeout=False):
        if timeout:
            self.result_label.config(text="Zeit abgelaufen!", fg="red")
            self.highlight_correct_answer()
        else:
            selected = self.var.get()
            if selected == -1:
                self.result_label.config(text="Bitte wählen Sie eine Antwort aus.")
                return
            
            q = self.questions[self.qn]
            if q["optionen"][selected] == q["antwort"]:
                self.correct += 1
                self.result_label.config(text="Richtig!", fg="green")
                self.options[selected].config(fg="green")
            else:
                self.result_label.config(text=f"Falsch!", fg="red")
                self.options[selected].config(fg="red")
                self.highlight_correct_answer()

        # Show next button instead of auto-advancing
        if self.qn < len(self.questions) - 1:  # Don't show on last question
            self.next_button.pack(side='right', pady=10)
        self.submit_button.config(state='disabled')  # Disable answer button

    def highlight_correct_answer(self):
        q = self.questions[self.qn]
        correct_idx = q["optionen"].index(q["antwort"])
        self.options[correct_idx].config(fg="green")

    def next_question(self):
        self.qn += 1
        if self.qn < len(self.questions):
            self.next_button.pack_forget()  # Hide next button
            self.submit_button.config(state='normal')  # Re-enable answer button
            self.display_question()
        else:
            self.show_score()

    def show_score(self):
        self.timer_label.pack_forget()
        self.question_label.config(text=f"Quiz beendet! Sie haben {self.correct} von {len(self.questions)} Fragen richtig beantwortet.")
        self.options_frame.pack_forget()
        self.submit_button.pack_forget()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
