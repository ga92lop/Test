import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk, Image
import re


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.defaultPath = "C:/POOL/Pcap"
        if not os.path.exists(self.defaultPath):
            os.makedirs(self.defaultPath)
        self.bgcolor = "white"
        self.master = master
        self.canvas = tk.Canvas(master, width=880, height=500, bd=0, highlightthickness=0)
        self.img = Image.open('2.gif')
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
        self.label1.config(bg=self.bgcolor, font=("", 14))
        self.canvas.create_window(425, 50, width=550, height=30,
                                  window=self.label1)

        folderselection = tk.Button(self.master)
        folderselection["text"] = "Select a folder"
        folderselection["command"] = lambda: self.folderselection()
        folderselection.config(bg=self.bgcolor)
        self.canvas.create_window(800, 50, width=100, height=60,
                                                 window=folderselection)

        # second row: Recording Num input
        label2 = tk.Label(self.master)
        label2["text"] = "Recording Number:"
        label2.config(bg=self.bgcolor, fg='Blue', font=("Courier", 12))
        self.canvas.create_window(120, 160, width=240, height=40,
                                  window=label2)

        self.recordingnum = tk.Entry("")
        self.recordingnum.config(bg=self.bgcolor, font=("", 16))
        self.canvas.create_window(400, 160, width=300, height=40,
                                  window=self.recordingnum)

        label21 = tk.Label(self.master)
        label21["text"] = "(3 digits)"
        label21.config(bg=self.bgcolor, fg="red", font=("Courier", 12))
        self.canvas.create_window(610, 160, width=120, height=40,
                                  window=label21)

        # third row: Description file Num input
        label3 = tk.Label(self.master)
        label3["text"] = "DescriptionFile Number:"
        label3.config(bg=self.bgcolor, fg='Blue', font=("Courier", 12))
        self.canvas.create_window(120, 230, width=240, height=40,
                                  window=label3)

        self.descriptionnum = tk.Entry("")
        self.descriptionnum.config(bg=self.bgcolor, font=("", 16))
        self.canvas.create_window(400, 230, width=300, height=40,
                                  window=self.descriptionnum)

        label31 = tk.Label(self.master)
        label31["text"] = "(2 digits)"
        label31.config(bg=self.bgcolor, fg="red", font=("Courier", 12))
        self.canvas.create_window(610, 230, width=120, height=40,
                                  window=label31)

        #forth row: Power Cycle input
        label4 = tk.Label(self.master)
        label4["text"] = "Power Cycle Number:"
        label4.config(bg=self.bgcolor, fg='Blue', font=("Courier", 12))
        self.canvas.create_window(120, 300, width=240, height=40,
                                  window=label4)

        self.powercyclenum = tk.Entry("")
        self.powercyclenum.config(bg=self.bgcolor, font=("", 16))
        self.canvas.create_window(400, 300, width=300, height=40,
                                  window=self.powercyclenum)
        label41 = tk.Label(self.master)
        label41["text"] = "(2 digits)"
        label41.config(bg=self.bgcolor, fg="red", font=("Courier", 12))
        self.canvas.create_window(610, 300, width=120, height=40,
                                  window=label41)


        # fifth row: button to rename, merge data and quit
        rename = tk.Button(self.master, text="Rename")
        rename["command"] = lambda: self.rename()
        rename.config(bg=self.bgcolor)
        self.canvas.create_window(80, 400, width=100, height=60,
                                  window=rename)

        merge = tk.Button(self.master, text="Merge tdms")
        merge["command"] = lambda: self.mergingtdms()
        merge.config(bg=self.bgcolor)
        self.canvas.create_window(420, 400, width=100, height=60,
                                  window=merge)

        quit = tk.Button(self.master, text="QUIT", fg="red", command=self.master.destroy)
        quit.config(bg=self.bgcolor)
        self.canvas.create_window(800, 400, width=100, height=60,
                                  window=quit)


    def folderselection(self):
        currentfolder = self.label1["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.label1["text"] = selectedfolder

    def rename(self):
        if not self.inputcheck() is True:
            return None
        recordingnum = self.recordingnum.get()
        descriptionnum = self.descriptionnum.get()
        currentfolder = self.label1["text"] + "/"
        prefix = currentfolder+"t13100"+descriptionnum+"_"+recordingnum + "_"
        renameflag = 0
        for f in os.listdir(currentfolder):
            if f.endswith('.cap') and not f.startswith('t131'):
                old_name = currentfolder + f
                new_name = prefix + f
                os.rename(old_name, new_name)
                renameflag += 1
        if renameflag == 0:
            return messagebox.showerror("No File", "No pcap file to be renamed")
        else:
            return messagebox.showinfo("Finish Renaming", "Rename finished, use PCAP2TDMSv1.2.exe to convert pcap to tdms,"
                                                      "and name tdms following time sequence then come back to merging")

    def mergingtdms(self):
        if not self.inputcheck() is True:
            return None
        if re.match("^[0-9]{2}$", self.powercyclenum.get()) is None:
            messagebox.showerror("Power Cycle Num", "Input two digits of Power cycle Number" )
            return None
        currentfolder = self.label1["text"]+"/"
        tdmsflag=0
        for f in os.listdir(currentfolder):
            if not re.match("t13100[0-9]{2}_[0-9]{3}_00[0-9]{2}_merged", f) is None:
                messagebox.showerror("Power Cycle Conflict", "Merged tdms data for one power cycle exist")
                return None
            if f.endswith(".tdms"):
                tdmsflag += 1
        if tdmsflag == 0:
            messagebox.showerror("No tdms file", "No tdms file to be merged")
            return None
        descriptionnum = self.descriptionnum.get()
        recordingnum = self.recordingnum.get()
        powercycle = self.powercyclenum.get()
        cmdpath = currentfolder.replace("/", "\\")
        print("merging start...")
        cmdcommand = "\"" + "copy/b " + cmdpath + "*.tdms " + cmdpath + "t13100"+descriptionnum+"_"+recordingnum +\
                     "_00" + powercycle + "_merged.tdms" + "\""
        totalcommand = "start /wait cmd /c "+cmdcommand
        os.system(totalcommand)
        print("merging finished:D")
        return messagebox.showinfo("Finish Merging", "tdms merging for one power cycle finished, please move the merged"
                                                     " tdms data and renamed pcap file(s) to hard drive. If there is "
                                                     "not only one power cycle, clean up the folder, and start from "
                                                     "renaming for data of other cycle ")



    def inputcheck(self):
        if re.match("^[0-9]{3}$", self.recordingnum.get()) is None:
            messagebox.showerror("Recording Number", "Input three digits of Recording Number" )
            return None
        if re.match("^[0-9]{2}$", self.descriptionnum.get()) is None:
            messagebox.showerror("Description Number", "Input two digits of Description Number")
            return None
        return True





root = tk.Tk()
root.title("Welcome to Pcap rename and tdms merging tool")
root.geometry('880x500+500+200')
root.resizable(0, 0)
root.configure(bg='white')

app = Application(master=root)
app.mainloop()
