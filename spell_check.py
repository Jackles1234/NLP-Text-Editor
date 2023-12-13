import re
import nltk
import tkinter as tk
from nltk.corpus import words
from tkinter import *

nltk.download("words")


class SpellingChecker:
    def __init__(self, text1):
        self.text = text1
        self.text.bind("<KeyRelease>", self.check)
        self.text.pack()
        self.old_spaces = 0

    def check(self, event):
        #print("working")
        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        if space_count != self.old_spaces:
            self.old_spaces = space_count
            for word in content.split(" "):
                if re.sub(r"[^\w]", "", word.lower()) not in words.words():
                    position = content.find(word)
                    self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(word, foreground="red")


