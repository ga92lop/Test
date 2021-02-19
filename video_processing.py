import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk, Image
import datetime
import re
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.defaultPath = os.getcwd()
        if not os.path.exists(self.defaultPath):
            os.makedirs(self.defaultPath)
        self.bgcolor = "white"
        self.master = master
        self.canvas = tk.Canvas(master, width=880, height=500, bd=0, highlightthickness=0)
        self.img = Image.open('3.gif')
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(440, 250, image=self.photo)
        self.canvas.grid(row=0, column=0)
        self.create_widgets()

    def create_widgets(self):
        # Select folder and file
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
        self.canvas.create_window(800, 50, width=100, height=30,
                                  window=folderselection)

        label2 = tk.Label(self.master)
        label2["text"] = "Select a file:"
        label2.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(100, 100, width=200, height=30,
                                  window=label2)

        self.fileselection = tk.ttk.Combobox(self.master)
        self.fileselection["values"] = self.list_files(self.defaultPath)
        self.fileselection.configure(state="readonly")
        self.canvas.create_window(460, 100, width=480, height=30,
                                  window=self.fileselection)

        # Function Start:
        header = tk.Label(self.master)
        header["text"] = "Functions:"
        header.config(bg="lightgreen", font=("Courier", 12))
        self.canvas.create_window(440, 150, width=880, height=30,
                                  window=header)

        # Compression
        b_compression = tk.Button(self.master, text="Compress MP4")
        b_compression["command"] = lambda: self.compress(self.fileselection.get())
        b_compression.config(bg=self.bgcolor)
        self.canvas.create_window(750, 200, width=100, height=40,
                                  window=b_compression)




        # Remove Audio
        test_date = tk.Label(self.master)
        test_date["text"] = "Test Date:"
        self.canvas.create_window(60, 225, width=100, height=40,
                                  window=test_date)

        self.date_input = tk.Entry("")
        self.date_input.config(font=16)
        self.canvas.create_window(200, 225, width=160, height=40,
                                  window=self.date_input)


        activity = tk.Label(self.master)
        activity["text"] = "Activity:"
        self.canvas.create_window(400, 225, width=100, height=40,
                                  window=activity)

        self.activity_input = tk.Entry("")
        self.activity_input.config(font=16)
        self.canvas.create_window(540, 225, width=150, height=40,
                                  window=self.activity_input)


        b_removeAudio = tk.Button(self.master, text="Remove Audio")
        b_removeAudio["command"] = lambda: self.removeAudio(self.fileselection.get())
        b_removeAudio.config(bg=self.bgcolor)
        self.canvas.create_window(750, 250, width=100, height=40,
                                  window=b_removeAudio)

        # get slice
        starttime = tk.Label(self.master)
        starttime["text"] = "Start Time:"
        self.canvas.create_window(60, 330, width=100, height=40,
                                  window=starttime)

        self.starttimeinput = tk.Entry("")
        self.starttimeinput.config(font=16)
        self.canvas.create_window(200, 330, width=160, height=40,
                                  window=self.starttimeinput)

        endtime = tk.Label(self.master)
        endtime["text"] = "End Time:"
        self.canvas.create_window(60, 390, width=100, height=40,
                                  window=endtime)

        self.endtimeinput = tk.Entry("")
        self.endtimeinput.config(font=16)
        self.canvas.create_window(200, 390, width=160, height=40,
                                  window=self.endtimeinput)

        slicename = tk.Label(self.master)
        slicename["text"] = "Slice Name:"
        self.canvas.create_window(400, 360, width=100, height=40,
                                  window=slicename)

        self.slicenameinput = tk.Entry("")
        self.slicenameinput.config(font=16)
        self.canvas.create_window(540, 360, width=150, height=40,
                                  window=self.slicenameinput)

        b_slice = tk.Button(self.master, text="Get Time Slice")
        b_slice["command"] = lambda: self.gettimeslice(self.starttimeinput.get(), self.endtimeinput.get(), self.fileselection.get(), self.slicenameinput.get(), self.label1["text"])
        b_slice.config(bg=self.bgcolor)
        self.canvas.create_window(750, 360, width=100, height=40,
                                  window=b_slice)

        # Button to quit
        quit = tk.Button(self.master, text="QUIT", fg="red", command=self.master.destroy)
        quit.config(bg=self.bgcolor)
        self.canvas.create_window(830, 450, width=100, height=40,
                                  window=quit)

    """"
    Back end functions start, Including:
    folder selection
    list files and section
    resampling
    reformat
    """

    def folderselection(self):
        currentfolder = self.label1["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.label1["text"] = selectedfolder
        self.fileselection['values'] = self.list_files(selectedfolder)
        self.fileselection.current(0)

    def list_files(self, directory):
        videofiles = []
        for f in os.listdir(directory):
            if f.endswith('.mp4'):
                old = directory + "/" + f
                print(old)
                new = old[:len(old)-4] + ".MP4"
                print(new)
                os.rename(old, new)
            if f.endswith('.AVI'):
                old = directory + "/" + f
                new = old[:len(old)-4] + ".avi"
        for f in os.listdir(directory):
            if f.endswith(".MP4") or f.endswith(".avi"):
                videofiles.append(f)
        if videofiles == []:
            self.label1["fg"] = "red"
        else:
            self.label1["fg"] = "green"
        videofiles.insert(0, "All")
        return videofiles

    def check(self, filename, path):
        if re.match("^20[0-9]{2}[0-1][0-9][0-3][0-9]$", self.date_input.get()) is None:
            messagebox.showerror("Test date", "Input Year(xxxx)Month(xx)Day(xx), e.g. 20201021")
            return None
        if len(self.activity_input.get().strip()) == 0:
            messagebox.showerror("Activity", "Input Test Activity, e.g. FLT10")
            return None
        if filename == "":
            message = "Select a file or all files to be processed"
            messagebox.showerror(title="Select a file", message=message)
            return None
        if " " in path:
            message = "There should not be a blank in the file path"
            messagebox.showerror(title="Select a file", message=message)
            return None
        if filename == "All":
            if len(self.fileselection["values"]) == 1:
                message = "No file to be processed"
                messagebox.showerror(title="Select a file", message=message)
                return None
        return True

    def compress(self, filename):
        if not self.check(filename, self.label1["text"]) is True:
            return None
        ffmpegoperation = " -crf 23 "
        mode = "compress"
        self.operation(filename, ffmpegoperation, mode)

    def removeAudio(self, filename):
        if not self.check(filename, self.label1["text"]) is True:
            return None
        ffmpegoperation = " -map 0:0 -vcodec copy "
        mode = "Remove Audio"
        self.operation(filename, ffmpegoperation, mode)

    def operation(self, filename, ffmpegoperation, mode):
        if filename == "All":
            outputprefix = self.date_input.get() + "_" + self.activity_input.get() + "_"
            for f in os.listdir(self.label1["text"]):
                if outputprefix in f:
                    messagebox.showerror("File exists", outputprefix + "xxx already exist")
                    return None
            command = ""
            filenum = 1
            files =list()
            for f in self.fileselection["values"]:
                if f != "All":
                    files.append(f)
                    if mode == "compress":
                        if (".mp4" not in f) and (".MP4" not in f):
                            files.remove(f)
            print(files)
            for f in files:
                if len(str(filenum)) == 1:
                    outputsuffix = "P" + "0" + str(filenum) + f[len(f) - 4:]
                else:
                    outputsuffix = "P" + str(filenum) + f[len(f) - 4:]
                if len(command) == 0:
                    command = self.cmdgenerate(f, outputprefix + outputsuffix, ffmpegoperation)
                else:
                    command = command + " & " + self.cmdgenerate(f, outputprefix + outputsuffix, ffmpegoperation)
                filenum += 1
            totalcommand = "start /wait cmd /c " + "\"" + command + "\""
            os.system(totalcommand)
        if filename != "All" and filename != "":
            outputprefix = self.date_input.get() + "_" + self.activity_input.get() + "_"
            f = self.fileselection.get()
            if mode == "compress":
                if (".mp4" not in f )and(".MP4" not in f):
                    message = "Compression is only for Gopro MP4 files"
                    messagebox.showerror(title="Select MP4", message=message)
                    return None
            outputsuffix = "P" + "01" + f[len(f) - 4:]
            command = self.cmdgenerate(filename, outputprefix + outputsuffix, ffmpegoperation)
            totalcommand = "start /wait cmd /c " + "\"" + command + "\""
            os.system(totalcommand)

    def cmdgenerate(self, inputfilename, outputfilename, operation):
        input = self.label1["text"].replace("/", "\\") + "\\" + inputfilename
        output = self.label1["text"].replace("/", "\\") + "\\" + outputfilename
        while os.path.exists(output):
            filenum = output[len(output)-6:len(output)-4]
            if filenum[0] == "0" and filenum[1] != "9":
                numoffile = int(filenum) + 1
                print(str(numoffile))
                output = self.label1["text"].replace("/", "\\") + "\\" + outputfilename[:len(outputfilename)-5] + str(numoffile) + outputfilename[len(outputfilename)-4:]
                print(output)
            else:
                numoffile = int(filenum) + 1
                output = self.label1["text"].replace("/", "\\") + "\\" + outputfilename[:len(outputfilename)-6] + str(numoffile) + outputfilename[len(outputfilename)-4:]
                print(output)
        currentfolder = os.getcwd()
        cmdpath = currentfolder + "\\ffmpeg\\bin\\"
        cmdcommand = cmdpath + "ffmpeg -i " + input + operation + output
        return cmdcommand

    def gettimeslice(self, time1, time2, inname, outname, path):
        if inname == "" or inname == "All":
            message = "Select a file to be processed"
            messagebox.showerror(title="Select a file", message=message)
            return None
        if " " in path:
            message = "There should not be a blank in the file path"
            messagebox.showerror(title="Wrong Path", message=message)
            return None
        if re.match("^[0-5][0-9]:[0-5][0-9]:[0-5][0-9]$", time1) is None:
            messagebox.showerror("Start Time", "Input hh:mm:ss, e.g.00:08:10")
            return None
        if re.match("^[0-5][0-9]:[0-5][0-9]:[0-5][0-9]$", time2) is None:
            messagebox.showerror("End Time", "Input hh:mm:ss, e.g.00:16:18")
            return None
        temp = time1.split(":")
        t1 = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
        temp = time2.split(":")
        t2 = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
        diff = t2 - t1
        if diff <= 0:
            messagebox.showerror("Time Input", "end time should be greater than start time")
            return None
        if outname =="":
            message = "Input a name for slice"
            messagebox.showerror(title="Input Necessary", message=message)
            return None
        output = self.label1["text"].replace("/", "\\") + "\\" + outname + inname[len(inname)-4:]
        if os.path.exists(output):
            overwriteflag = False
            overwriteflag = overwriteflag = tk.messagebox.askokcancel("resampled file exists", "Resampled file exists, overwrite?")
            if overwriteflag == False:
                return None
        input = self.label1["text"].replace("/", "\\") + "\\" + inname
        currentfolder = os.getcwd()
        cmdpath = currentfolder + "\\ffmpeg\\bin\\"
        cmdcommand = cmdpath + "ffmpeg -ss " + time1 + " -t " + str(diff) + " -accurate_seek " + "-i " + input + " -codec copy  -avoid_negative_ts 1 " + output
        totalcommand = "start /wait cmd /c " + "\"" + cmdcommand + "\""
        os.system(totalcommand)






root = tk.Tk()
root.title("Welcome to Video Data Processing Tool")
root.geometry('880x500+500+200')
root.resizable(0, 0)
root.configure(bg='white')

app = Application(master=root)
app.mainloop()