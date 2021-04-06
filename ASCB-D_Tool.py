import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import os
import xlsxwriter
from PIL import ImageTk, Image
import datetime
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
        # Select folder and file
        inputfolder_label = tk.Label(self.master)
        inputfolder_label["text"] = "Input folder:"
        inputfolder_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(75, 25, width=150, height=30,
                                  window=inputfolder_label)

        self.inputfolder = tk.Label(self.master)
        self.inputfolder["text"] = self.defaultPath
        self.inputfolder.config(bg=self.bgcolor)
        self.canvas.create_window(425, 25, width=550, height=30,
                                  window=self.inputfolder)

        folderselection = tk.Button(self.master)
        folderselection["text"] = "Select a folder"
        folderselection["command"] = lambda: self.folderselection()
        folderselection.config(bg=self.bgcolor)
        self.canvas.create_window(800, 25, width=100, height=30,
                                  window=folderselection)

        outputfolder_label = tk.Label(self.master)
        outputfolder_label["text"] = "Output folder:"
        outputfolder_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(75, 70, width=150, height=30,
                                  window=outputfolder_label)

        self.outputfolder = tk.Label(self.master)
        self.outputfolder["text"] = "Same with input folder by default"
        self.outputfolder.config(bg=self.bgcolor)
        self.canvas.create_window(425, 70, width=550, height=30,
                                  window=self.outputfolder)

        outfolderselection = tk.Button(self.master)
        outfolderselection["text"] = "Select a folder"
        outfolderselection["command"] = lambda: self.outputfolderselection()
        outfolderselection.config(bg=self.bgcolor)
        self.canvas.create_window(800, 70, width=100, height=30,
                                  window=outfolderselection)

        filesel_label = tk.Label(self.master)
        filesel_label["text"] = "Select a file:"
        filesel_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(100, 110, width=200, height=30,
                                  window=filesel_label)

        self.fileselection = tk.ttk.Combobox(self.master)
        self.fileselection["values"] = self.list_files(self.defaultPath)
        self.fileselection.configure(state="readonly")
        self.canvas.create_window(460, 110, width=480, height=30,
                                  window=self.fileselection)

        # Function Start:
        header = tk.Label(self.master)
        header["text"] = "Functions:"
        header.config(bg="lightgreen", font=("Courier", 12))
        self.canvas.create_window(440, 150, width=880, height=30,
                                  window=header)

        # Resampling function
        oringinalrate_label = tk.Label(text="Original \n Rate(Hz):")
        oringinalrate_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(90, 200, width=120, height=40,
                                  window=oringinalrate_label)

        default_rate = tk.StringVar(value='80')
        self.org_rateselection = tk.Entry(textvariable=default_rate)
        self.org_rateselection.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(200, 200, width=100, height=30,
                                  window=self.org_rateselection)

        resamplingrate_label = tk.Label(text="Resampling \n Rate(Hz):")
        resamplingrate_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(360, 200, width=120, height=40,
                                  window=resamplingrate_label)

        self.resamplingrate = tk.Entry("")
        self.resamplingrate.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(470, 200, width=100, height=30,
                                  window=self.resamplingrate)

        b_resampling = tk.Button(self.master, text="Resample CSV")
        b_resampling["command"] = lambda: self.resampling(self.fileselection.get(), self.org_rateselection.get(), self.resamplingrate.get())
        b_resampling.config(bg=self.bgcolor)
        self.canvas.create_window(800, 200, width=100, height=30,
                                  window=b_resampling)
        self.check_header = tk.StringVar()
        b_withheader = tk.Checkbutton(self.master, text="with header", variable=self.check_header, onvalue="with header",
                                      offvalue="No header")
        b_withheader.config(bg=self.bgcolor, font=("Courier", 10))
        self.canvas.create_window(650, 200, width=120, height=30,
                                  window=b_withheader)
        b_withheader.select()



        # Reformat function
        utcyear_label = tk.Label(text="UTC Year:")
        utcyear_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(90, 270, width=120, height=40,
                                  window=utcyear_label)

        default_utcyear = tk.StringVar(value=str(datetime.datetime.today().year))
        self.b_utcyear = tk.Entry(textvariable=default_utcyear)
        self.b_utcyear.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(200, 270, width=100, height=30,
                                  window=self.b_utcyear)

        delimiter_label = tk.Label(text="delimiter:")
        delimiter_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(350, 270, width=100, height=30,
                                  window=delimiter_label)

        self.delimiter_sel = tk.ttk.Combobox(self.master)
        self.delimiter_sel["values"] = ["Comma", "Semicolon", "Tab", "Space"]
        self.delimiter_sel.configure(state="readonly")
        self.delimiter_sel.current(0)
        self.canvas.create_window(470, 270, width=100, height=30,
                                  window=self.delimiter_sel)

        b_reformat = tk.Button(self.master, text="Reformat ASCB_D")
        b_reformat["command"] = lambda: self.reformat_csv()
        b_reformat.config(bg=self.bgcolor)
        self.canvas.create_window(800, 270, width=100, height=30,
                                  window=b_reformat)

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
        self.fileselection.set('')
        currentfolder = self.inputfolder["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.inputfolder["text"] = selectedfolder
        self.fileselection['values'] = self.list_files(selectedfolder)

    def outputfolderselection(self):
        currentfolder = self.outputfolder["text"]
        selectedfolder = tk.filedialog.askdirectory()
        if selectedfolder == "":
            selectedfolder = currentfolder
        self.outputfolder["text"] = selectedfolder

    def list_files(self, directory):
        csvfiles = []
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                csvfiles.append(f)
        if csvfiles == []:
            self.inputfolder["fg"] = "red"
        else:
            self.inputfolder["fg"] = "green"
        return csvfiles

    def getdelimiter(self):
        delimiter = ""
        if self.delimiter_sel.get() == "Comma":
            delimiter = ","
        elif self.delimiter_sel.get() == "Semicolon":
            delimiter = ";"
        elif self.delimiter_sel.get() == "Tab":
            delimiter = "\t"
        elif self.delimiter_sel.get() == "Space":
            delimiter = " "
        return delimiter


    def resampling(self, filename, original_rate, rate):
        if filename == "" or rate == "" or original_rate == "":
            errormessage = "please select one file and original rate and resampling rate, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if "_resampled_" in filename:
            errormessage = "Cannot resample file which is aleardy resampled"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if not original_rate.isdecimal() or not rate.isdecimal():
            errormessage = "Please input integer as rate value"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        ration = int(original_rate) / int(rate)
        if not ration.is_integer():
            errormessage = "The initial sampling rate should be an integer multiple of the resampling rate"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if not float(ration).is_integer():
            errormessage = "Make sure original rate is integral number of resampling rate"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None

        inputfile = self.inputfolder["text"] + "/" + filename
        if self.outputfolder["text"] == "Same with input folder by default":
            Outputfile = inputfile[0:len(inputfile)-4] + "_resampled_" + rate + "Hz.csv"
        else:
            Outputfile = self.outputfolder["text"] + "/" + filename[0:len(filename)-4] + "_resampled_" + rate + "Hz.csv"
        overwriteflag = True
        if os.path.exists(Outputfile):
            overwriteflag = tk.messagebox.askokcancel("resampled file exists", "Resampled file exists, overwrite?")
        if overwriteflag == False:
            return None

        selecteddelimiter = self.getdelimiter()
        try:
            with open(inputfile, newline='') as csvfile:
                print("Open original data file")
                spamreader = csv.reader(csvfile, delimiter=selecteddelimiter)
                counter = 0
                with open(Outputfile, 'w', newline='') as newcsvfile:
                    print("Open resampled data file")
                    filewriter = csv.writer(newcsvfile, delimiter=selecteddelimiter, quoting=csv.QUOTE_MINIMAL)
                    print("Writing data...")

                    # check box clicked, write header in new file, start resampling from second row
                    if self.check_header.get() == "with header":
                        header = next(spamreader)
                        filewriter.writerow(header)

                    for row in spamreader:
                        if counter == ration:
                            counter = 0
                        if counter == 0:
                            filewriter.writerow(row)
                        counter += 1
            print("Finished:D")
        except PermissionError:
            errormessage = "please make sure data file is closed and accessible, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)



    def reformat_csv(self):
        #general check about user input
        if self.fileselection.get() == "":
            errormessage = "please select one file, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if self.b_utcyear.get() != "":
            template = "^20[1-2][0-9]$"
            inputyear = self.b_utcyear.get()
            if re.match(template, inputyear) == None:
                errormessage = "please input right format of year 20xx, thank you:D"
                tk.messagebox.showerror(title=None, message=errormessage)
                return None
            else:
                utcyear = inputyear

        # define input & output filename
        inputfile = self.inputfolder["text"] + "/" + self.fileselection.get()
        if self.outputfolder["text"] == "Same with input folder by default":
            Outputfile = inputfile[0:len(inputfile)-4] + "_reformat.xlsx"
        else:
            Outputfile = self.outputfolder["text"] + self.fileselection.get()[0:len(inputfile)-4] + "_reformat.xlsx"
        if os.path.exists(Outputfile):
            errormessage = "Excel file exists, please remove it before reformat, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None

        # reformat file:
        def is_number(s):       # function will be used later
            try:
                float(s)
                return True
            except ValueError:
                return False
        new_headers = list()
        new_headers.append("UTC Time")
        parameter_position = 0
        col_count = 0
        values_position = list()
        values = list()
        selecteddelimiter = self.getdelimiter()
        try:
            with open(inputfile, newline='') as csvfile:
                print("Open original file")
                spamreader = csv.reader(csvfile, delimiter=selecteddelimiter)
                headers = next(spamreader)
                print(headers)
                if "IRIG Time" not in headers or "Parameter Name" not in headers or "Value" not in headers:
                    errormessage = "Please make sure right delimiter selected and \"IRIG Time\", \"Parameter Name\" " \
                                   "and " "\"Value\" in the first row of CSV file"
                    tk.messagebox.showerror(title=None, message=errormessage)
                    return None
                secound_row = next(spamreader)
                print("Matching MNEs...")
                for header in headers:
                    if header == "IRIG Time":
                        values_position.append(col_count)
                    if header == "Parameter Name":
                        parameter_position = col_count
                    if header == "Value" and secound_row[col_count].strip() != "":
                        new_headers.append(secound_row[parameter_position][3:])
                        values_position.append(col_count)
                    col_count += 1

                parameter_position = 0
                for col in secound_row:
                    if parameter_position in values_position:
                        if parameter_position == values_position[0]:
                            utc_time_str = utcyear + ":" + col
                            utc_time = datetime.datetime.strptime(utc_time_str, '%Y:%j:%H:%M:%S.%f')
                            values.append(utc_time)
                        else:
                            if "0x " in col:
                                lastbit = col[len(col)-1]
                                if is_number(lastbit):
                                    values.append(lastbit)
                                else:
                                    values.append(col[3:5])
                            else:
                                values.append(col)
                    parameter_position += 1
                print("Create New file and Writing data...")
                workbook = xlsxwriter.Workbook(Outputfile)
                worksheet = workbook.add_worksheet()
                worksheet.set_column('A:A', 30)
                date_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss.000',
                                                   'align': 'left'})
                row_num = 0
                for col_num, col_value in enumerate(new_headers):
                    worksheet.write_string(row_num, col_num, col_value)
                row_num += 1
                for col_num, col_value in enumerate(values):
                    if isinstance(col_value, str):
                        if is_number(col_value):
                            worksheet.write_number(row_num, col_num, float(col_value))
                        else:
                            worksheet.write_string(row_num, col_num, col_value)
                    else:
                        worksheet.write_datetime(row_num, col_num, col_value, date_format)
                row_num += 1

                for row in spamreader:
                    values.clear()
                    parameter_position = 0
                    for col_value in row:
                        if parameter_position in values_position:
                            if parameter_position == values_position[0]:
                                utc_time_str = utcyear + ":" + col_value
                                utc_time = datetime.datetime.strptime(utc_time_str, '%Y:%j:%H:%M:%S.%f')
                                values.append(utc_time)
                            else:
                                if "0x " in col_value:
                                    lastbit = col_value[len(col_value) - 1]
                                    if is_number(lastbit):
                                        values.append(lastbit)
                                    else:
                                        values.append(col_value[3:5])
                                else:
                                    values.append(col_value)
                        parameter_position += 1
                    for col_num, col_value in enumerate(values):
                        if isinstance(col_value, str):
                            if is_number(col_value):
                                worksheet.write_number(row_num, col_num, float(col_value))
                            else:
                                worksheet.write_string(row_num, col_num, col_value)
                        else:
                            worksheet.write_datetime(row_num, col_num, col_value, date_format)
                    row_num += 1
                workbook.close()
                print("reformat finished!:D")
        except PermissionError:
            errormessage = "please make sure data file is closed and accessible, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)


root = tk.Tk()
root.title("Welcome to ASCB-D CSV Data Processing Tool")
root.geometry('880x500+500+200')
root.resizable(0, 0)
root.configure(bg='white')

app = Application(master=root)
app.mainloop()
