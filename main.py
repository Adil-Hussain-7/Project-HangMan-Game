import os
import random
import tkinter as tk
from tkinter import ttk
from itertools import cycle
import nltk #Install The Module using pip installation
nltk.download('words')
from nltk.corpus import words

word_list = words.words()

class TKinter_Hangman():
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.title('Project 1: Hangman Game')
        
        self.root.geometry('400x590')
        
        self.root.resizable(False, False)
        
        self.mainframe = tk.Frame(background='light green')
        self.mainframe.pack (fill="both", expand=True)
        
        self.text = ttk.Label(self.mainframe, text='Welcome to Hangman Game', font=('century gothic bold', 18), background='light green', foreground='black')
        self.text.grid(row=0, column=0, columnspan=2, pady=10, padx=23)
        
        self.word_blank = ttk.Label(self.mainframe, text='', font=('century gothic bold', 16), background='light green', foreground='black')
        self.word_blank.grid(row=1, column=0, columnspan=2)
        
        self.attempts_remaining = ttk.Label(self.mainframe, text='', font=('century gothic bold', 16), background='light green', foreground='black')
        self.attempts_remaining.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.input_entry = ttk.Entry(self.mainframe, font=('century gothic bold', 12))
        self.input_entry.grid(row=3, column=0, columnspan=2, pady=0)
        
        self.input_entry.bind("<Return>", self.submit_Guess)
        
        self.submit_Button = ttk.Button(self.mainframe, text='Submit Guess', command=self.submit_Guess)
        self.submit_Button.grid(row=4, column=0, columnspan=2, pady=7)
        
        self.indications = ttk.Label(self.mainframe, text='', font=('century gothic bold', 12), background='light green', foreground='black', anchor="center", justify="center")
        self.indications.grid(row=5, column=0, columnspan=2)
        
        self.canvas = tk.Canvas(self.mainframe, width=300, height=300, background='light green')
        self.canvas.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.First_Image = [tk.PhotoImage(file=os.path.join("C:/path/to/your/First_Image/Directory", "1.png"))]
        
        self.Win_Images = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Winning/Images/Directory", f"win_{i}.png")) for i in range(2, 12)]
        
        self.game_over = False
        
        self.image_cycle = cycle(self.Win_Images)
        
        self.Lose_1 = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Act_1/Directory", f"{i}.png")) for i in range(1, 4)]
        self.Lose_2 = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Act_2/Directory", f"{i}.png")) for i in range(1, 4)]
        self.Lose_3 = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Act_3/Directory", f"{i}.png")) for i in range(1, 4)]
        self.Lose_4 = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Act_4/Directory", f"{i}.png")) for i in range(1, 4)]
        
        self.Death_Act = [tk.PhotoImage(file=os.path.join("C:/path/to/your/Death_Act/Directory", f"{i}.png")) for i in range(1, 5)]
        
        self.current_Image_id = self.canvas.create_image(150, 150, image=self.First_Image)
        
        self.words = self.list_of_words()
        self.Attempts = 6
        self.guessed_letters = set()

        self.update_display()
        
        self.root.mainloop()

        
    def list_of_words(self):
        return random.choice(word_list)

    def update_display(self):
        display = "".join([letter if letter in self.guessed_letters else "_" for letter in self.words])
        self.word_blank.config(text=f"Word: {display}")

        self.attempts_remaining.config(text=f"Your Attempts Left: {self.Attempts}")

    def submit_Guess(self, event=None):  

        if self.game_over:
            return
        
                    
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            self.indications.config(text="Please Select Valid Single Letter!")
            return
        
        if guess in self.guessed_letters:
            self.indications.config(text="The Letter is Already in your Word!")
            return
        
        self.guessed_letters.add(guess)
        
        if guess in self.words:
            self.indications.config(text=f"Good Guess! The Word {guess} you Entered is Right!")
            
        else:
            self.indications.config(text=f"Wrong Guess! The Word {guess} you Entered is Wrong!")
            self.Attempts -= 1
            self.Lose_def()
        
        self.update_display()
            
        if all(letter in self.guessed_letters for letter in self.words):
            self.indications.config(text=f"Woohoo! You Won the Game, Congrats!,\nAlthough the Word is {self.words}")
            self.endgame()
            self.win_def()
            
            
        elif self.Attempts == 0:
            self.indications.config(text=f"Game Over! You ran out of Attempts,\nAlthough the Word is {self.words}")
            self.endgame()
            self.Final_act()
            
            
        self.root.after(300, lambda:self.submit_Button.config(state='Normal'))
            
    
        
    def Lose_def(self):
    # Pick a random cycle of loss images
        chosen_loss_cycle = random.choice([self.Lose_1, self.Lose_2, self.Lose_3, self.Lose_4])
    
    # Iterate through the chosen cycle and display the images
        for img in chosen_loss_cycle:
            self.canvas.itemconfig(self.current_Image_id, image=img)
            self.root.update()
            self.root.after(500)  # 500 milliseconds delay between images

    def Final_act(self):  
        
        self.Current_Image = 0

        self.all_images = len(self.Death_Act)
        
        self.Final_Animation()
        
        
    def Final_Animation(self):
        if self.Current_Image < self.all_images:
            next_Image = self.Death_Act[self.Current_Image]
            
            self.canvas.itemconfig(self.current_Image_id, image=next_Image)
            self.root.update()
            
            self.Current_Image += 1
            
            self.root.after(30, self.Final_Animation)


    def win_def(self):
        
        for i in range(2, 12):
            self.canvas.itemconfig(self.current_Image_id, image=self.Win_Images[i-2])
            self.root.update()
            self.root.after(100)  # 100 milliseconds delay for 10 fps
            
        self.image_cycle = cycle(self.Win_Images[2:])
        
        self.Infi_Loop = True
        
        self.Infinite_Loop()

    
    def Infinite_Loop(self):
        if self.Infi_Loop:
            next_image = next(self.image_cycle)
            self.canvas.itemconfig(self.current_Image_id, image=next_image)  
            self.root.update()
            self.root.after(100, self.Infinite_Loop)

        

    def endgame(self):
        self.input_entry.config(state='Disable')
        self.submit_Button.config(state='Disable')
        
        self.game_over = True
    
    
        restart_Button = ttk.Button(self.mainframe, text='Restart and Play Again', command=self.Restart_Game)
        restart_Button.grid(row=6, column=0, columnspan=2)
        
    def Restart_Game(self):
        
        self.words = self.list_of_words()
        self.Attempts = 6
        self.guessed_letters = set()

        self.game_over = False
        
        self.Infi_Loop = False
        
        self.input_entry.config(state='Normal')
        
        self.submit_Button.config(state='Normal')
        
        self.indications.config(text="")
        
        self.canvas.itemconfig(self.current_Image_id, image=self.First_Image)
        
        self.Infi_Loop = False

        self.update_display()


if __name__ == '__main__':
    TKinter_Hangman()