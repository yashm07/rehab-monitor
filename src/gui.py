import tkinter as tk
import customtkinter
from tkinter.filedialog import askopenfilename
import pandas as pd
from src.live import get_data, save_data
from src.saved import plot_data

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.title("GaitKeeper")

        # add textbox widget
        textbox = customtkinter.CTkTextbox(
        self, width=250, corner_radius=3, fg_color="transparent", font=("Roboto Condensed", 25, 'bold'), text_color='#141414')
        textbox.grid(row=0, column=0)

        textbox.insert("0.0", "GaitKeeper")  # insert at line 0 character 0
        textbox.place(x=130, y=25)

        textbox.configure(state="disabled")  # configure textbox to be read-only
        
        # add button widget
        button1 = customtkinter.CTkButton(master=self, width=190, height=50, corner_radius=20, border_width=3, hover=False,
                                          fg_color='transparent', border_color='#0096FF', text_color="#141414", text="MEASURE", command=self.__button1_callback)
        button1.place(x=105, y=150)
        
        # add button widget
        button1 = customtkinter.CTkButton(master=self, width=190, height=50, corner_radius=20, border_width=3, hover=False,
                                          fg_color='transparent', border_color='#0096FF', text_color="#141414", text="UPLOAD CSV", command=self.__button2_callback)
        button1.place(x=105, y=225)


    def __button1_callback(self):
        # live plot knee flexion angle and heel strike
        data = get_data()

        # save data to csv file once done measuring
        save_data(data)
    
    def __button2_callback(self):
        file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
        df = pd.read_csv(file_path)
        
        # plots saved data
        plot_data(df)
    
if __name__ == "__main__":
    # run app
    app = App()
    app.mainloop()