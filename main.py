import sys
import requests
from bs4 import BeautifulSoup


# i am writing a 64 bit hash function for a word using polynomial rolling hash function
def bithashf(word):
    p=53
    m=2**64
    hashvalue=0
    for i in range(len(word)):
        asciivalue=ord(word[i])
        hashvalue+=asciivalue*(p**i)
    return hashvalue%m


# Now writing function that will calculate simhash by taking wordfreq dicitionary as input
def calculatesimhash(wordfreq):
    array = [0]*64
    for word in wordfreq:
        hashofword=bithashf(word)
        frequency=wordfreq[word]
        for i in range(64):
            if (hashofword>>i) & 1:
                array[i]+=frequency
            else:
                array[i]-=frequency

    result=0
    for i in range(64):
        if array[i]>0:
            result = result | (1<<i)
    return result

# writting a fucntion which will calculate evrything requred and will print only if we wanted it to , i will be using this function for handling only one link case and two link case.
def fetchdetails(url, printdetails=True):

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

    # Now i am going to work on words and its frequencies
    htmlbody=htmlbody.lower()
    wordlist=[]
    currword=""
    for ch in htmlbody:
        if ch.isalnum():
            currword+=ch
        else:
            if currword!="":
                wordlist.append(currword)
                currword=""
    if currword!="":
        wordlist.append(currword)

    # creating a dictionary that will store the word as key and its frequency as value
    wordfreq={}
    for word in wordlist:
        if word in wordfreq.keys():
            wordfreq[word]+=1
        else:
            wordfreq[word]=1

    if printdetails:
        print("Printing some words and their frequencies for testing example")
        print("Word :   Frequency\n")
        for i in range(min(4,len(wordlist))):
            print(f"{wordlist[i]}    {wordfreq[wordlist[i]]}")
        print("\n")

        print("Printing some hashvalues of some words as example")
        print("Word :     Hash Value")
        for i in range(min(4,len(wordlist))):
            print(f"{wordlist[i]}    {bithashf(wordlist[i])}")

    simhashvalue = calculatesimhash(wordfreq)

    if printdetails:
        print("Simhash Value :")
        print(simhashvalue)

    return simhashvalue


if __name__=="__main__":

    if len(sys.argv)<2:
        print("No URL entered, please enter a valid link\n")
        sys.exit()

    # Only one URL entered here so i will be printing details like body, links under href tag etc.
    elif len(sys.argv)==2:
        fetchdetails(sys.argv[1], True)

    # if two links are entered then i will print only the difference between the simhash values 
    elif len(sys.argv)==3:
        simhash1 = fetchdetails(sys.argv[1], False)
        simhash2 = fetchdetails(sys.argv[2], False)

        xorvalue = simhash1 ^ simhash2
        differentbits =0
        while xorvalue:
            if xorvalue & 1==1:
                differentbits+=1
            xorvalue=xorvalue>>1    
        commonbits = 64 - differentbits

        print("Common Bits in both the simhash values is:", commonbits)

    else:
        print("Too many links are enterd, please enter either one or two links separated by tab")