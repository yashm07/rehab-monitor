from PIL import Image
import tkinter as tk
import customtkinter
from tkinter.filedialog import askopenfilename
import pandas as pd
from live import get_data, save_data
from saved import plot_data

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.title("GaitKeeper")

        # add image widget

        my_image = customtkinter.CTkImage(light_image=Image.open("gitCode/3p04-project/src/company_logo.jpg"),
                                  dark_image=Image.open("gitCode/3p04-project/src/company_logo.jpg"),
                                  size=(200, 100))

        button = customtkinter.CTkButton(master=self, image=my_image, hover=False, fg_color='transparent', text=" ")
        button.place(x=100, y=20)
        
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