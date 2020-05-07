# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.filedialog import askopenfilename, asksaveasfilename
from txt_area import TextArea
from status_bar import StatusBar


#TODO w ustawieniach możliwość wyłączenia przesuwani po enterze oraz możliwość ustawienia wartości skoku


class GET(object):

    DOWN_FACTOR = 20
    COLUMN_SELECT = True
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
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill='both', expand=True)
        self.text_area = TextArea(self.root, self.status_bar)
        self.text_area['font'] = ('consolas', '12')
        self.text_area.pack(expand=True, fill='both')
        if self.COLUMN_SELECT:
            self.text_area.bind('<ButtonPress-1>', self.text_area.column_select_start)
            self.text_area.bind('<B1-Motion>', self.text_area.active_choice)
            self.text_area.bind('<ButtonRelease-1>', self.text_area.column_select)
            self.text_area.bind('<Control-x>', self.cut)
            self.text_area.bind('<Control-X>', self.cut)
            self.text_area.bind('<Control-v>', self.paste)
            self.text_area.bind('<Control-V>', self.paste)
            self.text_area.bind('<Control-c>', self.copy)
            self.text_area.bind('<Control-C>', self.copy)
            self.text_area.tag_configure("block", background="gainsboro")
            self.text_area.tag_configure("sel", background='black',
                                             foreground='lime green')
        else:
            self.text_area.tag_delete("block")
            self.text_area.unbind('<ButtonPress-1>')
            self.text_area.unbind('<B1-Motion>')
            self.text_area.unbind('<ButtonRelease-1>')
            self.text_area.tag_configure("sel", background='gainsboro')


    def menu_bar(self):
        self.menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Otwórz', command=self.open_file)
        self.file_menu.add_command(label='Zapisz', command=self.save_file, accelerator='Ctrl+S')
        self.file_menu.add_command(label='Zapisz jako...', command=self.save_file_as)
        # menu edycji
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label='Kopiuj', command=self.copy, accelerator='Ctrl+C')
        self.edit_menu.add_command(label='Wklej', command=self.paste, accelerator='Ctrl+V')
        self.edit_menu.add_command(label='Wytnij', command=self.cut, accelerator='Ctrl+X')
        # menu operacji na liniach
        self.line_menu = tk.Menu(self.menu, tearoff=0)
        self.line_menu.add_command(label='Usuń duplikaty', command=self.text_area.remove_duplicates)
        # menu operacji na kolumnach
        self.column_menu = tk.Menu(self.menu, tearoff=0)
        self.column_menu.add_command(label='Zamiana początkowych kolumn', command=self.text_area.column_swap)
        # pomoc
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='O programie', command=self.help)

        self.menu.add_cascade(label='Plik', menu=self.file_menu)
        self.menu.add_cascade(label='Edycja', menu=self.edit_menu)
        self.menu.add_cascade(label='Linie', menu=self.line_menu)
        self.menu.add_cascade(label='Kolumny', menu=self.column_menu)
        self.menu.add_cascade(label='Pomoc', menu=self.help_menu)

        self.root.config(menu=self.menu)

    def read_chunk(self):
        return self.file.read(1024)

    def open_file(self):
        self.text_area.clear()
        self.file_path = askopenfilename(title='Wskaż plik', initialdir='./')
        self.file = open(self.file_path)
        for frag in iter(self.read_chunk, ''):
            self.text_area.insert(tk.END, frag)
        self.status_bar.set(self.file_path)

    def save_file(self):
        content = self.text_area.get(1.0, tk.END)
        try:
            with open(self.file_path, 'w') as save_file:
                save_file.writelines(content)
                self.status_bar.set('Zapisano!')
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

    def copy(self, event):
        if self.COLUMN_SELECT:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text_area.block_txt.strip())
            except AttributeError:
                pass
        else:
            self.text_area.event_generate("<<Copy>>")
        return "break"

    def paste(self, event):
        if self.COLUMN_SELECT:
            try:
                w, k = self.text_area.index(tk.INSERT).split('.')
                w_kon, k_kon = self.text_area.index(tk.END).split('.')
                ran = int(w_kon) - int(w)
                clipboard = self.root.clipboard_get().split('\n')
                if ran < len(clipboard):
                    showwarning('UWAGA', 'Dane poza zakresem!')
                clipboard = clipboard[0:ran]
                for l in range(0, len(clipboard)):
                    wiersz = str(int(w) + l)
                    self.text_area.insert("%s.%s" % (wiersz, k), clipboard[l])
            except tk.TclError:
                pass
        else:
            self.text_area.event_generate("<<Paste>>")
        return "break"

    def cut(self, event):
        if self.COLUMN_SELECT:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text_area.block_txt.strip())
                for i in range(int(self.text_area.start_row), int(self.text_area.row) + 1):
                    self.text_area.delete('%s.%s' % (i, self.text_area.start_column),
                                              '%s.%s' % (i, self.text_area.column))
            except AttributeError:
                pass
        else:
            self.text_area.event_generate("<<Cut>>")
        return "break"


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



