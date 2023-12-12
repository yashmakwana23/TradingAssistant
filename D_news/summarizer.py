import requests
import tkinter as tk
from tkinter import ttk
import json

def HuggingSumarization(text):

    with open('E_tokens\othertokne.json', 'r') as file:
        token_data = json.load(file)

    api_token = token_data.get("summarization")
    print("Summarization in Progess")
    
    API_TOKEN = api_token
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    payload = {
        "inputs":text
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    output = response.json()

    return(output[0]['summary_text'])

def APISumarization(content,date):

    def close_window():
        root.destroy()

    def get_formatted_news(content,date):
      
        extracted_content, date = HuggingSumarization(content),date
        formatted_content = f"Date: {date}\n\nContent:\n{extracted_content}"
        return formatted_content

    # Create the main window
    root = tk.Tk()
    root.title("Trading App")

    # Set a background color for the main window
    root.configure(bg='#f0f0f0')

    # Increase button size using style
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 16))

    # News Display with border
    news_frame = ttk.Frame(root, borderwidth=2, relief="solid", padding=(10, 10))
    news_frame.pack(expand=True, fill='both', padx=10, pady=10)

    news_text = tk.Text(news_frame, font=("Arial", 12), wrap=tk.WORD, state=tk.NORMAL)

    news_text.insert(tk.END, get_formatted_news(content,date))
    news_text.config(state=tk.DISABLED)
    news_text.pack(expand=True, fill='both')

    # Buttons with background color and padding
    button_frame = ttk.Frame(root, padding=(10, 10))
    button_frame.pack(side=tk.BOTTOM, fill='x', pady=(0, 10))

    close_button = ttk.Button(button_frame, text="Close", command=close_window)
    close_button.pack(side=tk.RIGHT, padx=10, pady=10)
    # Run the main loop
    root.mainloop()

    return None

if __name__ == "__main__":
    content="Yash Makwana asda sda sd asd sad sad sad asd gt erkyngh roteiy nwoef woe fowe fowe foeqwfowo "
    date=" asdas "
    APISumarization(content,date)