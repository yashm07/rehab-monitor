import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x350")

textbox = customtkinter.CTkTextbox(app, width=250, corner_radius=3, fg_color="transparent", font=("Roboto Condensed", 25, 'bold'))
textbox.grid(row=0, column=0)

textbox.insert("0.0", "GaitKeeper")  # insert at line 0 character 0
textbox.place(x=130, y=25)

textbox.configure(state="disabled")  # configure textbox to be read-only



def button1_function():
    print("button1 pressed")

# Use CTkButton instead of tkinter Button
button1 = customtkinter.CTkButton(master=app, width=190, height=50, corner_radius=20, border_width=3, fg_color = 'transparent', border_color='#0096FF', text_color="#71797E", text="MEASURE", command=button1_function)
button1.place(x=105, y=150)

def button2_function():
    print("button2 pressed")

# Use CTkButton instead of tkinter Button
button2 = customtkinter.CTkButton(master=app, width=240, height=30, corner_radius=20, border_width=3, fg_color = 'transparent', border_color='#0096FF', text_color="#71797E", text="Upload CVS", command=button1_function)
button2.place(x=80, y=270)

app.mainloop()