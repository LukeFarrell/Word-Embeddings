from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from collections import Counter

def Hannity_Scrape():
    wordCount = 6113674
    corpus = open('testText3.txt','a')
    driver = webdriver.Chrome("/Users/Luke.Farrell1@ibm.com/Downloads/chromedriver")
    targetPage = "http://www.foxnews.com/on-air/hannity/transcripts?page="
    driver.get(targetPage)
    time.sleep(2)
    for pageNum in range(203,295):
        for linkNum in range(1,11):
            try:
                link = driver.find_element_by_xpath('//*[@id="block-hannity-transcripts-search-list"]/ul/li[%s]/article/div[1]/a/div/img'%linkNum)
                link.click()
                soup = BeautifulSoup(driver.page_source)
                article = soup.find("div", class_= "article-text")
                text = (article.get_text()).encode('utf-8')
                wordCount += len(text.split())
                corpus.write(text)
                print "SUCCESS", pageNum, linkNum, "TOTAL WORDS: ",wordCount
            except:
                print "----ERROR AT", pageNum, linkNum, "MOVING ON----"
            try:
                driver.get(targetPage+str(pageNum))
            except:
                driver.get(targetPage+str(pageNum))

def Fox_and_Friends_Scrape():
    wordCount = 0
    corpus = open('TheFoxFive.txt','a')
    driver = webdriver.Chrome("/Users/Luke.Farrell1@ibm.com/Downloads/chromedriver")
    targetPage = "http://www.foxnews.com/on-air/the-five/transcripts?page="
    driver.get(targetPage)
    time.sleep(2)
    for pageNum in range(0,170):
        for linkNum in range(1,11):
            try:
                link = driver.find_element_by_xpath('//*[@id="block-thefive-transcripts-search-list"]/article[%s]/header/div/h2/a'%linkNum)
                link.click()
                soup = BeautifulSoup(driver.page_source)
                article = soup.find("div", class_= "article-text")
                text = (article.get_text()).encode('utf-8')
                wordCount += len(text.split())
                corpus.write(text)
                print "SUCCESS", pageNum, linkNum, "TOTAL WORDS: ",wordCount
            except:
                print "----ERROR AT", pageNum, linkNum, "MOVING ON----"
            try:
                driver.get(targetPage+str(pageNum))
            except:
                driver.get(targetPage+str(pageNum))

if __name__ == '__main__':
    Fox_and_Friends_Scrape()
