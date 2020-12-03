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
        self.canvas.create_window(430, 50, width=570, height=30,
                                  window=self.label1)

        folderselection = tk.Button(self.master)
        folderselection["text"] = "select a folder"
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
        self.canvas.create_window(640, 160, width=150, height=40,
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
        label31["text"] = "(3 digits)"
        label31.config(bg=self.bgcolor, fg="red", font=("Courier", 12))
        self.canvas.create_window(640, 230, width=150, height=40,
                                  window=label31)

        # forth row: Power Cycle input
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
        label41["text"] = "(3 digits)"
        label41.config(bg=self.bgcolor, fg="red", font=("Courier", 12))
        self.canvas.create_window(640, 300, width=150, height=40,
                                  window=label41)

        # fifth row: button to rename, merge data and quit
        rename_ASCB_D = tk.Button(self.master, text="ASCB-D_Rename")
        rename_ASCB_D["command"] = lambda: self.rename_ASCB()
        rename_ASCB_D.config(bg=self.bgcolor)
        self.canvas.create_window(80, 400, width=100, height=60,
                                  window=rename_ASCB_D)

        label5 = tk.Label(self.master)
        label5["text"] = "Only Recording \n Num necessary"
        label5.config(bg=self.bgcolor)
        self.canvas.create_window(180, 400, width=100, height=60,
                                  window=label5)

        rename = tk.Button(self.master, text="PCAP_Rename")
        rename["command"] = lambda: self.rename()
        rename.config(bg=self.bgcolor)
        self.canvas.create_window(320, 400, width=100, height=60,
                                  window=rename)

        merge = tk.Button(self.master, text="Merge tdms")
        merge["command"] = lambda: self.mergingtdms()
        merge.config(bg=self.bgcolor)
        self.canvas.create_window(560, 400, width=100, height=60,
                                  window=merge)

        quit = tk.Button(self.master, text="QUIT", fg="red", command=self.master.destroy)
        quit.config(bg=self.bgcolor)
        self.canvas.create_window(800, 400, width=100, height=60,
                                  window=quit)

        # sixth row: button to rename, merge data and quit
        re_do_ASCB = tk.Button(self.master, text="Redo")
        re_do_ASCB["command"] = lambda: self.redo_rename_ASCB()
        re_do_ASCB.config(bg=self.bgcolor)
        self.canvas.create_window(80, 470, width=100, height=40,
                                  window=re_do_ASCB)

        re_do_pcap = tk.Button(self.master, text="Redo")
        re_do_pcap["command"] = lambda: self.redo_rename()
        re_do_pcap.config(bg=self.bgcolor)
        self.canvas.create_window(320, 470, width=100, height=40,
                                  window=re_do_pcap)

    def folderselection(self):
        currentfolder = self.label1["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.label1["text"] = selectedfolder

    def rename_ASCB(self):
        if not self.inputcheck("ASCB_D") is True:
            return None
        currentfolder = self.label1["text"] + "/"
        recordingnum = self.recordingnum.get()
        renamedfiles = 0
        for f in os.listdir(currentfolder):
            if not re.match("ASCB_RAW", f) is None:
                old_name = currentfolder + f
                new_name = currentfolder + recordingnum + "_" + f
                try:
                    os.rename(old_name, new_name)
                    renamedfiles += 1
                except PermissionError:
                    messagebox.showerror("Cannot rename", "Cannot rename, make sure files are accessible and not used")
        if renamedfiles == 0:
            return messagebox.showerror("No File", "No ASCB-D data file with name ASCB_RAW_xx.xx to be renamed")
        else:
            return messagebox.showinfo("Finish Renaming",
                                       "Rename finished, please work on Pcap files")



    def rename(self):
        if not self.inputcheck("Pcap") is True:
            return None
        currentfolder = self.label1["text"] + "/"
        recordingnum = self.recordingnum.get()
        descriptionnum = self.descriptionnum.get()
        prefix = currentfolder + "t1310" + descriptionnum + "_" + recordingnum + "_"
        renamedfiles = 0
        for f in os.listdir(currentfolder):
            if not re.match("^[0-9]{4}_[0-9]{4}.cap$", f) is None:
                old_name = currentfolder + f
                new_name = prefix + f
                try:
                    os.rename(old_name, new_name)
                    renamedfiles += 1
                except PermissionError:
                    messagebox.showerror("Cannot rename", "Cannot rename, make sure files are accessible and not used")
        if renamedfiles == 0:
            return messagebox.showerror("No File", "No Pcap file with name xxxx_xxxx to be renamed")
        else:
            return messagebox.showinfo("Finish Renaming",
                                       "Rename finished, use PCAP2TDMSv1.2.exe to convert pcap to tdms,"
                                       "and name tdms following time sequence then come back to merging")

    def mergingtdms(self):
        if not self.inputcheck("mergeTDMS") is True:
            return None
        currentfolder = self.label1["text"] + "/"
        for f in os.listdir(currentfolder):
            if not re.match("t1310[0-9]{3}_[0-9]{3}_0[0-9]{3}_merged", f) is None:
                messagebox.showerror("Power Cycle Conflict", "Merged tdms data for one power cycle exist")
                return None
        tdmsfile = 0
        currentfile=""
        for f in os.listdir(currentfolder):
            if f.endswith(".tdms"):
                tdmsfile += 1
                currentfile = f
        if tdmsfile == 0:
            messagebox.showerror("No file", "No tdms file to be merged")
            return None
        descriptionnum = self.descriptionnum.get()
        recordingnum = self.recordingnum.get()
        powercycle = self.powercyclenum.get()
        if tdmsfile == 1:
            os.rename(currentfolder + currentfile, currentfolder + "t1310"+descriptionnum + "_" + recordingnum + "_0" +
                      powercycle + "_merged.tdms")
            return messagebox.showinfo('Rename', "Rename .tdms file finished, move the merged"
                                                 "tdms data and renamed .cap file to hard drive. If there are "
                                                 "more power cycles, clear up the folder, and start from renaming "
                                                 ".cap file from other cycle ")
        cmdpath = currentfolder.replace("/", "\\")
        cmdcommand = "\"" + "copy/b " + cmdpath + "*.tdms " + cmdpath + "t1310" + descriptionnum + "_" + \
                     recordingnum + "_0" + powercycle + "_merged.tdms" + "\""
        totalcommand = "start /wait cmd /c " + cmdcommand
        print('Merging start')
        os.system(totalcommand)
        print('Merging finished')
        return messagebox.showinfo("Finish Merging", "tdms merging for one power cycle finished, please move the merged"
                                                     "tdms data and renamed .cap file to hard drive. If there are "
                                                     "more power cycles, clear up the folder, and start from renaming "
                                                     ".cap file from other cycle ")

    def inputcheck(self, mode):
        if re.match("^[0-9]{3}$", self.recordingnum.get()) is None:
            messagebox.showerror("Recording Number", "Input three digits of Recording Number")
            return None
        if re.match("^[0-9]{3}$", self.descriptionnum.get()) is None and mode != "ASCB_D":
            messagebox.showerror("Description Number", "Input three digits of Description Number")
            return None
        if re.match("^[0-9]{3}$", self.powercyclenum.get()) is None and mode == "mergeTDMS":
            messagebox.showerror("Power Cycle Num", "Input three digits of Power cycle Number")
            return None
        return True

    def redo_rename_ASCB(self):
        currentfolder = self.label1["text"] + "/"
        renamedfile = 0
        for f in os.listdir(currentfolder):
            if not re.match("[0-9]{3}_ASCB_RAW", f) is None:
                renamedfile += 1
        if renamedfile == 0:
            messagebox.showerror("No renamed PCAP file", "There is no renamed file in current folder")
            return None
        else:
            redo_flag = False
            redo_flag = messagebox.askokcancel("redo_rename", "Do you want to redo the rename for ASCB_D, i.e. delete "
                                                              "3 digs of recording num at the start of these files")
            if redo_flag is False:
                return None

        for f in os.listdir(currentfolder):
            if not re.match("[0-9]{3}_ASCB_RAW", f) is None:
                old_name = currentfolder + f
                new_name = currentfolder + f[4:]
                os.rename(old_name, new_name)
        return messagebox.showinfo("", "redo finished")

    def redo_rename(self):
        currentfolder = self.label1["text"] + "/"
        renamedfile = 0
        for f in os.listdir(currentfolder):
            if not re.match("t1310[0-9]{3}_[0-9]{3}_[0-9]{4}_[0-9]{4}.cap", f) is None:
                renamedfile += 1
        if renamedfile == 0:
            messagebox.showerror("No renamed PCAP file", "There is no renamed file in current folder")
            return None
        else:
            redo_flag = False
            redo_flag = messagebox.askokcancel("redo_rename", "Do you want to redo the rename, i.e. change the name "
                                                              "t1310001_001_0000_0000 back to 0000_0000 for PCAP file")
            if redo_flag is False:
                return None

        for f in os.listdir(currentfolder):
            if not re.match("t1310[0-9]{3}_[0-9]{3}_[0-9]{4}_[0-9]{4}.cap", f) is None:
                old_name = currentfolder + f
                new_name = currentfolder + f[len(f) - 13:]
                os.rename(old_name, new_name)
        return messagebox.showinfo("", "redo finished")


root = tk.Tk()
root.title("Welcome to Pcap rename and tdms merging tool")
root.geometry('880x500+500+200')
root.resizable(0, 0)
root.configure(bg='white')

app = Application(master=root)
app.mainloop()
