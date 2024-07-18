import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser
import subprocess

# Get the directory where the script is located
base_path = os.path.dirname(os.path.abspath(__file__))

# Function to open instructions file
def open_instructions():
    instructions_path = os.path.join(base_path, 'instructions.html')
    try:
        webbrowser.open(instructions_path, new=2)  # Opens in a new tab if possible
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")

# Function to read the CSV file and process the data
def process_milesplit_csv(input_csv):
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    # Combine FName and LName to form the Athlete column
    df['Name'] = df['FName'] + ' ' + df['LName']

    # Sort by Team first and then by last name (portion after the last space in Name)
    df['Last Name'] = df['Name'].apply(lambda x: x.split()[-1])
    df = df.sort_values(by=['Team', 'Last Name'])

    # Create separate DataFrames for boys (males) and girls (females)
    boys_df = df[df['Gender'] == 'M'][['Team', 'Name', 'Grade']]
    girls_df = df[df['Gender'] == 'F'][['Team', 'Name', 'Grade']]

    return boys_df, girls_df

# Function to save the processed data to CSV and TXT files
def save_to_files(boys_df, girls_df):
    # Get the path to the Desktop
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # Save to CSV files
    boys_df.to_csv(os.path.join(desktop_path, "boys_output.csv"), index=False)
    girls_df.to_csv(os.path.join(desktop_path, "girls_output.csv"), index=False)

    # Save to TXT files
    boys_df.to_csv(os.path.join(desktop_path, "boys_output.txt"), columns=['Team', 'Name', 'Grade'], index=False, sep='\t')
    girls_df.to_csv(os.path.join(desktop_path, "girls_output.txt"), columns=['Team', 'Name', 'Grade'], index=False, sep='\t')

# Function to browse and select the CSV file
def browse_csv_file():
    global input_csv
    input_csv = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if input_csv:
        messagebox.showinfo("File Selected", f"Selected file: {input_csv}")

# Function to convert the CSV file to the desired CSV format and save to files
def convert_csv_to_files():
    if not input_csv:
        messagebox.showerror("Error", "No CSV file selected.")
        return
    
    # Process the input CSV
    boys_df, girls_df = process_milesplit_csv(input_csv)

    # Save the results to CSV and TXT files
    save_to_files(boys_df, girls_df)

    messagebox.showinfo("Success", "Processed results saved to boys_output.csv, girls_output.csv, boys_output.txt, and girls_output.txt")

# Function to open the CC_Scores file
def open_cc_scores():
    cc_scores_path = os.path.join(base_path, 'CC_Scorer.xls')
    try:
        if os.name == 'nt':  # Windows
            os.startfile(cc_scores_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.run(['open', cc_scores_path])
        else:
            messagebox.showerror("Error", "Unsupported OS")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")

# Function to open XNoteStopWatch
def open_xnsw():
    xnsw_path = os.path.join(base_path, 'xnsw.exe')
    try:
        subprocess.Popen(xnsw_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open XNoteStopWatch: {e}")

# Create the main GUI
def create_gui():
    root = tk.Tk()
    root.title("Milesplit CSV to CSV | TXT Converter")

    tk.Label(root, text="Milesplit CSV to CSV | TXT Converter", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Instructions", command=open_instructions).pack(pady=5)
    tk.Button(root, text="Browse Milesplit CSV File", command=browse_csv_file).pack(pady=5)
    tk.Button(root, text="Convert to Boys and Girls CSV | TXT files", command=convert_csv_to_files).pack(pady=5)
    tk.Button(root, text="Open CC_Scorer", command=open_cc_scores).pack(pady=5)
    tk.Button(root, text="Open XNoteStopWatch", command=open_xnsw).pack(pady=5)
    tk.Button(root, text="Quit", command=root.quit).pack(pady=20)

    root.mainloop()

# Global variable to store the input CSV file path
input_csv = None

# Run the GUI
create_gui()
