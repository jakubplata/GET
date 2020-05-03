# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.filedialog import askopenfilename, asksaveasfilename
from txt_area import TextArea


#TODO pasek statusu - wykorzystać ten z aplikacji wcięcie podobnie jak okna dialogowe, potrzebne duże okno do ustawien
#TODO w ustawieniach możliwość wyłączenia przesuwani po enterze oraz możliwość ustawienia wartości skoku


class GET(object):

    DOWN_FACTOR = 20
    _VERSION = '0.1'
    _helptext = """
        GET - %s
        Geodezyjny Edytor Tekstowy
    """

    def __init__(self, root):
        self.root = root
        self.root.title('GET')
        self.root.geometry('450x200')
        self.root.bind('<Return>', self.move)
        self.root.bind('<Control-s>', self.save_file_shrt)

        self.make_widgets()
        self.menu_bar()

    def make_widgets(self):
        self.text_area = TextArea(self.root)
        self.text_area['font'] = ('consolas', '12')
        self.text_area.pack(expand=True, fill='both')

    def menu_bar(self):
        self.menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Otwórz', command=self.open_file)
        self.file_menu.add_command(label='Zapisz', command=self.save_file, accelerator='Ctrl+S')
        self.file_menu.add_command(label='Zapisz jako...', command=self.save_file_as)

        self.line_menu = tk.Menu(self.menu, tearoff=0)
        self.line_menu.add_command(label='Usuń duplikaty', command=self.text_area.remove_duplicates)



        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='O programie', command=self.help)

        self.menu.add_cascade(label='Plik', menu=self.file_menu)
        self.menu.add_cascade(label='Linie', menu=self.line_menu)
        self.menu.add_cascade(label='Pomoc', menu=self.help_menu)

        self.root.config(menu=self.menu)

    def read_chunk(self):
        return self.file.read(1024)

    def open_file(self):
        self.file_path = askopenfilename(title='Wskaż plik', initialdir='./')
        self.file = open(self.file_path)
        for frag in iter(self.read_chunk, ''):
            self.text_area.insert(tk.END, frag)

    def save_file(self):
        content = self.text_area.get(1.0, tk.END)
        try:
            with open(self.file_path, 'w') as save_file:
                save_file.writelines(content)
        except AttributeError:
            self.save_file_as()

    def save_file_shrt(self, event):
        self.save_file()

    def save_file_as(self):
        content = self.text_area.get(1.0, tk.END)
        self.file_path = asksaveasfilename(title='Zapisz plik', initialdir='./')
        if content != '':
            try:
                with open(self.file_path, 'w') as save_file:
                    save_file.writelines(content)
            except FileNotFoundError:
                showwarning('Uwaga', 'Nie wskazano pliku!!!')

    def move(self, event):
        """
        Metoda umożliwiajaca przesuwanie całego okna w pionie,
        przydatana podczas przepisywania współrzędnych
        :param event:
        :return:
        """
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        y = str(int(current_y) + self.DOWN_FACTOR)
        self.root.geometry(f'+{current_x}+{y}')

    def help(self):
        showinfo('O programie', self._helptext % (self._VERSION))


def main():
    root = tk.Tk()
    GET(root)
    root.mainloop()


if __name__ == "__main__":
    main()



