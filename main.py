import sys
import requests
from bs4 import BeautifulSoup

# writting a fucntion which will calculate evrything requred and will print only if we wanted it to , i will be using this function for handling only one link case and two link case.
def fetchdetails(url, printdetails=True):
    if not url.startswith("https://"):
        url = "https://" + url

    link = url
    fetchresponse=requests.get(link)
    if fetchresponse.status_code==200:
        if printdetails:
            print("get request run succesfully\n")
    else:
        print("get request failed to fetch data from the server\n")

    founddata=fetchresponse.text

    newsoup = BeautifulSoup(founddata,"html.parser")

    if newsoup.title:
        if printdetails:
            print("Title :" +newsoup.title.string)
            print("\n")
    else:
        if printdetails:
            print("No title present in the  html document of fetched data\n")

    if newsoup.body:
        htmlbody =  newsoup.body.get_text()
        if printdetails:
            print("Body:\n"+htmlbody)
    else:
        if printdetails:
            print("No body present in the html file of this site.")
        htmlbody=""

    alllinks = newsoup.find_all("a")

    if printdetails:
        print("\nLinks :")

    for link in alllinks:
        href=link.get("href")
        if href:
            if printdetails:
                print(href)

    if printdetails:
        print("\n")
        

if __name__=="__main__":

    if len(sys.argv)<2:
        print("No URL entered, please enter a valid link\n")
        sys.exit()

    # Only one URL entered here so i will be printing details like body, links under href tag etc.
    elif len(sys.argv)==2:
        fetchdetails(sys.argv[1], True)

    else:
        print("Too many links are enterd, please enter one")
