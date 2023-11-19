import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.entry_var, font=('Helvetica', 16), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, sticky='nsew')

        button_texts = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('CE', 5, 0),  # افزودن دکمه CE
        ]

        for (text, row, col) in button_texts:
            button = ttk.Button(root, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky='nsew')
            button.grid(padx=5, pady=5)

    def on_button_click(self, button_text):
        current_entry_text = self.entry_var.get()

        if button_text == '=':
            try:
                result = eval(current_entry_text)
                self.entry_var.set(result)
            except Exception as e:
                self.entry_var.set("Error")
        elif button_text == 'CE':
            self.entry_var.set('')  # پاک کردن محتوای ورودی
        else:
            self.entry_var.set(current_entry_text + button_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
