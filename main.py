import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
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

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=container.winfo_width())  # Set initial width of canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Expand canvas and scrollbar within the frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel scrolling to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Variable to set the warning threshold in days
days_warning = 30  # Rows will turn orange if expiry date is within this many days

# Variable to hold the sorting option
sort_option = tk.StringVar()
sort_option.set("Nearest Expiry")  # Default sorting by nearest expiry

def update_days_warning():
    """Update the days_warning variable based on user input."""
    global days_warning
    try:
        days_warning = int(days_warning_entry.get())
        show_inventory()  # Refresh the inventory display with the new days_warning
    except ValueError:
        # If the input is invalid, reset it to the previous valid value or default
        days_warning_entry.delete(0, tk.END)
        days_warning_entry.insert(0, str(days_warning))

search_query = tk.StringVar()

def show_inventory():
    # Clear previous widgets in the view_inventory frame
    for widget in frames["view_inventory"].winfo_children():
        widget.destroy()

    # Container for days warning, sorting options, and search
    options_frame = tk.Frame(frames["view_inventory"])
    options_frame.pack(pady=10)

    # Days before expiring input
    days_warning_label = tk.Label(options_frame, text="Days before expiring:", font=("Arial", 12))
    days_warning_label.grid(row=0, column=0, padx=5)

    global days_warning_entry
    days_warning_entry = tk.Entry(options_frame, font=("Arial", 12), width=5)
    days_warning_entry.insert(0, str(days_warning))  # Default value is 30
    days_warning_entry.grid(row=0, column=1, padx=5)

    # Update button
    update_button = tk.Button(options_frame, text="Update", command=update_days_warning)
    update_button.grid(row=0, column=2, padx=5)

    # Dropdown for sorting options
    sorting_options = ["ID", "Quantity", "Farthest Expiry", "Nearest Expiry"]
    sort_menu = tk.OptionMenu(options_frame, sort_option, *sorting_options, command=lambda _: show_inventory())
    sort_menu.grid(row=0, column=3, padx=5)

    # Search input
    search_label = tk.Label(options_frame, text="Search:", font=("Arial", 12))
    search_label.grid(row=0, column=4, padx=5)

    search_entry = tk.Entry(options_frame, textvariable=search_query, font=("Arial", 12), width=20)
    search_entry.grid(row=0, column=5, padx=5)
    search_entry.bind("<KeyRelease>", lambda event: show_inventory())  # Trigger search on key release

    # ScrollableFrame for the table
    scrollable_frame = ScrollableFrame(frames["view_inventory"])
    scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Container for the table content
    container_frame = tk.Frame(scrollable_frame.scrollable_frame, relief="solid", bd=1)
    container_frame.pack(fill="both", expand=True)

    # Table headers
    headers = ["ID", "Batch No", "Medicine Name", "Generic_Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]

    # Configure column width to fit the frame
    for col in range(len(headers)):
        container_frame.grid_columnconfigure(col, weight=1)  # Use weight to let all columns expand equally

    # Header row
    for col, header in enumerate(headers):
        tk.Label(container_frame, text=header, font=("Arial", 14, "bold"), borderwidth=2, 
                 relief="solid", padx=10, pady=10, anchor="center").grid(row=0, column=col, sticky="nsew")

    # Get data and sort by the selected option
    medicines = dbhandler.get_all_medicines()

    # Apply search filter
    query = search_query.get().strip().lower()
    if query:
        medicines = [medicine for medicine in medicines if query in medicine[2].lower()]  # Filter by medicine name

    # Sort by the selected option
    if sort_option.get() == "ID":
        medicines.sort(key=lambda x: int(x[0]))  # Sort by ID
    elif sort_option.get() == "Quantity":
        medicines.sort(key=lambda x: (int(x[5]) if x[6] else -1), reverse=True)  # Treat empty as -1, sort descending
    elif sort_option.get() == "Farthest Expiry":
        medicines.sort(key=lambda x: datetime.strptime(x[5], "%Y-%m-%d"), reverse=True)
    elif sort_option.get() == "Nearest Expiry":
        medicines.sort(key=lambda x: datetime.strptime(x[5], "%Y-%m-%d"))

    # Populate data rows
    current_date = datetime.now().date()
    for row, medicine in enumerate(medicines, start=1):
        expiry_date = datetime.strptime(medicine[5], "%Y-%m-%d").date()
        days_until_expiry = (expiry_date - current_date).days

        # Determine row color
        if days_until_expiry <= 0:
            row_color = "#ff9999"
        elif 0 < days_until_expiry <= days_warning:
            row_color = "#ffd078"
        else:
            row_color = "#9dff94"

        for col, value in enumerate(medicine):
            tk.Label(container_frame, text=value, font=("Arial", 12), borderwidth=1, 
                     relief="solid", padx=10, pady=5, anchor="center", bg=row_color).grid(row=row, column=col, sticky="nsew")

    # Frame stretching
    frames["view_inventory"].grid_rowconfigure(0, weight=1)
    frames["view_inventory"].grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_rowconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # Make sure the container frame fills the available space
    container_frame.grid_rowconfigure(0, weight=1)  # Ensure the header row expands

# Add Medicine Form
def add_medicine_form():
    # Clear previous widgets in the add_medicine frame
    for widget in frames["add_medicine"].winfo_children():
        widget.destroy()
    
    # Create a container frame with a black border
    container_frame = tk.Frame(frames["add_medicine"], bd=5, relief="solid")
    container_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Define labels including the new 'ID' field
    labels = ["ID (Barcode)", "Batch No", "Medicine Name", "Generic_Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]
    entries = []
    
    # Create a label and entry for each field
    for i, label in enumerate(labels):
        tk.Label(container_frame, text=label, font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=10, sticky="w")
        
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
    labels = ["Medicine Name", "Generic_Name", "Pharmaceutical Name", "Expiry Date", "Quantity"]
    entries = [tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid") for _ in labels]
    
    # Display labels and entries for medicine details
    for i, label in enumerate(labels, start=2):

        if label == "Expiry Date":
            # Use DateEntry widget for expiry date input
            entry = DateEntry(container_frame, font=("Arial", 14), date_pattern="yyyy-mm-dd", width=25, borderwidth=2, relief="solid")
        else:
            # Use regular Entry widget for other inputs
            entry = tk.Entry(container_frame, font=("Arial", 14), width=25, borderwidth=2, relief="solid")
        
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
        entries.append(entry)

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

# Function to toggle between maximize and normal window state
def toggle_maximize():
    if root.state() == "normal":
        root.state("zoomed")  # Maximize
    else:
        root.state("normal")  # Restore to normal size

# Close button
close_button = tk.Button(top_nav, text="X", font=("Arial", 14), command=root.destroy, fg="red")
close_button.pack(side="right", padx=10)

# Maximize/Restore button
maximize_button = tk.Button(top_nav, text="🗖", font=("Arial", 14), command=toggle_maximize)
maximize_button.pack(side="right", padx=10)

# Minimize button
minimize_button = tk.Button(top_nav, text="_", font=("Arial", 14), command=root.iconify)
minimize_button.pack(side="right", padx=10)

# Run the application
root.mainloop()
