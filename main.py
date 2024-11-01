import tkinter as tk

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

# Place the frames in the display area, but hide them initially
for frame in frames.values():
    frame.place(relwidth=1, relheight=1)

# Function to switch frames and highlight active button
def show_frame(frame_name, button):
    for name, frame in frames.items():
        frame.tkraise() if name == frame_name else frame.lower()
    # Update button backgrounds
    for btn in buttons:
        btn.config(bg="SystemButtonFace")
    button.config(bg="green")

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
