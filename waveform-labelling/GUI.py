import csv
try:
    import Tkinter
except:
    import tkinter as Tkinter
    from tkinter import *
    from tkinter import messagebox
    from tkinter import ttk
    from tkinter import filedialog

import path
import image_load
import pandas as pd
import os

class PictureWindow(Tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        Tkinter.Canvas.__init__(self, *args, **kwargs)

        self.imagelist = path.get_image_list()
        self.current_index = 0

        self.rhythm_list = [0 for i in self.imagelist]
        self.rhythm_button_var = IntVar()

        self.noise_list = [0 for i in self.imagelist]
        self.noise_button_var = IntVar()

        self.all_function_trigger()
        self.show_image(self.imagelist[self.current_index])

    def get_image_list(self):
        path_to_data = filedialog.askdirectory()
        extensions = ['JPG', 'BMP', 'GIF', 'PNG']
        image_list = []
        for i in os.listdir(path_to_data):
            image_path = os.path.join(path_to_data, i)
            ext = image_path.split('.')[::-1][0].upper()
            if ext in extensions:
                image_list.append(image_path)

        return sorted(image_list)

    def update_fields(self):
        print('Button clicked')
        self.rhythm_list[self.current_index] = self.rhythm_button_var.get()
        self.noise_list[self.current_index] = self.noise_button_var.get()

    def load_fields(self):
        print('Load fields called')
        self.rhythm_button_var.set(self.rhythm_list[self.current_index])
        self.noise_button_var.set(self.noise_list[self.current_index])

    def show_image(self, image_path):
        img = image_load.format(image_path, 1300, 600)
        self.delete(self.find_withtag("bacl"))
        self.allready = self.create_image(0, 400, image=img,
                                          anchor='w', tag="bacl")
        self.image = img
        self.master.title("Image Viewer ({})".format(image_path))

        self.load_fields()

#        print(self.noise_list)
#        print(self.rhythm_list)

        return


    def submit(self):
        if 0 in self.rhythm_list:
            response = Tkinter.messagebox.askyesno("Question",'The following rhythms not selected:' +f'{[i for i in range(len(self.rhythm_list)) if self.rhythm_list[i] == 0]} Do you want to complete them?')
            if response:
                return

        self.save_to_csv()
        self.dataframe_to_csv()
        self.destroy()

    def save_to_csv(self):
        with open('class.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(self.rhythm_list)
        with open('noises.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(self.noise_list)

    def dataframe_to_csv(self):
        print('called')
        dict = {'Files': self.imagelist, 'Rhythm Classifications':self.rhythm_list, 'Noise Classifications':self.noise_list}
        df = pd.DataFrame(dict)
        print(df)
        export_csv = df.to_csv ('dataframe.csv', index = None, header=True)


    def previous_image(self):
        try:
            if self.current_index > 0:
                self.current_index = self.current_index - 1
                self.show_image(self.imagelist[self.current_index])
            else:
                print('On first image, can\'t go back')
        except:
            pass
        return

    def next_image(self):
        try:
            if self.current_index == len(self.imagelist)-1:
                print('On last image, can\'t go forward')
            else:
                self.current_index = self.current_index + 1
                self.show_image(self.imagelist[self.current_index])
        except:
            pass
        return


    def all_function_trigger(self):

        self.create_buttons_navigation()
        self.create_class_buttons()
        self.create_noise_buttons()
        self.window_settings()

        return

    def window_settings(self):
        self['width'] = 1400
        self['height'] = 800
        return


    def create_buttons_navigation(self):
        Tkinter.Button(self, text=" > ", command=self.next_image, highlightbackground ='#3E4149').place(x=500,
                                                                        y=40)
        Tkinter.Button(self, text=" < ", command=self.previous_image, highlightbackground ='#3E4149').place(x=450,
                                                                            y=40)

        Tkinter.Button(self, text="Submit", command=self.submit, highlightbackground ='#3E4149').place(x=1200,
                                                                   y=700)
        self['bg'] = "white"
        return


    def create_class_buttons(self):
        y_pos = 80

        ttk.Label(self,
                 text="""Choose Heart Rhythm:""",
                 justify=Tkinter.LEFT).place(x=100,y=y_pos-20)

        ttk.Radiobutton(self,
                        text="AF",
                        variable=self.rhythm_button_var,
                        command = self.update_fields,
                        value=1).place(x=100, y =y_pos)

        ttk.Radiobutton(self,
                       text="Noise",
                       variable=self.rhythm_button_var,
                        command=self.update_fields,
                        value=2).place(x=170, y =y_pos)

        ttk.Radiobutton(self,
                       text="Sinus",
                       variable=self.rhythm_button_var,
                        command=self.update_fields,
                        value=3).place(x=240, y=y_pos)

        ttk.Radiobutton(self,
                       text="Other",
                       variable=self.rhythm_button_var,
                        command=self.update_fields,
                        value=4).place(x=310, y=y_pos)

        ttk.Radiobutton(self,
                       text="Discard",
                       variable=self.rhythm_button_var,
                        command=self.update_fields,
                        value=5).place(x=380, y=y_pos)
                            
        self['bg'] = "white"
        return


    def create_noise_buttons(self):
        y_pos = 30
        ttk.Label(self,
                 text="""Choose Noise level:""",
                 justify=Tkinter.LEFT).place(x=100,y=y_pos-20)

        ttk.Radiobutton(self,
                        text="1",
                        variable=self.noise_button_var,
                        command = self.update_fields,
                        value=1).place(x=100, y =y_pos)
        ttk.Radiobutton(self,
                        text="2",
                        variable=self.noise_button_var,
                        command = self.update_fields,
                        value=2).place(x=160, y =y_pos)
        ttk.Radiobutton(self,
                        text="3",
                        variable=self.noise_button_var,
                        command = self.update_fields,
                        value=3).place(x=220, y =y_pos)
        ttk.Radiobutton(self,
                        text="4",
                        variable=self.noise_button_var,
                        command = self.update_fields,
                        value=4).place(x=280, y =y_pos)
        ttk.Radiobutton(self,
                        text="5",
                        variable=self.noise_button_var,
                        command = self.update_fields,
                        value=5).place(x=340, y =y_pos)

        self['bg'] = "white"
        return

    def keyboard_input(self, key):
        map = {'1':1, '2':2, '3':3, '4':4, '5':5, 'q':1, 'w':2, 'e':3, 'r':4, 't':5}
        if key in '12345':
            self.noise_list[self.current_index] = map[key]
        else:
            self.rhythm_list[self.current_index] = map[key]

        self.load_fields()





# Main Functionx§
def main():
    # Creating Window
    root = Tkinter.Tk(className=" Image Viewer")
    # Creating Canvas Widget
    pw = PictureWindow(root)
    pw.pack(expand="yes", fill="both")
    # Not Resizable
    root.resizable(width=0, height=0)
    root.bind('<Left>', lambda event: pw.previous_image())
    root.bind('<Right>', lambda event: pw.next_image())

    root.bind('q', lambda event: pw.keyboard_input('q'))
    root.bind('w', lambda event: pw.keyboard_input('w'))
    root.bind('e', lambda event: pw.keyboard_input('e'))
    root.bind('r', lambda event: pw.keyboard_input('r'))
    root.bind('t', lambda event: pw.keyboard_input('t'))


    root.bind('1', lambda event: pw.keyboard_input('1'))
    root.bind('2', lambda event: pw.keyboard_input('2'))
    root.bind('3', lambda event: pw.keyboard_input('3'))
    root.bind('4', lambda event: pw.keyboard_input('4'))
    root.bind('5', lambda event: pw.keyboard_input('5'))


#    root.bind('f', lambda event: pw.next_image())

    # Window Mainloop
    root.mainloop()
    return


# Main Function Trigger
if __name__ == '__main__':
    main()

