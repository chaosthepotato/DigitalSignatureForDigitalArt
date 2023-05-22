import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename
from Signature import *
from Stegano import *
import os

class UtilityFunction:
    @staticmethod
    def open_file():
        file_path = askopenfilename(filetypes=[('Files', '*')])
        if file_path is not None:
            pass
        return file_path
    
    def decryptClick(self, event=None):
        hid_msg = Decode(self.steganoFileName)
        val = Signature(hid_msg, self.keyFileName, mode="string")
        val2 = val.validateSign()
        if(val2 == True):
            tk.messagebox.showinfo("Decrypt Result",  "Valid")
        else:
            tk.messagebox.showinfo("Decrypt Result",  "Invalid")
    
    def steganoClick(self, mode, event=None):
        if(mode==1):
            sign = Signature(self.signFileName)
        elif(mode==2):
            signInput = self.input_signature_Text.get("1.0", 'end-1c')
            text_file = open("inputSign.txt", "w")
            n = text_file.write(signInput)
            text_file.close()
            sign = Signature('inputSign.txt')
            
        sign2 = sign.signFile()
        steg = Encode(self.fileName, sign2, "output.png")
        tk.messagebox.showinfo("Steganography Result",  "Signature Embedded.")
        
    def importKeyFile(self, event=None):
        self.keyFileName = UtilityFunction.open_file()
        self.input_key_Text.delete('1.0', 'end')
        self.input_key_Text.insert(tk.INSERT, self.keyFileName)

    def importPNGFile(self, event=None):
        self.fileName = UtilityFunction.open_file()
        self.input_png_Text.delete('1.0', 'end')
        self.input_png_Text.insert(tk.INSERT, self.fileName)
        
    def importSteganoPNGFile(self, event=None):
        self.steganoFileName = UtilityFunction.open_file()
        self.input_steganopng_Text.delete('1.0', 'end')
        self.input_steganopng_Text.insert(tk.INSERT, self.steganoFileName)
        
    def importSignFile(self, event=None):
        self.signFileName = UtilityFunction.open_file()
        self.input_sign_Text.delete('1.0', 'end')
        self.input_sign_Text.insert(tk.INSERT, self.signFileName)
        
    def getString(self, event=None):
        signInput = self.input_signature_Text.get("1.0", 'end-1c')
        text_file = open("testSign.txt", "w")
        n = text_file.write(signInput)
        text_file.close()
        print(signInput)
        print('////////////')
    
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        headerContainer = tk.Frame(self) 
        headerContainer.pack(side = "top", fill="both", padx=10)
  
        headerContainer.grid_rowconfigure(0, weight = 1)
        headerContainer.grid_columnconfigure(3, weight = 1)
        
        mainContainer = tk.Frame(self,highlightbackground="grey",highlightthickness=2) 
        mainContainer.pack(side = "bottom", fill = "both", padx=10, pady=(0,10))
  
        mainContainer.grid_rowconfigure(1, weight = 1)
        mainContainer.grid_columnconfigure(0, weight = 1)
        
        stegano_btn = ttk.Button(headerContainer, text ="Stegano", command = lambda : self.show_frame(Stegano))
        stegano_btn.grid(row = 0, column = 0, padx = 0, pady = 0, sticky='w')
        decrypt_btn = ttk.Button(headerContainer, text ="Decrypt", command = lambda : self.show_frame(Decrypt))
        decrypt_btn.grid(row = 0, column = 1, padx = 0, pady = 0, sticky='w')
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Stegano, Decrypt):
  
            frame = F(mainContainer, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Stegano)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class Stegano(tk.Frame):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        
        self.desc_label = tk.Label(self, text ="Apply Steganography to chosen file.\nThe signature file would be encrypted\nusing SHA256 + RSA method.", width=30, borderwidth=1, relief="solid", anchor='w', justify='left')
        self.desc_label.grid(row = 1, column = 1, padx = 10, pady = (5,5), columnspan=2, sticky='w')
        
        self.import_png_btn = ttk.Button(self, text ="Import PNG File", width=20, command=lambda : UtilityFunction.importPNGFile(self))
        self.import_png_btn.grid(row = 2, column = 1, padx = 10, pady = (25,5))
        self.input_png_Text = tk.Text(self, height = 1, width = 30)
        self.input_png_Text.grid(row = 2, column = 2, padx = 10, pady = (25,5), columnspan=3)
        
        self.import_sign_btn = ttk.Button(self, text ="Import Signature File", width=20, command=lambda : UtilityFunction.importSignFile(self))
        self.import_sign_btn.grid(row = 3, column = 1, padx = 10, pady = (5,5))
        self.input_sign_Text = tk.Text(self, height = 1, width = 30)
        self.input_sign_Text.grid(row = 3, column = 2, padx = 10, pady = (5,5), columnspan=3)
        
#         self.input_signature_label = ttk.Button(self, text ="Input Signature", width=20)
        self.input_signature_label = tk.Label(self, text ="Input Signature", width=17)
        self.input_signature_label.grid(row = 4, column = 1, padx = 10, pady = (5,5))
        self.input_signature_Text = tk.Text(self, height = 1, width = 30)
        self.input_signature_Text.grid(row = 4, column = 2, padx = 10, pady = (5,5), columnspan=3)
        
#         self.run_btn = ttk.Button(self, text ="Run", width=10, command=lambda : UtilityFunction.steganoClick(self, 1))
        self.run_btn = ttk.Button(self, text ="Run with Imported File", command=lambda : UtilityFunction.steganoClick(self, 1))
        self.run_btn.grid(row = 5, column = 2, padx = 0, pady = (0,25), sticky='e')
        self.run_input_btn = ttk.Button(self, text ="Run with Input", command=lambda : UtilityFunction.steganoClick(self, 2))
        self.run_input_btn.grid(row = 5, column = 3, padx = 0, pady = (0,25), sticky='w')

class Decrypt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.desc_decrypt_label = tk.Label(self, text ="Check the validity of the hash\nvalue of the hidden message within the\nimage file with the public key.", width=30, borderwidth=1, relief="solid", anchor='w', justify='left')
        self.desc_decrypt_label.grid(row = 1, column = 1, padx = 10, pady = (5,5), columnspan=2, sticky='w')
        
        self.import_steganopng_btn = ttk.Button(self, text ="Import PNG File", width=20, command=lambda : UtilityFunction.importSteganoPNGFile(self))
        self.import_steganopng_btn.grid(row = 2, column = 1, padx = 10, pady = (25,5))
        self.input_steganopng_Text = tk.Text(self, height = 1, width = 30)
        self.input_steganopng_Text.grid(row = 2, column = 2, padx = 10, pady = (25,5), columnspan=2)
        
        self.import_key_btn = ttk.Button(self, text ="Import Certificate File", width=20, command=lambda : UtilityFunction.importKeyFile(self))
        self.import_key_btn.grid(row = 3, column = 1, padx = 10, pady = (5,5))
        self.input_key_Text = tk.Text(self, height = 1, width = 30)
        self.input_key_Text.grid(row = 3, column = 2, padx = 10, pady = (5,5), columnspan=2)
        
        self.run_btn = ttk.Button(self, text ="Run", width=10, command=lambda : UtilityFunction.decryptClick(self))
        self.run_btn.grid(row = 4, column = 2, padx = 10, pady = (0,25))
  
  
# Driver Code
app = tkinterApp()
app.title('Image Digital Signing')
app.mainloop()