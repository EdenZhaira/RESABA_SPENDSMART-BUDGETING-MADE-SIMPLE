import os
import sqlite3
from PIL import Image
import customtkinter as ctk

ctk.set_appearance_mode("dark")

DATABASE_NAME = "user_data.db"

def init_database():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Error")
        self.geometry("300x150")
        self.resizable(False, False)
        self.configure(fg_color="#E5CFD1")

        self.grab_set()
        self.focus_set()

        content_frame = ctk.CTkFrame(self, 
                                     fg_color="#E5CFD1")
        content_frame.place(relx=0.5, 
                            rely=0.5,
                            anchor="center")

        error_labeling = ctk.CTkLabel(content_frame, text=message,
                                   font=("Comic Sans MS",14, "bold"),
                                   text_color="#BB909B")
        error_labeling.pack(pady=(20, 10))

        close_button = ctk.CTkButton(content_frame, text="Close",
                                     font=("Comic Sans MS", 12),
                                     fg_color="#BB909B",
                                     text_color="#FFFFFF",
                                     hover_color="#EAE7E4",
                                     corner_radius=50,
                                     width=100,
                                     height=30,
                                     command=self.destroy)
        close_button.pack(pady=(10, 10))


class SuccessDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, callback=None):
        super().__init__(parent)
        self.callback = callback  
        self.title("Success")
        self.geometry("300x150")
        self.resizable(False, False)
        self.configure(fg_color="#E5CFD1")

        self.grab_set()
        self.focus_set()

        content_frame = ctk.CTkFrame(self, fg_color="#E5CFD1")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        success_label = ctk.CTkLabel(content_frame, text=message,
                                     font=("Comic Sans MS", 14, "bold"),
                                     text_color="#657E75")
        success_label.pack(pady=(20, 10))

        close_button = ctk.CTkButton(content_frame, text="Close",
                                     font=("Comic Sans MS", 12),
                                     fg_color="#BB909B",
                                     text_color="#FFFFFF",
                                     hover_color="#EAE7E4",
                                     corner_radius=50,
                                     width=100,
                                     height=30,
                                     command=self.on_close)
        close_button.pack(pady=(10, 10))

    def on_close(self):
        if self.callback: 
            self.callback() 
        self.destroy() 



class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SpendSmart: Budgeting Made Simple")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(fg_color="#E5CFD1")

        self.create_widgets()

    def create_widgets(self):
        left_frame = ctk.CTkFrame(self, width=250,
                                  height=500,
                                  fg_color="#8D99AE",
                                  corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=False)

        image_path = "Money_Money.jpg"
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
        else:
            wallet_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(250, 500)
            )
            wallet_label = ctk.CTkLabel(left_frame, image=wallet_image, text="")
            wallet_label.place(relx=0.5, rely=0.5, anchor="center")

        right_frame = ctk.CTkFrame(self, width=450, height=500, fg_color="#E5CFD1", corner_radius=20)
        right_frame.pack(side="right", fill="both", expand=True)

        content_frame = ctk.CTkFrame(right_frame, fg_color="#E5CFD1")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        label1 = ctk.CTkLabel(content_frame,
                              text="SpendSmart: Budgeting Made Simple",
                              font=("Comic Sans MS", 23, "bold"),
                              text_color="#657E75")
        label1.pack(pady=(80, 50))

        label2 = ctk.CTkLabel(content_frame,
                              text="Sign in to your account",
                              font=("Comic Sans MS", 16),
                              text_color="#657E75")
        label2.pack(pady=(0, 15))

        self.email_login = ctk.CTkEntry(content_frame, placeholder_text="Email",
                                        placeholder_text_color="#657E75",
                                        fg_color="#B6BAB3",
                                        border_color="#B6BAB3",
                                        text_color="#FFFFFF", width=300,
                                        height=40, corner_radius=70,
                                        font=("Comic Sans MS", 14))
        self.email_login.pack(pady=(0, 10))

        self.password_login = ctk.CTkEntry(content_frame, placeholder_text="Password",
                                           placeholder_text_color="#657E75",
                                           fg_color="#B6BAB3",
                                           border_color="#B6BAB3",
                                           text_color="#FFFFFF", show="*",
                                           width=300, height=40,
                                           corner_radius=70,
                                           font=("Comic Sans MS", 14))
        self.password_login.pack(pady=(5, 20))

        login_button = ctk.CTkButton(content_frame, text="Login",
                                     font=("Comic Sans MS", 16, "bold"),
                                     fg_color="#BB909B",
                                     text_color="#FFFFFF",
                                     hover_color="#EAE7E4",
                                     corner_radius=50,
                                     width=130, height=30,
                                     command=self.login)
        login_button.pack(pady=(0, 40))

        label3 = ctk.CTkLabel(content_frame, text="No account yet?",
                              font=("Comic Sans MS", 10),
                              text_color="#657E75")
        label3.pack(pady=(0, 0))

        signup_button = ctk.CTkButton(content_frame, text="SIGN UP",
                                      font=("Comic Sans MS", 12, "bold"),
                                      fg_color="#E5CFD1",
                                      text_color="#FFFFFF",
                                      hover_color="#E5CFD1",
                                      corner_radius=10,
                                      width=130, height=70,
                                      command=self.open_signup)
        signup_button.pack(pady=(0, 5))

    def login(self):
        email = self.email_login.get()
        password = self.password_login.get()

        # Check if the fields are empty
        if not email or not password:
            ErrorDialog(self, "Please enter both email and password.")
            return

        # Check the credentials against the database
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()

        if result:
            
            if result[0] == password:
                # Create success dialog with a callback
                SuccessDialog(self, "Login successful!", callback=self.open_budget_window)
                self.withdraw()  # Hide the login window
        
            else:
                ErrorDialog(self, "Incorrect password. Please try again.")
        else:
            ErrorDialog(self, "Email not registered. Please sign up.")

    def open_signup(self):
        self.withdraw()
        SignUpWindow(self)

    def open_budget_window(self):
        BudgetingWindow(self)


class SignUpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Sign Up - SpendSmart")
        self.geometry("400x450")
        self.resizable(False, False)
        self.configure(fg_color="#E5CFD1")

        content_frame = ctk.CTkFrame(self, fg_color="#E5CFD1")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(content_frame, text="Create Your Account",
                             font=("Comic Sans MS", 20, "bold"),
                             text_color="#657E75")
        label.pack(pady=(20, 20))

        self.email_signup = ctk.CTkEntry(content_frame, placeholder_text="Email",
                                         placeholder_text_color="#657E75",
                                         fg_color="#B6BAB3",
                                         border_color="#B6BAB3",
                                         text_color="#FFFFFF", width=300,
                                         height=40, corner_radius=70,
                                         font=("Comic Sans MS", 14))
        self.email_signup.pack(pady=(10, 10))

        #This is for the password input box in sign up
        self.password_signup = ctk.CTkEntry(content_frame, placeholder_text="Password",
                                            placeholder_text_color="#657E75",
                                            fg_color="#B6BAB3",
                                            border_color="#B6BAB3",
                                            text_color="#FFFFFF", show="*",
                                            width=300, height=40,
                                            corner_radius=70,
                                            font=("Comic Sans MS", 14))
        self.password_signup.pack(pady=(10, 10))

        #This is for the design of sign up button
        self.button_signup = ctk.CTkButton(content_frame, text="Sign Up",
                                           font=("Comic Sans MS", 16, "bold"),
                                           fg_color="#BB909B",
                                           text_color="#FFFFFF",
                                           hover_color="#EAE7E4",
                                           corner_radius=50,
                                           width=130, height=30,
                                           command=self.signup)
        self.button_signup.pack(pady=(20, 20))

    def signup(self):
        email = self.email_signup.get()
        password = self.password_signup.get()

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn.commit()
                SuccessDialog(self, "Account created successfully!")
            except sqlite3.IntegrityError:
                ErrorDialog(self, "Email already exists. Please use a different email.")


import tkinter as tk
import customtkinter as ctk
import sqlite3

class BudgetingWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("SpendSmart: Budgeting Made Simple")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(fg_color="#7F948B")

        self.init_db()
        self.load_data()

        self.left_frame = ctk.CTkFrame(self, width=250, height=500, fg_color="#7F948B", corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=False)

        self.right_frame = ctk.CTkFrame(self, width=450, height=500, fg_color="#E5CFD1", corner_radius=20)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.content_frame = ctk.CTkFrame(self.right_frame, fg_color="#E5CFD1")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label1 = ctk.CTkLabel(self.content_frame, text="Welcome", font=("Comic Sans MS", 23, "bold"), text_color="#657E75")
        self.label1.pack(pady=(50, 0))
        
        self.label2 = ctk.CTkLabel(self.content_frame, text="SpendSmart: Budgeting Made Simple", font=("Comic Sans MS", 20), text_color="#657E75")
        self.label2.pack(pady=(0, 50))

        self.content2_frame = ctk.CTkFrame(self.left_frame, fg_color="#7F948B")
        self.content2_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.button1 = ctk.CTkButton(self.content2_frame, text="Allowance", font=("Comic Sans MS", 16, "bold"),
                                     fg_color="#596F67", bg_color="#7F948B", text_color="#FFFFFF", hover_color="#EAE7E4",
                                     corner_radius=50, width=200, height=40, command=self.allowance_design_area)
        self.button1.pack(pady=(20, 10))

        self.button2 = ctk.CTkButton(self.content2_frame, text="Expenses", font=("Comic Sans MS", 16, "bold"),
                                     fg_color="#596F67", bg_color="#7F948B", text_color="#FFFFFF", hover_color="#EAE7E4",
                                     corner_radius=50, width=200, height=40, command=self.expense_design_area)
        self.button2.pack(pady=(10, 10))

        self.button3 = ctk.CTkButton(self.content2_frame, text="Savings", font=("Comic Sans MS", 16, "bold"),
                                     fg_color="#596F67", bg_color="#7F948B", text_color="#FFFFFF", hover_color="#EAE7E4",
                                     corner_radius=50, width=200, height=40, command=self.savings_area)
        self.button3.pack(pady=(10, 20))

        self.added_values_label = ctk.CTkLabel(self.right_frame, text=" ", font=("Comic Sans MS", 14), text_color="#FFFFFF")
        self.added_values_label.place(x=20, y=80)

        self.entry_value = ctk.CTkEntry(self.right_frame, width=180)
        self.entry_value.place(x=20, y=300)
        self.entry_value.place_forget()

        self.item_name = ctk.CTkEntry(self.right_frame, width=180)
        self.item_name.place(x=20, y=340)
        self.item_name.place_forget()

        self.add_button = ctk.CTkButton(self.right_frame, text="Add Expense", font=("Comic Sans MS", 16, "bold"),
                                        fg_color="#596F67", text_color="#FFFFFF", hover_color="#EAE7E4", corner_radius=50,
                                        width=200, height=40, command=self.expense_design_area)
        self.add_button.place(x=20, y=380)
        self.add_button.place_forget()

        self.expenses = []
        self.allowance = 0
        self.current_category = None

    def init_db(self):
        self.conn = sqlite3.connect("budgeting.db")
        self.cursor = self.conn.cursor()
        # Create tables if not exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS allowances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            amount REAL
        )
        """)
        self.conn.commit()

    def load_data(self):
        self.cursor.execute("SELECT amount FROM allowances ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        self.allowance = result[0] if result else 0

        self.cursor.execute("SELECT item, amount FROM expenses")
        self.expenses = [f"{row[0]}: {row[1]}" for row in self.cursor.fetchall()]

    def clear_input_area(self):
        if hasattr(self, 'values_listbox') and self.values_listbox:
            self.values_listbox.delete(0, tk.END)
        if hasattr(self, 'entry_value') and self.entry_value:
            self.entry_value.delete(0, tk.END)
        if hasattr(self, 'item_name') and self.item_name:
            self.item_name.delete(0, tk.END)

        self.label1.configure(text="")
        self.label2.configure(text="")
        self.added_values_label.configure(text="")

    #Design for allowance button
    def allowance_design_area(self):
        self.clear_input_area()
        self.current_category = 'Allowance'

        self.label1.configure(text="Allowance")
        self.label1.place(relx=0.5, rely=0.05, anchor="n")
        
        self.label2.configure(text=" Add your Allowance here")
        self.added_values_label.place_forget()

        self.values_listbox1 = tk.Listbox(self.right_frame, height=10, width=35, font=("Comic Sans MS", 12))
        self.values_listbox1.place(relx=0.5, rely=0.4, anchor="center")

        if self.allowance > 0:
            self.values_listbox1.insert(tk.END, f"Allowance: {self.allowance}")

        self.entry_value.place(x=130, y=300)
        self.entry_value.configure(state="normal")

        self.item_name.place_forget()

        self.add_button.place(x=120, y=380)
        self.add_button.configure(text="Add Allowance", command=self.allowance_area)

    #Function to add allowance in the system
    def allowance_area(self):
        value = self.entry_value.get()
        if value:
            self.allowance = float(value)
            self.cursor.execute("INSERT INTO allowances (amount) VALUES (?)", (self.allowance,))
            self.conn.commit()
            self.values_listbox1.insert(tk.END, f"Allowance: {self.allowance}")
            self.entry_value.delete(0, tk.END)

    def expense_design_area(self):
        self.clear_input_area()  # Clears the input area (removes any previous content)
        self.current_category = 'Expenses'
        
        self.label1.configure(text="Add Expense")
        self.label2.configure(text="")
        self.added_values_label.configure(text="Expenses Added:")
        
        # Create a listbox to show the expenses
        self.values_listbox2 = tk.Listbox(self.right_frame, height=10, width=35, font=("Comic Sans MS", 12))
        self.values_listbox2.place(relx=0.5, rely=0.4, anchor="center")
        
        # Display all the current expenses
        for expense in self.expenses:
            self.values_listbox2.insert(tk.END, expense)

        # Show the input fields for amount and item
        self.entry_value.place(x=130, y=300)
        self.item_name.place(x=130, y=340)
        
        
        # Make sure the input fields are enabled
        self.entry_value.configure(state="normal")
        self.item_name.configure(state="normal")

        # Show the "Add Expense" button
        self.add_button.place(x=130, y=380)
        self.add_button.configure(text="Add Expense", command=self.expense_area)

   
    #Function to add expense amount and item
    def expense_area(self):
        amount = self.entry_value.get()
        item = self.item_name.get()
        if amount and item:
            expense = f"{item}: {amount}"
            self.cursor.execute("INSERT INTO expenses (item, amount) VALUES (?, ?)", (item, float(amount)))
            self.conn.commit()
            self.expenses.append(expense)
            self.values_listbox2.insert(tk.END, expense)
            self.entry_value.delete(0, tk.END)
            self.item_name.delete(0, tk.END)

    # Design where it will show the possible savings
    def savings_area(self):
        self.clear_input_area()
        self.current_category = 'Savings'

        self.label1.configure(text="Savings Overview")
        self.label1.place(relx=0.5, rely=0.05, anchor="n")
        self.label2.configure(text=" ")
        
        self.added_values_label.configure(text="")
        self.added_values_label.place_forget()
        
        # Listbox to show savings details
        self.values_listbox3 = tk.Listbox(self.right_frame, height=10, width=35, font=("Comic Sans MS", 12))
        self.values_listbox3.place(relx=0.5, rely=0.4, anchor="center")

        # Calculate savings
        total_expenses = sum(float(exp.split(":")[1].strip()) for exp in self.expenses)
        remaining_savings = self.allowance - total_expenses

        # Display savings information
        self.values_listbox3.insert(tk.END, f"Total Expenses: {total_expenses}")
        self.values_listbox3.insert(tk.END, f"Remaining Allowance: {remaining_savings}")

        # Ensure no other widgets are interfering
        self.entry_value.place_forget()
        self.item_name.place_forget()
        self.add_button.place_forget()

        
if __name__ == "__main__":
    init_database()  
    app = FinanceApp()
    app.mainloop()

