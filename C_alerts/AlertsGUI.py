import tkinter as tk
from tkinter import ttk
import sys
import threading
import subprocess
sys.path.append(".")  


def activate_position_alert(duration_var,minutes_var,root):
    from C_alerts.PositionPnL import runsscript
    duration = duration_var.get()
    minutes = minutes_var.get()
    threading.Thread(target=runsscript,args=(int(duration),int(minutes),)).start()
    back(root)


def activate_market_price(stock_var,update_frequency_var):
    from C_alerts.qutoes import quotesscript
    selected_stock = stock_var.get()
    selected_update_frequency = update_frequency_var.get()
    if selected_stock=='HDFCBANK' and selected_update_frequency=='Live Update':
        subprocess.Popen(['python','C_alerts\HDFCBANk.py']) 
    elif selected_stock=='RELIANCE' and selected_update_frequency=='Live Update':
        subprocess.Popen(['python','C_alerts\RIL.py']) 
    elif selected_stock=='GOLD MCX' and selected_update_frequency=='Live Update':
        subprocess.Popen(['python','C_alerts\GOLD.py']) 
    else:
        threading.Thread(target=quotesscript,args=(selected_stock,)).start()


def button1_click(news_display):
    from D_news.newsScarping import CustomizegetLastestNews

    link='https://economictimes.indiatimes.com/markets/stocks/news'
    dataxpath='/html/body/main/div[11]/div/div[1]/div[3]/div/article/div[3]'
    newsdate= '//*[@id="pageContent"]/div[2]/div[1]/time'
    newlink= '//*[@id="pageContent"]/div[2]/div[1]/h3/a'
    news_display.config(state=tk.DISABLED)
    threading.Thread(target=CustomizegetLastestNews,args=(link,dataxpath,newsdate,newlink,news_display)).start()

def button2_click(news_display):
    from D_news.newsScarping import CustomizegetLastestNews
    link='https://economictimes.indiatimes.com/news/international/world-news'
    dataxpath='/html/body/main/div[11]/div/div[1]/div[3]/div/article/div[2]'
    newsdate= '//*[@id="pageContent"]/div/div[1]/time'
    newlink= '//*[@id="pageContent"]/div/div[1]/h3/a'
    news_display.config(state=tk.DISABLED)
    threading.Thread(target=CustomizegetLastestNews,args=(link,dataxpath,newsdate,newlink,news_display)).start()

def button3_click(dropdown_var,news_display):
    from D_news.newsScarping import CustomizegetLastestNews
    dataxpath="""/html/body/main/div[11]/div/div[1]/div[3]/div/article/div[2]"""
    newsdate= "//div[@class='eachStory']//div[@class='storyDate']"
    newlink= "//div[@class='eachStory']//a[@href]"

    selected_option = dropdown_var.get()
    if selected_option == "HDFCBANK":
        link='https://economictimes.indiatimes.com/hdfc-bank-ltd/stocksupdate/companyid-9195.cms'
        threading.Thread(target=CustomizegetLastestNews,args=(link,dataxpath,newsdate,newlink,news_display)).start()

    elif selected_option == "RELIANCE":
        link='https://economictimes.indiatimes.com/reliance-industries-ltd/stocksupdate/companyid-13215.cms'
        threading.Thread(target=CustomizegetLastestNews,args=(link,dataxpath,newsdate,newlink,news_display)).start()

    elif selected_option == "TATA":
        link='https://economictimes.indiatimes.com/tata-consultancy-services-ltd/stocksupdate/companyid-8345.cms'
        threading.Thread(target=CustomizegetLastestNews,args=(link,dataxpath,newsdate,newlink,news_display)).start()

def back(root):
    from main import mainGui  # Adjust the import statement
    print("Main Page Opening")
    for widget in root.winfo_children():
        widget.destroy()
    mainGui(root)

def alertGui(root):
    root.title("Alert System")

    # Social Media Alert Section
    social_media_title = tk.Label(root, text="Social Media & News Alerts", font=("Helvetica", 14, "bold"))
    social_media_title.pack(pady=5)

    social_media_frame = tk.Frame(root, bd=2, relief="solid")
    social_media_frame.pack(side="left", fill="both", expand=True)

    # Position Alert Subsection
    position_alert_frame = tk.Frame(social_media_frame)
    position_alert_frame.pack(side="top", fill="both", expand=True)

    position_alert_label = tk.Label(position_alert_frame, text="Position Alert", font=("Helvetica", 10, "bold"))
    position_alert_label.pack(pady=5)

    duration_label = tk.Label(position_alert_frame, text="Duration", font=("Helvetica", 8))
    duration_label.pack(pady=2)

    duration_var = tk.StringVar()
    duration_entry = tk.Entry(position_alert_frame, textvariable=duration_var)
    duration_entry.pack(pady=2)

    minutes_label = tk.Label(position_alert_frame, text="Minutes", font=("Helvetica", 8))
    minutes_label.pack(pady=2)

    minutes_var = tk.StringVar()
    minutes_entry = tk.Entry(position_alert_frame, textvariable=minutes_var)
    minutes_entry.pack(pady=2)

    activate_position_alert_button = tk.Button(position_alert_frame, text="Activate", command=lambda:activate_position_alert(duration_var,minutes_var,root), width=20)
    activate_position_alert_button.pack(pady=(0, 5), padx=5) 

    # Separator Line
    separator = tk.Frame(social_media_frame, height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill="x", padx=5, pady=5)

    # Market Price Subsection
    market_price_frame = tk.Frame(social_media_frame)
    market_price_frame.pack(side="top", fill="both", expand=True)

    market_price_label = tk.Label(market_price_frame, text="Market Price Alert", font=("Helvetica", 10, "bold"))
    market_price_label.pack(pady=5)

    # Stock Dropdown
    stock_var = tk.StringVar()
    stock_var.set("Select Stock")
    stock_dropdown = tk.OptionMenu(market_price_frame, stock_var, "HDFCBANK", "RELIANCE", "GOLD MCX")
    stock_dropdown.pack(pady=5, padx=5)

    # Update Frequency Dropdown
    update_frequency_var = tk.StringVar()
    update_frequency_var.set("Select Frequency")
    update_frequency_dropdown = tk.OptionMenu(market_price_frame, update_frequency_var, "Live Update", "Update")
    update_frequency_dropdown.pack(pady=5, padx=5)

    # Activate Market Price Button
    activate_market_price_button = tk.Button(market_price_frame, text="Activate", command=lambda:activate_market_price(stock_var,update_frequency_var), width=20)
    activate_market_price_button.pack(pady=(0, 5), padx=5) 

    # News Alert Section
    news_frame = tk.Frame(root, bd=2, relief="solid")
    news_frame.pack(side="left", fill="both", expand=True)

    news_label = tk.Label(news_frame, text="Latest News", font=("Helvetica", 12, "bold"))
    news_label.pack(pady=5)

    button_frame = tk.Frame(news_frame)
    button_frame.pack(side="top", pady=5)

    button1 = tk.Button(button_frame, text="Market NEWS", command=lambda:button1_click(news_display), width=20)
    button1.pack(side="left", padx=5)

    button2 = tk.Button(button_frame, text="Global News", command=lambda:button2_click(news_display), width=20)
    button2.pack(side="left", padx=5)

    # Replaced one button with a dropdown menu
    dropdown_var = tk.StringVar(news_frame)
    dropdown_var.set("Select")
    dropdown_menu = tk.OptionMenu(button_frame, dropdown_var, "HDFCBANK", "RELIANCE", "TATA")
    dropdown_menu.config(width=17)
    dropdown_menu.pack(side="left", padx=5)

    button3 = tk.Button(button_frame, text="Submit", command=lambda:button3_click(dropdown_var,news_display), width=20)
    button3.pack(side="left", padx=5)

    news_display = tk.Text(news_frame, height=20, width=70)  # Increased height and width
    news_display.pack(pady=5)

    bottom_button_frame = tk.Frame(news_frame)
    bottom_button_frame.pack(side="bottom", pady=10)

    back_button = tk.Button(bottom_button_frame, text="Back", command=lambda:back(root), width=20)
    back_button.pack(side="left", padx=5)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    alertGui(root)