from lxml import html
import requests
import tkinter as tk
def getLastestNews(companyUrl,xpaths):

    response = requests.get(companyUrl)
    response.raise_for_status()

    tree = html.fromstring(response.content)
    story_dates = tree.xpath("//div[@class='eachStory']//div[@class='storyDate']")
    links = tree.xpath("//div[@class='eachStory']//a[@href]")

    story_dates = [date.text_content().strip() for date in story_dates]
    links = [link.get("href") for link in links]

    for index,link in enumerate(links):
        try:
            url = f"https://economictimes.indiatimes.com/{link}"
            xpath = xpaths

            response = requests.get(url)
            response.raise_for_status()

            tree = html.fromstring(response.content)
            content = tree.xpath(xpath)

            extracted_content= content[0].text_content().strip() if content else None
            if extracted_content is not None:
                return extracted_content,story_dates[index]
        except:
            pass

def CustomizegetLastestNews(companyUrl,xpaths,datepath,linkpath,news_display):

    response = requests.get(companyUrl)
    response.raise_for_status()

    tree = html.fromstring(response.content)
    story_dates = tree.xpath(datepath)
    links = tree.xpath(linkpath)

    story_dates = [date.text_content().strip() for date in story_dates]
    links = [link.get("href") for link in links]
    print(links)
    for index,link in enumerate(links):
        try:
            url = f"https://economictimes.indiatimes.com/{link}"
            xpath = xpaths

            response = requests.get(url)
            response.raise_for_status()

            tree = html.fromstring(response.content)
            content = tree.xpath(xpath)

            extracted_content= content[0].text_content().strip() if content else None

            if extracted_content is not None:
                # return extracted_content,story_dates[index]
                formatted_content = f"Date: {story_dates[index]}\n\nContent:\n{extracted_content}"
                news_display.config(state=tk.NORMAL)
                news_display.delete('1.0', tk.END)
                news_display.insert(tk.END, formatted_content)
                news_display.config(state=tk.DISABLED)
                return 
        except:
                pass
        formatted_content="404 Error"
        news_display.config(state=tk.NORMAL)
        news_display.delete('1.0', tk.END)
        news_display.insert(tk.END, formatted_content)
        news_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    link = "https://economictimes.indiatimes.com/hdfc-bank-ltd/stocksupdate/companyid-9195.cms"
    xpath="/html/body/main/div[11]/div/div[1]/div[3]/div/article/div[2]"
    getLastestNews(link,xpath)