# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.scrolledtext as scrolledtext


class TextArea(scrolledtext.ScrolledText):

    def __init__(self, root, status_bar):
        super().__init__(root, undo=True)
        self.status_bar = status_bar

    def remove_duplicates(self):
        content = self.get(1.0, tk.END)
        content = content.strip().split()
        wd_content = []
        for line in content:
            if line not in wd_content:
                wd_content.append(line)
        self.delete(1.0, tk.END)
        self.insert(1.0, '\n'.join(wd_content))
        self.status_bar.set('Usunięto duplikaty')
        self.status_bar.clear_sleep()
