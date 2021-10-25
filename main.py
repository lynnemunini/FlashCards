from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/FlashCards.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # Convert DataFrame to dictionary
    to_learn = data.to_dict(orient="records")

current_card = {}


def on_click():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(lang_text, fill="black", text=current_card["Spanish"].title())
    canvas.itemconfig(title_text, fill="black", text="Spanish")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title_text, fill="white", text="English")
    canvas.itemconfig(lang_text, fill="white", text=current_card["English"].title())
    canvas.itemconfig(card_background, image=card_back)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    new_data = pandas.DataFrame(to_learn)
    # To not include the index
    new_data.to_csv("data/words_to_learn.csv", index=False)
    on_click()


window = Tk()
window.title("Flashy")
window.config(padx=60, pady=60, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, fill="black", font=("Arial", 40, "italic"))
lang_text = canvas.create_text(400, 263, fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, columnspan=2, row=0)
# Right Image
right_image = PhotoImage(file="images/right.png")
right_image_button = Button(image=right_image, bg="white", highlightthickness=0, border=0, command=is_known)
right_image_button.grid(column=1, row=1, padx=0)
# Left Image
wrong_image = PhotoImage(file="images/wrong.png")
wrong_image_button = Button(image=wrong_image, bg="white", highlightthickness=0, border=0, command=on_click)
wrong_image_button.grid(column=0, row=1, padx=0)

on_click()


window.mainloop()


