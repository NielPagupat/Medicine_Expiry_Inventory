import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import dbhandler  # Assuming dbhandler.py contains the database functions provided earlier

# Initialize the root window
root = tk.Tk()
root.title("Full-Screen App")
root.attributes("-fullscreen", True)

# Bind the Escape key to exit full-screen mode and close the app
root.bind("<Escape>", lambda e: root.destroy())

# Create the top navigation bar
top_nav = tk.Frame(root, height=50)
top_nav.pack(side="top", fill="x")

app_title = tk.Label(top_nav, text="Medicine Inventory", font=("Arial", 18), fg="black", pady=15)
app_title.pack(side="left", padx=20)

search = tk.Entry(top_nav, font=('calibre', 10, 'normal'))
search.pack(side="right", padx=20)

search_lbl = tk.Label(top_nav, text="Search", font=("Arial", 18), fg="black", pady=15)
search_lbl.pack(side="right", padx=5)

# Create a main content area below the top navigation bar
main_content = tk.Frame(root, bg="gray")
main_content.pack(expand=True, fill="both")

# Add a side content area to the left in the main content area
side_content = tk.Frame(main_content, bd=2)
side_content.pack(side="left", fill="y", padx=10, pady=10)

# Create the display frame
display = tk.Frame(main_content, bd=2, bg="white", relief="sunken")
display.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# Define frames for different views in the display area
frames = {
    "view_inventory": tk.Frame(display, bg="lightblue"),
    "add_medicine": tk.Frame(display, bg="lightgreen"),
    "edit_product": tk.Frame(display, bg="lightyellow")
}

for frame in frames.values():
    frame.place(relwidth=1, relheight=1)

# Populate Inventory List
def show_inventory():
    # Clear previous widgets in the view_inventory frame
    for widget in frames["view_inventory"].winfo_children():
        widget.destroy()
    
    # Create a container frame with a solid border
    container_frame = tk.Frame(frames["view_inventory"], bd=5, bg="white", relief="solid")
    container_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    # Fetch all medicines data from the database
    medicines = dbhandler.get_all_medicines()
    headers = ["ID", "Batch No", "Medicine Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]
    
    # Configure weights for centered alignment and even column distribution
    for i in range(len(headers)):
        container_frame.grid_columnconfigure(i, weight=1)
    
    # Create header row with larger font and centered alignment
    for col, header in enumerate(headers):
        tk.Label(container_frame, text=header, font=("Arial", 14, "bold"), borderwidth=2, 
                 relief="solid", padx=10, pady=10, anchor="center").grid(row=0, column=col, sticky="nsew")
    
    # Populate table rows with medicine data and format cells
    for row, medicine in enumerate(medicines, start=1):
        for col, value in enumerate(medicine):
            tk.Label(container_frame, text=value, font=("Arial", 12), borderwidth=1, 
                     relief="solid", padx=10, pady=5, anchor="center").grid(row=row, column=col, sticky="nsew")
    
    # Add padding around the entire frame for spacing
    container_frame.grid(padx=20, pady=20)

    # Configure the parent frame to allow the inventory frame to expand and fill the available space
    frames["view_inventory"].grid_rowconfigure(0, weight=1)
    frames["view_inventory"].grid_columnconfigure(0, weight=1)



# Add Medicine Form
def add_medicine_form():
    # Clear previous widgets in the add_medicine frame
    for widget in frames["add_medicine"].winfo_children():
        widget.destroy()
    
    # Create a container frame with a black border
    container_frame = tk.Frame(frames["add_medicine"], bd=5, bg="white", relief="solid")
    container_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Define labels including the new 'ID' field
    labels = ["ID (Barcode)", "Batch No", "Medicine Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]
    entries = []
    
    # Create a label and entry for each field
    for i, label in enumerate(labels):
        tk.Label(container_frame, text=label, font=("Arial", 14), bg="white").grid(row=i, column=0, padx=10, pady=10, sticky="w")
        
        if label == "Expiry Date":
            # Use DateEntry widget for expiry date input
            entry = DateEntry(container_frame, font=("Arial", 14), date_pattern="yyyy-mm-dd", width=25, borderwidth=2, relief="solid")
        else:
            # Use regular Entry widget for other inputs
            entry = tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid")
        
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
        entries.append(entry)
    
    # Center the container frame in the display area
    frames["add_medicine"].grid_rowconfigure(0, weight=1)
    frames["add_medicine"].grid_columnconfigure(0, weight=1)

    # Submit function to insert medicine data into the database
    def submit():
        # Retrieve values from entries
        values = [entry.get() for entry in entries]
        id_no, batch_no = values[0], values[1]  # Get ID and Batch No
        
        # Validation for ID and Batch No
        if not id_no.strip():
            messagebox.showerror("Validation Error", "ID (Barcode) cannot be empty.")
            return
        if not batch_no.strip():
            messagebox.showerror("Validation Error", "Batch No cannot be empty.")
            return

        try:
            # Insert data into the database
            dbhandler.add_medicine(*values)
            messagebox.showinfo("Success", "Medicine added successfully!")
            # Refresh inventory view
            show_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add medicine: {e}")
    
    # Add the submit button with increased font size
    tk.Button(container_frame, text="Add Medicine", command=submit, font=("Arial", 14)).grid(row=len(labels), columnspan=2, pady=20)


# Edit Medicine Form
def edit_product_form():
    # Clear previous widgets in the edit_product frame
    for widget in frames["edit_product"].winfo_children():
        widget.destroy()
    
    # Create a container frame with a black border
    container_frame = tk.Frame(frames["edit_product"], bd=5, bg="white", relief="solid")
    container_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Fields for ID and Batch No
    tk.Label(container_frame, text="Enter Medicine ID", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    id_entry = tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid")
    id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(container_frame, text="Enter Batch No", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    batch_entry = tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid")
    batch_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    # Labels and entries for medicine details
    labels = ["Medicine Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]
    entries = [tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid") for _ in labels]
    
    # Display labels and entries for medicine details
    for i, label in enumerate(labels, start=2):
        tk.Label(container_frame, text=label, font=("Arial", 14), bg="white").grid(row=i, column=0, padx=10, pady=10, sticky="w")
        entries[i-2].grid(row=i, column=1, padx=10, pady=10, sticky="w")
    
    # Function to load data into the entries
    def load_data():
        medicine_id = id_entry.get()
        batch_no = batch_entry.get()
        medicine = dbhandler.get_medicine_by_id_and_batch(medicine_id, batch_no)
        if medicine:
            for entry, value in zip(entries, medicine[2:]):  # Skip ID and Batch_No in medicine data
                entry.delete(0, tk.END)
                entry.insert(0, value)
        else:
            messagebox.showerror("Error", "Medicine ID and Batch No combination not found.")
    
    # Function to save changes to the database
    def save_changes():
        medicine_id = id_entry.get()
        batch_no = batch_entry.get()
        values = [entry.get() for entry in entries]
        try:
            dbhandler.edit_medicine(medicine_id, batch_no, *values)
            messagebox.showinfo("Success", "Medicine details updated successfully!")
            show_inventory()  # Refresh the inventory view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update medicine details: {e}")

    # Function to delete a record from the database
    def delete_record():
        medicine_id = id_entry.get()
        batch_no = batch_entry.get()
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this medicine record?"):
            try:
                dbhandler.delete_medicine(medicine_id, batch_no)
                messagebox.showinfo("Success", "Medicine record deleted successfully!")
                show_inventory()  # Refresh the inventory view
                # Clear the entries after deletion
                id_entry.delete(0, tk.END)
                batch_entry.delete(0, tk.END)
                for entry in entries:
                    entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete medicine record: {e}")

    # Load, Save, and Delete buttons
    tk.Button(container_frame, text="Load Data", command=load_data, font=("Arial", 14)).grid(row=len(labels)+2, column=0, pady=20)
    tk.Button(container_frame, text="Save Changes", command=save_changes, font=("Arial", 14)).grid(row=len(labels)+2, column=1, pady=20)
    tk.Button(container_frame, text="Delete Record", command=delete_record, font=("Arial", 14), bg="red", fg="white").grid(row=len(labels)+3, columnspan=2, pady=20)

    # Center the container frame in the display area
    frames["edit_product"].grid_rowconfigure(0, weight=1)
    frames["edit_product"].grid_columnconfigure(0, weight=1)


# Show the frame and call the appropriate function
def show_frame(frame_name, button):
    # Hide all frames initially
    for name, frame in frames.items():
        frame.place_forget()
        
    # Show only the selected frame
    frames[frame_name].place(relwidth=1, relheight=1)
    
    # Reset button colors and highlight the active button
    for btn in buttons:
        btn.config(bg="SystemButtonFace")
    button.config(bg="green")
    
    # Load specific functions for the selected frame
    if frame_name == "view_inventory":
        show_inventory()
    elif frame_name == "add_medicine":
        add_medicine_form()
    elif frame_name == "edit_product":
        edit_product_form()


# Create buttons and store references in a list for easy updating
buttons = [
    tk.Button(side_content, text="Check Inventory", font=("Arial", 14), command=lambda: show_frame("view_inventory", buttons[0])),
    tk.Button(side_content, text="Edit Product", font=("Arial", 14), command=lambda: show_frame("edit_product", buttons[1])),
    tk.Button(side_content, text="Add Medicine", font=("Arial", 14), command=lambda: show_frame("add_medicine", buttons[2]))
]

# Pack buttons in side_content with padding
for btn in buttons:
    btn.pack(pady=5, fill="x")

# Show default frame initially
show_frame("view_inventory", buttons[0])

# Run the application
root.mainloop()
