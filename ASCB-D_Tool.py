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

        # Resampling function
        oringinalrate_label = tk.Label(text="Original \n Rate(Hz):")
        oringinalrate_label.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(90, 200, width=120, height=40,
                                  window=oringinalrate_label)

        v = tk.StringVar(value='80')
        self.org_rateselection = tk.Entry(textvariable = v)
        self.org_rateselection.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(200, 200, width=100, height=30,
                                  window=self.org_rateselection)

        label3 = tk.Label(text="Resampling \n Rate(Hz):")
        label3.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(360, 200, width=120, height=40,
                                  window=label3)

        self.rateselection = tk.Entry("")
        self.rateselection.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(470, 200, width=100, height=30,
                                  window=self.rateselection)

        b_resampling = tk.Button(self.master, text="Resample CSV")
        b_resampling["command"] = lambda: self.resampling(self.fileselection.get(), self.org_rateselection.get(), self.rateselection.get())
        b_resampling.config(bg=self.bgcolor)
        self.canvas.create_window(800, 200, width=100, height=30,
                                  window=b_resampling)
        self.check_var1 = tk.StringVar()
        b_withheader = tk.Checkbutton(self.master, text="with header", variable=self.check_var1, onvalue="with header",
                                      offvalue="No header")
        b_withheader.config(bg=self.bgcolor, font=("Courier", 10))
        self.canvas.create_window(650, 200, width=120, height=30,
                                  window=b_withheader)
        b_withheader.select()



        # Reformat function
        label4 = tk.Label(text="UTC Year:")
        label4.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(80, 300, width=100, height=30,
                                  window=label4)
        self.b_utcyear = tk.Entry("")
        self.b_utcyear.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(270, 300, width=100, height=30,
                                  window=self.b_utcyear)

        label4 = tk.Label(text="(Use this year when no input)")
        label4.config(bg=self.bgcolor, font=("Courier", 12))
        self.canvas.create_window(480, 300, width=300, height=30,
                                  window=label4)


        b_reformat = tk.Button(self.master, text="Reformat ASCB_D")
        b_reformat["command"] = lambda: self.reformat_csv()
        b_reformat.config(bg=self.bgcolor)
        self.canvas.create_window(800, 300, width=100, height=30,
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

        inputfile = self.label1["text"] + "/" + filename
        Outputfile = inputfile[0:len(inputfile) - 4] + "_resampled_" + rate + "Hz.csv"
        overwriteflag = True
        if os.path.exists(Outputfile):
            overwriteflag = tk.messagebox.askokcancel("resampled file exists", "Resampled file exists, overwrite?")
        if overwriteflag == False:
            return None
        try:
            with open(inputfile, newline='') as csvfile:
                print("Open original data file")
                spamreader = csv.reader(csvfile)
                counter = 0
                with open(Outputfile, 'w', newline='') as newcsvfile:
                    print("Open resampled data file")
                    filewriter = csv.writer(newcsvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    print("Writing data...")

                    # check box clicked, write header in new file, start resampling from second row
                    if self.check_var1.get() == "with header":
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
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False
        if self.fileselection.get() == "":
            errormessage = "please select one file, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None
        if self.b_utcyear.get() == "":
            utcyear = str(datetime.datetime.today().year)
        if self.b_utcyear.get() != "":
            template = "^20[1-2][0-9]$"
            inputyear = self.b_utcyear.get()
            if re.match(template, inputyear) == None:
                errormessage = "please input right format of year 20xx, thank you:D"
                tk.messagebox.showerror(title=None, message=errormessage)
                return None
            else:
                utcyear = inputyear

        inputfile = self.label1["text"] + "/" + self.fileselection.get()
        Outputfile = inputfile[0:len(inputfile) - 4] + "_reformat.xlsx"
        if os.path.exists(Outputfile):
            errormessage = "Excel file exists, please remove it before reformat, thank you:D"
            tk.messagebox.showerror(title=None, message=errormessage)
            return None

        new_headers = list()
        new_headers.append("UTC Time")
        parameter_position = 0
        col_count = 0
        values_position = list()
        values = list()
        try:
            with open(inputfile, newline='') as csvfile:
                print("Open original file")
                spamreader = csv.reader(csvfile, delimiter=',')
                headers = next(spamreader)
                if "IRIG Time" not in headers or "Parameter Name" not in headers or "Value" not in headers:
                    errormessage = "Please configure FLIGHTLINE to set \"IRIG Time\", \"Parameter Name\" and " \
                                   "\"Value\" in the first row of CSV file"
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
                                values.append(col[len(col) - 1:])
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
                                    values.append(col_value[len(col_value)-1:])
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
