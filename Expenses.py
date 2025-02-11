import json
import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import Calendar

class ExpensesManager:

    # Load expenses from a JSON file
    @staticmethod
    def load_expenses():
        try:
            with open("expenses.json", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Save expenses to a JSON file
    @staticmethod
    def save_expenses(expenses):
        with open("expenses.json", 'w') as f:
            json.dump(expenses, f, indent=2)

    # Calculate the total balance from the expenses
    @staticmethod
    def sum_of_balance():
        expenses = ExpensesManager.load_expenses()
        balance = sum(expense["Price"] for expense in expenses)

        with open("Balance.json", 'w') as f:
            json.dump({"Total": balance}, f, indent=2)

        return balance

    # Show the add expenses form and hide other frames
    @staticmethod
    def show_add_expenses(event=None):
        frame_wallet.pack_forget()
        frame_total.pack_forget()
        Frame_add.pack_forget()
        button.pack_forget()
        Frame_Calender.pack_forget()

        Frame_Date.pack(pady=20)
        Frame_Reason.pack(pady=20)
        Frame_Price.pack(pady=20)
        B_okay.pack(pady=10)
        Frame_Exit.pack(pady=10)

    # Hide the add expenses form and show the main frames
    @staticmethod
    def hide_add_expenses():
        Frame_Date.pack_forget()
        Frame_Reason.pack_forget()
        Frame_Price.pack_forget()
        B_okay.pack_forget()
        F_income_or_Outcome.pack_forget()

        frame_wallet.pack(pady=60)
        frame_total.pack()
        Frame_add.pack(side=tk.RIGHT)
        button.pack(side=tk.LEFT)
        Frame_Calender.pack(side=tk.TOP)

        # for clear the Entry fields

        Entry_Date.delete(0, tk.END)
        Entry_Reason.delete(0, tk.END)
        Entry_Price.delete(0, tk.END)
        Entry_Date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))


    # Add new expense data and update the balance
    @staticmethod
    def add_expense_data(response, date, reason, price):
        expenses = ExpensesManager.load_expenses()

        price = int(price)
        if response == "outcome":
            price = -price

        data = {
            "Date": date,
            "Reason": reason,
            "Price": price,
        }
        expenses.append(data)

        ExpensesManager.save_expenses(expenses)

        total_balance = ExpensesManager.sum_of_balance()
        label_total.config(text=f"Total Balance: {total_balance}")

    # Handle the OK button click in the add expenses form
    @staticmethod
    def handle_ok():
        

        date = Entry_Date.get()
        reason = Entry_Reason.get()
        price = Entry_Price.get()

        if not date or not reason or not price:
            error_label.config(text="Please fill all fields", foreground="red")
            error_label.pack()
            return

        Frame_Date.pack_forget()
        Frame_Reason.pack_forget()
        Frame_Price.pack_forget()
        B_okay.pack_forget()
        error_label.pack_forget()
        Frame_Exit.pack_forget()

        F_income_or_Outcome.pack(pady=50)

    # Handle the Income button click in the income/outcome selection
    @staticmethod
    def handle_income():
        ExpensesManager.add_expense_data("income", Entry_Date.get(), Entry_Reason.get(), Entry_Price.get())
        ExpensesManager.hide_add_expenses()

    # Handle the Outcome button click in the income/outcome selection
    @staticmethod
    def handle_outcome():
        ExpensesManager.add_expense_data("outcome", Entry_Date.get(), Entry_Reason.get(), Entry_Price.get())
        ExpensesManager.hide_add_expenses()

    # Exit the add expenses form and show the main frames
    @staticmethod
    def exit():
        Frame_Date.pack_forget()
        Frame_Price.pack_forget()
        Frame_Reason.pack_forget()
        B_okay.pack_forget()
        Frame_Exit.pack_forget()
        Frame_Display.pack_forget()
        Frame_cal.pack_forget()
        Frame_list_calender.pack_forget()
        Check.pack_forget()
        error_label.pack_forget()

        frame_wallet.pack(pady=60)
        frame_total.pack()
        Frame_add.pack(side=tk.RIGHT)
        button.pack(side=tk.LEFT)
        Frame_Calender.pack(side=tk.TOP)

    # Check and display expenses in the scrollable text field
    @staticmethod
    def check_Expenses():
        expenses = ExpensesManager.load_expenses()

        text_display.config(state=tk.NORMAL)
        text_display.delete('1.0', tk.END)  # Clear existing text
        for expense in expenses:
            text_display.insert(tk.END, f"Date: {expense['Date']}\nReason: {expense['Reason']}\nPrice: {expense['Price']}\n\n")
        text_display.config(state=tk.DISABLED)
    
    # Show the check expenses screen and hide other frames
    @staticmethod 
    def show_check_expenses():
        frame_wallet.pack_forget()
        frame_total.pack_forget()
        Frame_add.pack_forget()
        button.pack_forget()
        Frame_Calender.pack_forget()
        
        Frame_Display.pack(pady=10)
        Frame_Exit.pack(pady=10)
        ExpensesManager.check_Expenses()
    
    # This is for the calender
    @staticmethod
    def show_calender():

        frame_wallet.pack_forget()
        frame_total.pack_forget()
        Frame_add.pack_forget()
        button.pack_forget()
        Frame_Calender.pack_forget()
        
        Frame_cal.pack(side=tk.TOP)
        Frame_Exit.pack(side='bottom',pady=10)
        Check.pack(pady=10)
    
    # This is for the check details according to the calender
    @staticmethod
    def check_according_to_the_calender():
        
        frame_wallet.pack_forget()
        frame_total.pack_forget()
        Frame_add.pack_forget()
        button.pack_forget()
        Frame_Calender.pack_forget()
        Frame_cal.pack_forget()
        Check.pack_forget()

        # Clear previous entries in the listbox
        Calender_list.delete(0, tk.END)

        # Get the selected date from the calendar
        selected_date = calender.selection_get()

        expenses = ExpensesManager.load_expenses()

        for expense in expenses:
            if expense["Date"] == selected_date.strftime("%Y-%m-%d"):
                Calender_list.insert(tk.END, f"Date: {expense['Date']}")
                Calender_list.insert(tk.END, f"Reason: {expense['Reason']}")
                Calender_list.insert(tk.END, f"Price: {expense['Price']}")
                Calender_list.insert(tk.END, "\n")
        
        Frame_list_calender.pack(pady=10)
        


        

###############################################################################################
# Function to create a round button with an image on a Canvas
def create_round_button(canvas, x, y, r, image, command):
    # Draw a circle
    circle = canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="")
    
    # Place the image in the center of the circle
    img = canvas.create_image(x, y, image=image)

    # Bind the click event to both the circle and the image
    canvas.tag_bind(circle, "<Button-1>", command)
    canvas.tag_bind(img, "<Button-1>", command)
###############################################################################################

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Expenses Counter")

# Get the user's screen width and height to center the window
user_width = root.winfo_screenwidth()
user_height = root.winfo_screenheight()
left = int(user_width / 2 - 400 / 2)
top = int(user_height / 2 - 700 / 2)

# Set the geometry of the main window
root.geometry(f"400x700+{left}+{top}")
root.resizable(False, False)
root.iconbitmap('icon/icon.ico')

###############################################################################################
# Frame to hold the wallet image
frame_wallet = ttk.Frame(root, width=400, height=300)
frame_wallet.pack(pady=60)

wallet_image = tk.PhotoImage(file="icon/wallet.png")
wallet_label = ttk.Label(frame_wallet, image=wallet_image)
wallet_label.pack()
#############################################################
# Frame to show the total balance
frame_total = ttk.Frame(root, width=400, height=20)
frame_total.pack()

# Load and display the total balance
try:
    with open("Balance.json", "r") as f:
        json_variable = json.load(f)
    balance_text = f'Total Balance: {json_variable["Total"]}'
except (FileNotFoundError, json.JSONDecodeError):
    balance_text = "Total Balance: 0"

label_total = ttk.Label(frame_total, text=balance_text, font='arial 20 bold')
label_total.pack()

###############################################################################################
# Frame to hold the add button
Frame_add = ttk.Frame(root, width=300, height=300)
Frame_add.pack(side=tk.RIGHT)

# Create a round button using Canvas
canvas = tk.Canvas(Frame_add, width=60, height=60, highlightthickness=10)
canvas.pack(side=tk.RIGHT)

# Plus image
plus_image = tk.PhotoImage(file="icon/add.png")

# Create the round button with the plus image
create_round_button(canvas, 40, 40, 25, plus_image, ExpensesManager.show_add_expenses)
###############################################################################################

# Get today's date and set it as the default value
today = datetime.date.today().strftime("%Y-%m-%d")
today_date = tk.StringVar(value=today)

# Frame and entry for the date input
Frame_Date = ttk.Frame(root, width=400, height=50)
Label_Date = ttk.Label(Frame_Date, text="Date:", font='arial 15 bold')
Entry_Date = ttk.Entry(Frame_Date, textvariable=today_date)

Label_Date.pack()
Entry_Date.pack(pady=10)

# Frame and entry for the reason input
Frame_Reason = ttk.Frame(root, width=400, height=50)
Label_Reason = ttk.Label(Frame_Reason, text="Reason:", font='arial 15 bold')
Entry_Reason = ttk.Entry(Frame_Reason)

Label_Reason.pack()
Entry_Reason.pack(pady=10)

# Frame and entry for the price input
Frame_Price = ttk.Frame(root, width=400, height=50)
Label_Price = ttk.Label(Frame_Price, text="Cost:", font='arial 15 bold')
Entry_Price = ttk.Entry(Frame_Price)

Label_Price.pack()
Entry_Price.pack(pady=10)

# Error label for validation messages
error_label = ttk.Label(root, text="", font='arial 12 bold')

# Button to submit the add expense form
B_okay = ttk.Button(root, text="Okay", command=ExpensesManager.handle_ok)

# Frame to select between income and outcome
F_income_or_Outcome = ttk.Frame(root, width=400, height=100)
L_income_or_outcome = ttk.Label(F_income_or_Outcome, text="Is this", font='arial 20 bold')

B_income = ttk.Button(F_income_or_Outcome, text="Income", command=ExpensesManager.handle_income)
B_outcome = ttk.Button(F_income_or_Outcome, text="Outcome", command=ExpensesManager.handle_outcome)

F_income_or_Outcome.pack(pady=50)
L_income_or_outcome.pack()
B_income.pack(side=tk.LEFT)
B_outcome.pack(side=tk.RIGHT)

# Hide the add expense form and income/outcome selection initially
Frame_Date.pack_forget()
Frame_Reason.pack_forget()
Frame_Price.pack_forget()
B_okay.pack_forget()
F_income_or_Outcome.pack_forget()

# Frame to hold the exit button
Frame_Exit = ttk.Frame(root, width=400, height=50)
Button_Exit = ttk.Button(Frame_Exit, text="Exit", command=ExpensesManager.exit)
Button_Exit.pack(pady=10)

###############################################################################################
# Create a scrollable text field to show expenses
Frame_Display = ttk.Frame(root, width=400, height=200)
text_display = tk.Text(Frame_Display, wrap=tk.WORD, state=tk.DISABLED, width=48, height=38)
text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(Frame_Display, orient=tk.VERTICAL, command=text_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_display.config(yscrollcommand=scrollbar.set)

# Making looks good show expenses button
search_expenses= tk.PhotoImage(file="icon/search.png")

# Button to show the check expenses screen
button = ttk.Button(root, image=search_expenses, command=ExpensesManager.show_check_expenses)
button.pack(side=tk.LEFT)
###############################################################################################

# Loding the calender image to put into the button
calender_image = tk.PhotoImage(file="icon/calender.png")
# Making Frame to hold the calender button
Frame_Calender = ttk.Frame(root,width=50,height=50)
Button_calender = ttk.Button(Frame_Calender,image=calender_image,command= ExpensesManager.show_calender)
Button_calender.pack(side=tk.TOP)
Frame_Calender.pack(side=tk.TOP)

# calender Frame
Frame_cal = ttk.Frame(root,width=200,height=150)
calender = Calendar(Frame_cal, selectmode='day', year=2024, month=6, day=19)
calender.pack(pady=10)
# Run the main event loop
##############################################################################################

# making a frame to show detail of the calender
Frame_list_calender =  ttk.Frame(root,width=400,height=400)
Calender_list = tk.Listbox(Frame_list_calender,width=300,height=300)
Calender_list.pack(pady=10)

scrollbar_calender = ttk.Scrollbar(Frame_list_calender, orient=tk.VERTICAL, command=Calender_list.yview)
scrollbar_calender.pack(side=tk.RIGHT, fill=tk.Y)

Calender_list.config(yscrollcommand=scrollbar_calender.set)

# check button
Check = ttk.Button(root,text="Check the day", command=ExpensesManager.check_according_to_the_calender)



root.mainloop()
