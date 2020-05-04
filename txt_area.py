# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter.messagebox import showwarning


class TextArea(scrolledtext.ScrolledText):

    def __init__(self, root, status_bar):
        super().__init__(root, undo=True)
        self.status_bar = status_bar

    def _get_content(self):
        content = self.get(1.0, tk.END)
        content = content.strip().split('\n')
        return content

    def clear(self):
        self.delete(1.0, tk.END)

    def remove_duplicates(self):
        content = self._get_content()
        wd_content = []
        for line in content:
            if line not in wd_content:
                wd_content.append(line)
        self.clear()
        self.insert(1.0, '\n'.join(wd_content))
        self.status_bar.set('Usunięto duplikaty')

    def column_swap(self):
        content = self._get_content()
        swap_content = []
        for line in content:
            print(line)
            words = line.split()
            if len(words) == 2:
                new_line = '\t'.join(words[::-1])
            elif len(words) > 2:
                new_words = words[2:]
                new_words.insert(0, words[0])
                new_words.insert(0, words[1])
                new_line = '\t'.join(new_words)
            else:
                new_line = '\t'.join(words)
            swap_content.append(new_line)
        self.clear()
        self.insert(1.0, '\n'.join(swap_content))
        self.status_bar.set('Zamienion początkowe kolumn')