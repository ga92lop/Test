import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import os
from PIL import ImageTk, Image
import re


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.defaultPath = "C:/FLIGHTLINE/RECORDINGS"
        if not os.path.exists(self.defaultPath):
            os.makedirs(self.defaultPath)
        self.bgcolor = "white"
        self.master = master
        self.canvas = tk.Canvas(master, width=880, height=500, bd=0, highlightthickness=0)
        self.img = Image.open('1.gif')
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(440, 250, image=self.photo)
        self.canvas.grid(row=0, column=0)
        self.create_widgets()


    def create_widgets(self):
        # first row: button to select folder
        label0 = tk.Label(self.master)
        label0["text"] = "Current folder:"
        label0.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(75, 50, width=150, height=30,
                                  window=label0)

        self.label1 = tk.Label(self.master)
        self.label1["text"] = self.defaultPath
        self.label1.config(bg=self.bgcolor)
        self.canvas.create_window(425, 50, width=550, height=30,
                                  window=self.label1)

        folderselection = tk.Button(self.master)
        folderselection["text"] = "Select a folder"
        folderselection["command"] = lambda: self.folderselection()
        folderselection.config(bg=self.bgcolor)
        self.canvas.create_window(830, 50, width=100, height=60,
                                                 window=folderselection)

        # second row: label for file and rate selection
        label2 = tk.Label(self.master)
        label2["text"] = "Select a file:"
        label2.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(120, 160, width=240, height=30,
                                  window=label2)

        label3 = tk.Label(text="Resampling rate(Hz):")
        label3.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(420, 160, width=200, height=30,
                                  window=label3)

        # third row: list box for files and rates
        self.fileselection = tk.ttk.Combobox(self.master)
        self.fileselection["values"] = self.list_files(self.defaultPath)
        self.fileselection.configure(state="readonly")
        self.canvas.create_window(120, 200, width=240, height=30,
                                  window=self.fileselection)

        rateselection = tk.ttk.Combobox(self.master)
        rateselection["values"] = (1, 2, 4, 8, 10, 16, 20)
        rateselection.configure(state="readonly")
        self.canvas.create_window(420, 200, width=200, height=30,
                                  window=rateselection)

        # forth row: button to quit and resample
        ok = tk.Button(self.master, text="Resampling")
        ok["command"] = lambda: self.resampling(self.fileselection.get(), rateselection.get())
        ok.config(bg=self.bgcolor)
        self.canvas.create_window(650, 180, width=100, height=60,
                                  window=ok)

        quit = tk.Button(self.master, text="QUIT", fg="red", command=self.master.destroy)
        quit.config(bg=self.bgcolor)
        self.canvas.create_window(830, 180, width=100, height=60,
                                  window=quit)

    def resampling(self, filename, rate):
        if filename == "" or rate == "":
            errormessage = "please select one file and one resampling rate, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if "_resampled_" in filename and "80Hz" not in filename:
            errormessage = "Cannot resample file which is not 80Hz"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        else:
            ration = int(80 / int(rate))
            inputfile = self.label1["text"] + "/" + filename
            Outputfile = inputfile[0:len(inputfile) - 4] + "_resampled_" + rate + "Hz.csv"
            overwriteflag = True
            if os.path.exists(Outputfile):
                overwriteflag = tk.messagebox.askokcancel("resampled file exists","Resampled file exists, overwrite?")
            if overwriteflag == False:
                return None
            try:
                with open(inputfile, newline='') as csvfile:
                    print("Open original data file")
                    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    counter = 0
                    with open(Outputfile, 'w', newline='') as csvfile:
                        print("Open resampled data file")
                        filewriter = csv.writer(csvfile, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        print("Writing data...")
                        for row in spamreader:
                            if counter == ration:
                                counter = 0
                            if counter == 0:
                                filewriter.writerow(row)
                            counter += 1
                print("Finished:D")
            except:
                errormessage = "please make sure data file is closed and accessible, thank you:D"
                tk.messagebox.showerror(title=None, message=errormessage)

    def folderselection(self):
        currentfolder = self.label1["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.label1["text"] = selectedfolder
        self.fileselection['values'] = self.list_files(selectedfolder)

    def list_files(self, directory):
        csvfiles = []
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                csvfiles.append(f)
        if csvfiles == []:
            self.label1["fg"] = "red"
        else:
            self.label1["fg"] = "green"
        return csvfiles


root = tk.Tk()
root.title("Welcome to ASCB-D CSV Resampling")
root.geometry('880x500+500+200')
root.resizable(0, 0)
root.configure(bg='white')

app = Application(master=root)
app.mainloop()
