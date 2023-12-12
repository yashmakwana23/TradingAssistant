import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import threading
sys.path.append(".")

def open_trailing_stoploss(section_frame3):

    # Create a frame for the input fields
    input_frame = ttk.Frame(section_frame3)
    input_frame.pack(pady=(10, 5))

    # Create labels and entry fields
    label1 = ttk.Label(input_frame, text="StopLoss:")
    label1.grid(row=0, column=0, padx=(0, 5))
    entry1 = ttk.Entry(input_frame)
    entry1.grid(row=0, column=1, padx=(0, 10))

    label2 = ttk.Label(input_frame, text="Enter Position:")
    label2.grid(row=1, column=0, padx=(0, 5))
    entry2 = ttk.Entry(input_frame)
    entry2.grid(row=1, column=1, padx=(0, 10))

    # Create the "Setup" button
    trailing_stoploss_setup_button = ttk.Button(input_frame, text="Start", command=lambda: setup_trailing_stoploss(entry1.get(), entry2.get()))
    trailing_stoploss_setup_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

def setup_trailing_stoploss(input1, input2):
    from A_tradingtools.TrailingStopLoss import AUTOTSL
    print("Input 1:", input1)
    print("Input 2:", input2)
    threading.Thread(target=AUTOTSL,args=(input1,input2,)).start()


def buy_execute_clone_trading_action(clone_trading_var):
    from A_tradingtools.clonetrading import call_button_clicked
    selected_option = clone_trading_var.get()
    if selected_option == "R POWER":
        print('here')
        call_button_clicked()
    else:
        print("Please select another stock")


def sell_execute_clone_trading_action(clone_trading_var):
    from A_tradingtools.clonetrading import put_button_clicked
    selected_option = clone_trading_var.get()
    if selected_option == "R POWER":
        put_button_clicked()
    else:
        print("Please select another stock")

def start_algo_trading():
    subprocess.Popen(['python','A_tradingtools\Strategy.py']) 

def quick_trailing_stoploss():
    subprocess.Popen(['python','A_tradingtools\quickTrailingSL.py']) 



def go_back(root):  
    from main import mainGui  # Adjust the import statement
    print("Main Page Opening")
    for widget in root.winfo_children():
        widget.destroy()
    mainGui(root)


def ttGui(root):
    # root = tk.Tk()
    root.title("Trading Tools")
    root.geometry("800x300")

    # # Set a background color for the main window
    root.configure(bg='#f0f0f0')

    # Define section frames
    section_frame1 = ttk.Frame(root, borderwidth=2, relief="solid")
    section_frame2 = ttk.Frame(root, borderwidth=2, relief="solid")
    section_frame3 = ttk.Frame(root, borderwidth=2, relief="solid")

    # Add section headings
    heading1 = ttk.Label(section_frame1, text="Clone Trading", font=("Arial", 16, "bold"))
    heading1.pack(pady=(10, 5))
    heading2 = ttk.Label(section_frame2, text="Algo Trading", font=("Arial", 16, "bold"))
    heading2.pack(pady=(10, 5))
    heading3 = ttk.Label(section_frame3, text="Trailing Stoploss", font=("Arial", 16, "bold"))
    heading3.pack(pady=(10, 5))

    # Add dropdowns for each section
    clone_trading_options = ["R POWER", "Stock 2", "Stock 3"]
    clone_trading_var = tk.StringVar()
    clone_trading_dropdown = ttk.Combobox(section_frame1, values=clone_trading_options, textvariable=clone_trading_var)
    clone_trading_dropdown.pack(pady=(5, 10))

    algo_trading_options = ["SMA Strategy ", "Strategy 2", "Strategy 3"]
    algo_trading_var = tk.StringVar()
    algo_trading_dropdown = ttk.Combobox(section_frame2, values=algo_trading_options, textvariable=algo_trading_var)
    algo_trading_dropdown.pack(pady=(5, 10))

    # Add buttons for each section
    clone_trading_button_buy = ttk.Button(section_frame1, text="Buy", command=lambda:buy_execute_clone_trading_action(clone_trading_var))
    clone_trading_button_sell = ttk.Button(section_frame1, text="Sell", command=lambda:sell_execute_clone_trading_action(clone_trading_var))

    clone_trading_button_buy.pack(pady=(5, 5))
    clone_trading_button_sell.pack(pady=(5, 5))


    algo_trading_button_start = ttk.Button(section_frame2, text="Start", command=start_algo_trading)
    # algo_trading_button_stop = ttk.Button(section_frame2, text="Stop", command=stop_algo_trading)

    algo_trading_button_start.pack(pady=(5, 5))
    # algo_trading_button_stop.pack(pady=(5, 5))

    trailing_stoploss_setup_button = ttk.Button(section_frame3, text="Quick Start", command=quick_trailing_stoploss)
    trailing_stoploss_setup_button.pack(pady=(5, 10))
    Custom_trailing_stoploss_setup_button = ttk.Button(section_frame3, text="Customization", command=lambda:open_trailing_stoploss(section_frame3))
    Custom_trailing_stoploss_setup_button.pack(pady=(5, 10))

    back_button = ttk.Button(root, text="Back", command=lambda:go_back(root))
    back_button.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky="nsew")

    # Define positions for section frames
    section_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    section_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    section_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # Configure grid weights for equal sizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    ttGui(root)