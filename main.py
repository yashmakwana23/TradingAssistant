import tkinter as tk
from tkinter import ttk
import threading
from D_news.newsScarping import getLastestNews
from D_news.summarizer import APISumarization
global content,date

def get_formatted_news(news_text):
    global content,date
    link = "https://economictimes.indiatimes.com/hdfc-bank-ltd/stocksupdate/companyid-9195.cms"
    xpath="""/html/body/main/div[11]/div/div[1]/div[3]/div/article/div[2]"""
    content, date = getLastestNews(link,xpath)

    formatted_content = f"Date: {date}\n\nContent:\n{content}" if content else "No news available"
    
    news_text.config(state=tk.NORMAL)
    news_text.delete('1.0', tk.END)
    news_text.insert(tk.END, formatted_content)
    news_text.config(state=tk.DISABLED)

def textSummarization():
    global content,date
    print("Intializing",content,date)
    try:
        threading.Thread(target=APISumarization,args=(content,date,)).start()

    except AssertionError:
        print("Content not ready")

def TradingTools(root):
    from A_tradingtools.tradingToolGUI import ttGui
    print("Trading Tools Opening")
    for widget in root.winfo_children():
        widget.destroy()
    ttGui(root)

def StockAnalysis(root):
    from B_stockAnalysis.stockAnalysisGUI import taGui
    print("Trade Analysis Opening")
    for widget in root.winfo_children():
        widget.destroy()
    taGui(root)

def Alerts(root):
    from C_alerts.AlertsGUI import alertGui
    print("Alerts Opening")
    for widget in root.winfo_children():
        widget.destroy()
    alertGui(root)

def mainGui(root):
    root.title("Trading Assistant")
    root.configure(bg='#f0f0f0')
    root.geometry("800x600")
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 16))

    news_frame = ttk.Frame(root, borderwidth=2, relief="solid", padding=(10, 10))
    news_frame.pack(expand=True, fill='both', padx=10, pady=10)

    news_text = tk.Text(news_frame, font=("Arial", 12), wrap=tk.WORD, state=tk.NORMAL)
    news_text.insert(tk.END, "Loading News...")
    news_text.config(state=tk.DISABLED)
    news_text.pack(expand=True, fill='both')
    threading.Thread(target=get_formatted_news, args=(news_text,)).start()

    button_frame = ttk.Frame(root, padding=(10, 10))
    button_frame.pack(side=tk.BOTTOM, fill='x', pady=(0, 10))

    tools_button = ttk.Button(button_frame, text="Trading Tools",command=lambda:TradingTools(root))
    tools_button.pack(side=tk.LEFT, padx=10, pady=10)

    analysis_button = ttk.Button(button_frame, text="Trade Analysis",command=lambda:StockAnalysis(root))
    analysis_button.pack(side=tk.LEFT, padx=10, pady=10)

    alerts_button = ttk.Button(button_frame, text="Alerts",command=lambda:Alerts(root))
    alerts_button.pack(side=tk.LEFT, padx=10, pady=10)

    summarize_button = ttk.Button(button_frame, text="Summarize", command=textSummarization)
    summarize_button.pack(side=tk.LEFT, padx=10, pady=10)

    close_button = ttk.Button(button_frame, text="Close", command=root.destroy)
    close_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

def main():
    root = tk.Tk()
    mainGui(root)
if __name__ == "__main__":
    main()
