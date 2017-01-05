from Tkinter import *
import tkFileDialog
import os
from merge_csv import merge_csv
import subprocess

class App:

    def __init__(self, root):

        self.frame = Frame(root)
        self.frame.pack()

        self.select_ng_btn = Button(self.frame, 
            text="Select SAM Data File", 
            command=self.select_ng_data_file)
        
        self.select_u_btn = Button(self.frame, 
            text="Select U Data File", 
            command=self.select_u_data_file)

        self.merge_btn = Button(self.frame, 
            text="Merge Data", 
            command=self.merge_data, 
            state=DISABLED)

        self.ng_data_file_name = StringVar(value="SAM Data: none")
        self.ng_data_file_label = Label(self.frame, textvariable=self.ng_data_file_name)

        self.u_data_file_name = StringVar(value="U Data: none")
        self.u_data_file_label = Label(self.frame, textvariable=self.u_data_file_name)

        button_opt = {'fill': X, 'padx': 10, 'pady': 5}
        self.select_ng_btn.pack(**button_opt)
        self.ng_data_file_label.pack(fill=X)
        self.select_u_btn.pack(**button_opt)
        self.u_data_file_label.pack(fill=X)
        self.merge_btn.pack(**button_opt)
        self.u_data_file = ""
        self.ng_data_file = ""

    def select_u_data_file(self):
        self.u_data_file = self.select_csv_file()
        basename = os.path.basename(self.u_data_file)
        self.u_data_file_name.set("U Data: "+basename)
        self.set_merge_btn_state()

    def select_ng_data_file(self):
        self.ng_data_file = self.select_csv_file() 
        basename = os.path.basename(self.ng_data_file)
        self.ng_data_file_name.set("SAM Data: "+basename)
        self.set_merge_btn_state()

    def select_csv_file(self):
        return tkFileDialog.askopenfilename(filetypes=[('csv files', '.csv')], parent=self.frame)

    def set_merge_btn_state(self):
        if self.u_data_file and self.ng_data_file:
            self.merge_btn.config(state=NORMAL)
        else:
            self.merge_btn.config(state=DISABLED)

    def merge_data(self):
        merged_data, columns = merge_csv(self.u_data_file, self.ng_data_file)
        self.save_dataframe(merged_data, columns)
        
    def save_dataframe(self, data, columns):
        filename = os.path.splitext(os.path.basename(self.ng_data_file))[0]+"_R180U.csv"
        outfile_name = tkFileDialog.asksaveasfilename(
            filetypes=[('csv file', '.csv')], 
            parent=self.frame, 
            title='save output', 
            initialfile= filename)
        if not os.path.splitext(outfile_name)[1] == '.csv':
        	outfile_name = outfile_name + '.csv'
        if outfile_name:
            data.to_csv(outfile_name, header=True, columns=columns.tolist(), index=False)
            if sys.platform == 'darwin':
                subprocess.call(["open", "-R", outfile_name])
            elif sys.platform == 'win32':
                subprocess.Popen(r'explorer /select,"{}"'.format(os.path.abspath(outfile_name)))

if __name__ == '__main__':
    root = Tk()
    root.geometry("250x200")
    app = App(root)
    root.wm_title("R180 CSV Merge Tool")
    mainloop()