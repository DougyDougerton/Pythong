# expense_tracker.py-pie

import csv 
import os 
import tkinter as tk  
from tkinter import messagebox, ttk 

# Initialize an empty list to store expenses
expenses = []

# Function to load expenses from a CSV file
def load_expenses():
    if os.path.exists("expenses.csv"):
        with open("expenses.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    "category": row["category"],
                    "amount": float(row["amount"]),
                    "description": row["description"]
                })
        print("Expenses loaded successfully!\n")
    else:
        print("No saved expenses found.🤷\n")

# Function to save expenses to a CSV file.
def save_expenses():
    with open("expenses.csv", mode="w", newline="") as file:
        fieldnames = ["category", "amount", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # Write header only once at the start
        for expense in expenses:
            writer.writerow(expense)

# Function to update the expense list in the UI
def update_expense_list():
    expense_list.delete(*expense_list.get_children())
    for i, expense in enumerate(expenses):
        expense_list.insert("", "end", iid=i, values=(expense['category'], expense['amount'], expense['description']))

# Function to add an expense 😐
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    
    if category and amount and description:
        try:
            expenses.append({"category": category, "amount": float(amount), "description": description})
            update_expense_list()
            save_expenses()
            category_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number.")
    else:
        messagebox.showwarning("input Error", "Please fill in all of the fields.")
    
# Function to edit an expense
def edit_expense():
    try:
        selected_item = expense_list.selection()[0]
        index = int(selected_item)
        
        # Get updated values from the entry fields
        updated_category = category_entry.get()
        updated_amount = amount_entry.get()
        updated_description = description_entry.get()
        
        if updated_category and updated_amount and updated_description:           
            expenses[index] = {
            "category": updated_category,
            "amount": float(updated_amount),
            "description": updated_description
        }
            update_expense_list()
            save_expenses()
        else:
            messagebox.showwarning("Input Error", "Please fill in the fields.")
    except (IndexError, ValueError):
        messagebox.showwarning("Selection Error", "Please select an existing expense to update.")
    
    # Function to delete an expense
def delete_expense():
    try:
        selected_item = expense_list.selection()[0]
        index = int(selected_item)
        del expenses[index]
        update_expense_list()
        save_expenses()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")



    
 # Function to display all expenses 💸 FLY MONEY FLY!!!
def view_expenses():
    #Create a new window for viewing expenses
    window = tk.Toplevel()
    window.title("View Expenses")
    
    # Create a Treeview widget to display expenses
    tree = ttk.Treeview(window, columns=("Category", "Amount", "Description"), show="headings")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")
    
    # Add expenses to the Treeview
    for expense in expenses:
        tree.insert("", "end", values=(expense["category"], expense["amount"], expense["description"]))
    
    tree.pack(fill="both", expand=True)
    
# MaIn PrOgRaM lOoP 
def main():
    global root, category_entry, amount_entry, description_entry, expense_list
    root = tk.Tk()
    root.title("Expense Tracker")
    
    load_expenses() # Load any saved expenses at the start
    
    # Category entry
    tk.Label(root, text="Category:").pack()
    category_entry = tk.Entry(root)
    category_entry.pack()
    
    # Amount entry
    tk.Label(root, text="Amount").pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack()
    
    # Description entry
    tk.Label(root, text="Description").pack()
    description_entry = tk.Entry(root)
    description_entry.pack()
    
    # Create buttons
    add_button = tk.Button(root, text="Add expense", command=add_expense)
    add_button.pack(pady=5)
    
    edit_button = tk.Button(root, text="Edit Expense", command=edit_expense)
    edit_button.pack(pady=5)
    
    delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
    delete_button.pack(pady=5)
    
    view_button = tk.Button(root, text="View All Expenses", command=view_expenses)
    view_button.pack(pady=5)
    

    
    # Expense list
    expense_list = ttk.Treeview(root, columns=("Category", "Amount", "Description"), show="headings")
    expense_list.heading("Category", text="Category")
    expense_list.heading("Amount", text="Amount")
    expense_list.heading("Description", text="Description")
    expense_list.pack(pady=10)
    
    update_expense_list()
    
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    # Start the GUI event loop
    root.mainloop()
    
if __name__ == "__main__":
    main()