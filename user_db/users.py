import tkinter as tk
from tkinter import ttk
import sqlite3

class DatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("مدیریت افراد")
        
        # ایجاد یک پایگاه داده SQLite و جدول اطلاعات افراد
        self.conn = sqlite3.connect('people.db')
        self.create_table()

        # ایجاد ویژگی‌ها
        self.name_var = tk.StringVar()
        print(self.name_var)
        self.last_name_var = tk.StringVar()
        print(self.last_name_var)
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.postal_code_var = tk.StringVar()
        print(type(self.postal_code_var))

        # ایجاد ویژگی‌های ورودی
        self.name_entry = ttk.Entry(master, textvariable=self.name_var, width=30)
        self.last_name_entry = ttk.Entry(master, textvariable=self.last_name_var, width=30)
        self.phone_entry = ttk.Entry(master, textvariable=self.phone_var, width=30)
        self.email_entry = ttk.Entry(master, textvariable=self.email_var, width=30)
        self.address_entry = ttk.Entry(master, textvariable=self.address_var, width=30)
        self.postal_code_entry = ttk.Entry(master, textvariable=self.postal_code_var, width=30)

        # ایجاد دکمه‌ها
        ttk.Button(master, text="افزودن کاربر", command=self.add_user).grid(row=7, column=0, columnspan=1, pady=10, padx = 20)
        ttk.Button(master, text="مشاهده کاربران", command=self.view_users).grid(row=7, column=1, columnspan=1, pady=10, padx = 20)
        ttk.Button(master, text="جستجو در افراد", command=self.search_users).grid(row=7, column=2, columnspan=1, pady=10, padx = 20)

        # ایجاد برچسب‌ها
        ttk.Label(master, text="نام:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(master, text="نام خانوادگی:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(master, text="شماره تماس:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(master, text="ایمیل:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(master, text="آدرس:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(master, text="کد پستی:").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        # قرار دادن ورودی‌ها در شبکه
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=5)
        self.last_name_entry.grid(row=1, column=1, columnspan=2, pady=5)
        self.phone_entry.grid(row=2, column=1, columnspan=2, pady=5)
        self.email_entry.grid(row=3, column=1, columnspan=2, pady=5)
        self.address_entry.grid(row=4, column=1, columnspan=2, pady=5)
        self.postal_code_entry.grid(row=5, column=1, columnspan=2, pady=5)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                postal_code TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self):
        name = self.name_var.get()
        last_name = self.last_name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()
        postal_code = self.postal_code_var.get()

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO people (name, last_name, phone, email, address, postal_code)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, last_name, phone, email, address, postal_code))
        self.conn.commit()

        # پاک کردن محتوای ورودی‌ها بعد از افزودن کاربر
        self.name_var.set('')
        self.last_name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.address_var.set('')
        self.postal_code_var.set('')

    def view_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM people')
        records = cursor.fetchall()

        # نمایش اطلاعات در یک پنجره جدید
        new_window = tk.Toplevel(self.master)
        new_window.title("لیست افراد")

        # ایجاد یک جدول برای نمایش اطلاعات
        tree = ttk.Treeview(new_window, columns=("ID", "نام", "نام خانوادگی", "شماره تماس", "ایمیل", "آدرس", "کد پستی"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("نام", text="نام")
        tree.heading("نام خانوادگی", text="نام خانوادگی")
        tree.heading("شماره تماس", text="شماره تماس")
        tree.heading("ایمیل", text="ایمیل")
        tree.heading("آدرس", text="آدرس")
        tree.heading("کد پستی", text="کد پستی")

        for record in records:
            tree.insert("", "end", values=record)

        tree.pack()

    def search_users(self):
        # ایجاد یک پنجره جدید برای جستجو
        search_window = tk.Toplevel(self.master)
        search_window.title("جستجو در افراد")

        # ایجاد ویژگی برای جستجو
        search_var = tk.StringVar()

        # ایجاد ورودی برای جستجو
        search_entry = ttk.Entry(search_window, textvariable=search_var, width=30)
        search_entry.pack(pady=10)

        # ایجاد دکمه برای شروع جستجو
        ttk.Button(search_window, text="جستجو", command=lambda: self.search_results(search_var.get())).pack()

    def search_results(self, search_term):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM people
            WHERE name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR postal_code LIKE ?
        ''', ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        records = cursor.fetchall()

        # نمایش نتایج جستجو در یک پنجره جدید
        search_results_window = tk.Toplevel(self.master)
        search_results_window.title("نتایج جستجو")

        # ایجاد یک جدول برای نمایش نتایج جستجو
        tree = ttk.Treeview(search_results_window, columns=("ID", "نام", "نام خانوادگی", "شماره تماس", "ایمیل", "آدرس", "کد پستی"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("نام", text="نام")
        tree.heading("نام خانوادگی", text="نام خانوادگی")
        tree.heading("شماره تماس", text="شماره تماس")
        tree.heading("ایمیل", text="ایمیل")
        tree.heading("آدرس", text="آدرس")
        tree.heading("کد پستی", text="کد پستی")

        for record in records:
            tree.insert("", "end", values=record)

        tree.pack()

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
