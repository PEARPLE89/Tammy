import tkinter as tk
from tkinter import ttk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import pytz
from datetime import datetime
import time

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.happiness = 100
        self.health = 100
        self.time_to_deteriorate = 600  # Temps (en secondes) avant que les jauges ne commencent à baisser
        self.update_time = time.time()  # Heure de la dernière mise à jour du Tamagotchi
        self.hatching_time = 60  # Temps (en secondes) avant que l'œuf n'écloche
        self.hatching_done = False  # Indicateur pour vérifier si l'œuf a déjà éclos

        #Initaliser l'heure d'éclosion de l'oeuf
        self.hatch_time = self.update_time + self.hatching_time

    def feed(self):
        self.hunger -= 20
        self.happiness += 10
        self.health += 10
        self.update_status()
        self.show_message(f"{self.name} a été nourri.")

    def play(self):
        self.hunger += 10
        self.happiness += 30
        self.update_status()
        self.show_message(f"Vous avez joué avec {self.name}.")

    def heal(self):
        self.health = 100
        self.update_status()
        self.show_message(f"{self.name} a été soigné.")

    def update(self):
        current_time = time.time()
        time_passed = current_time - self.update_time

        if not self.hatching_done and time_passed >= self.hatching_time:
            # L'œuf a éclos, changer l'image et afficher le message
            self.hatching_done = True
            self.update_pet_image("tamagotchi.jpg")
            self.show_message("Votre Troll est né: il s'appelle Bobeuse")
        
        if time_passed >= self.time_to_deteriorate:
            # Le temps nécessaire pour que les jauges commencent à baisser est écoulé
            self.happiness -= 20
            self.health -= 20
            self.update_time = current_time  # Réinitialiser l'heure de la dernière mise à jour

        # Mettre à jour les autres aspects du Tamagotchi
        self.hunger += random.randint(0, 20)
        self.happiness -= random.randint(0, 10)
        self.health -= random.randint(0, 10)
        self.update_status()

        root.after(10000, self.update)  # Planifier la prochaine mise à jour après 1 seconde

    def update_status(self):
        if self.hunger >= 80:
            self.show_message(f"{self.name} a faim ! Nourrissez-le !")
        if self.happiness <= 20:
            self.show_message(f"{self.name} est malheureux ! Jouez avec lui !")
        if self.health <= 20:
            self.show_message(f"{self.name} est malade ! Soignez-le !")

        # Mettre à jour les jauges
        hunger_bar["value"] = self.hunger 
        happiness_bar["value"] = self.happiness 
        health_bar["value"] = self.health 

    def show_message(self, message):
        custom_style = ttk.Style()
        custom_style.configure("Custom.TLabel", font=("Marianne", 12), foreground="#1f1f1f", background="#f1e8d8")
        custom_style.map("Custom.TLabel", foreground=[("active", "#FFA41B")])

        message_box = ttk.Label(root, text=message, style="Custom.TLabel")
        message_box.pack(pady=10)

        # Centrer la boîte de dialogue au milieu de l'écran
        root.update_idletasks()
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - root_width) // 2
        y = (screen_height - root_height) // 2
        root.geometry(f"+{x}+{y}")

        # Attente pendant une courte période pour afficher le message, puis suppression automatique
        root.after(2000, message_box.destroy)

    def update_pet_image(self, image_path):
        pet_img = Image.open(image_path)
        pet_img = pet_img.resize((150, 150), Image.LANCZOS)
        pet_img = ImageTk.PhotoImage(pet_img)
        pet_img_label.config(image=pet_img)
        pet_img_label.image = pet_img

def update_time():
    time_format = "%d/%m/%Y %H:%M:%S"
    tz_paris = pytz.timezone("Europe/Paris")
    current_time = datetime.now(tz_paris).strftime(time_format)
    time_label.config(text=current_time)
    root.after(1000, update_time)

def on_feed_button_click():
    pet.feed()
    update_pet_image()

def on_play_button_click():
    pet.play()
    update_pet_image()

def on_heal_button_click():
    pet.heal()
    update_pet_image()

def on_exit_button_click():
    root.destroy()

def update_pet_image():
    pet.update_pet_image("Oeuf.png")

#def update_pet_image():
    #pet_img = Image.open("Oeuf.png")
    #pet_img = pet_img.resize((150, 150), Image.LANCZOS)
    #pet_img = ImageTk.PhotoImage(pet_img)
    #pet_img_label.config(image=pet_img)
    #pet_img_label.image = pet_img

# Create the Tamagotchi instance
pet = Tamagotchi("Tammy")

# Create the main window
root = tk.Tk()
root.title("Tamagotchi")
root.geometry("400x450")

# Background color
root.configure(bg="#f1e8d8")

# Custom font "Marianne"
custom_font = ("Marianne", 16)

# Welcome label
welcome_label = tk.Label(root, text=f"Bienvenue dans {pet.name} !", font=custom_font, bg="#f1e8d8")
welcome_label.pack(pady=10)

# Date label
date_label = tk.Label(root, font=("Marianne", 12), bg="#f1e8d8", fg="navy")
date_label.pack(anchor="nw", padx=10)

# Time label
time_label = tk.Label(root, font=("Marianne", 12), bg="#f1e8d8", fg="navy")
time_label.pack(anchor="nw", padx=10)

# Hunger progress bar
hunger_label = tk.Label(root, text="Faim:", font=("Marianne", 12), bg="#f1e8d8")
hunger_label.pack(pady=5, anchor="w", padx=10)

hunger_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
hunger_bar.pack(pady=5, padx=10, anchor="w")

# Happiness progress bar
happiness_label = tk.Label(root, text="Bonheur:", font=("Marianne", 12), bg="#f1e8d8")
happiness_label.pack(pady=5, anchor="w", padx=10)

happiness_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
happiness_bar.pack(pady=5, padx=10, anchor="w")

# Health progress bar
health_label = tk.Label(root, text="Santé:", font=("Marianne", 12), bg="#f1e8d8")
health_label.pack(pady=5, anchor="w", padx=10)

health_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
health_bar.pack(pady=5, padx=10, anchor="w")

# Update time
update_time()

# Pet image
pet_img = Image.open("Oeuf.png")
pet_img = pet_img.resize((150, 150), Image.LANCZOS)  
pet_img = ImageTk.PhotoImage(pet_img)
pet_img_label = tk.Label(root, image=pet_img, bg="#f1e8d8")
pet_img_label.pack(pady=10)

# Buttons
feed_button = tk.Button(root, text="Nourrir", font=custom_font, bg="#ffc300", command=on_feed_button_click)
feed_button.pack(pady=5, padx=10, side=tk.LEFT)

play_button = tk.Button(root, text="Jouer", font=custom_font, bg="#ffa41b", command=on_play_button_click)
play_button.pack(pady=5, padx=10, side=tk.LEFT)

heal_button = tk.Button(root, text="Soigner", font=custom_font, bg="#ff5b5b", command=on_heal_button_click)
heal_button.pack(pady=5, padx=10, side=tk.LEFT)

exit_button = tk.Button(root, text="Quitter", font=custom_font, bg="#66c0f4", command=on_exit_button_click)
exit_button.pack(pady=10)

# Update the pet's status and start the time-based updates
update_pet_image()
pet.update()

root.mainloop()
