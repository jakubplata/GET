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

    def choice(self, row, col):
        if row != self.start_row or col != self.start_column:
            if self.start_row >= row or self.start_column >= col:
                for i in range(int(row), int(self.start_row) + 1):
                    self.tag_add("sel", '%s.%s' % (i, col),
                                               '%s.%s' % (i, self.start_column))
            else:
                for i in range(int(self.start_row), int(row) + 1):
                    self.tag_add("sel", '%s.%s' %
                                               (i, self.start_column),
                                               '%s.%s' % (i, col))

    def active_choice(self, event=None):
        self.tag_remove('sel', 1.0, tk.END)
        self.tag_remove('block', 1.0, tk.END)
        row, col = self.index(tk.INSERT).split('.')
        self.choice(row, col)

    def column_select_start(self, event):
        self.tag_remove('sel', 1.0, tk.END)
        self.start_row, self.start_column = self.index(tk.CURRENT).split('.')

    def column_select(self, event):
        self.block_txt = ''
        self.row, self.column = self.index(tk.INSERT).split('.')
        self.tag_remove('sel', 1.0, tk.END)
        self.tag_remove('block', 1.0, tk.END)
        if self.start_row >= self.row or self.start_column >= self.column:
            self.row, self.column, self.start_row, self.start_column = self.start_row, self.start_column,\
                                                                       self.row, self.column
        for i in range(int(self.start_row), int(self.row)+1):
            self.block_txt += self.get('%s.%s' % (i, self.start_column), '%s.%s' % (i, self.column)) + '\n'
            self.tag_add('block', '%s.%s' % (i, self.start_column), '%s.%s' % (i, self.column))

