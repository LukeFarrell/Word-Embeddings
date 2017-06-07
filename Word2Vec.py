import gensim
import numpy as np
import scipy as sp
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from collections import Counter
import sys

def mineText(dataSource,text_file):
    wordCount = 0
    corpus = open(text_file,'a')
    driver = webdriver.Chrome("/Users/Luke.Farrell1@ibm.com/Downloads/chromedriver")
    targetPage = "dataSource"
    driver.get(targetPage)
    time.sleep(2)
    for pageNum in range(295):
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

def text_preprocessing(text_files):
    #Convert raw text in document into [[sentence], [sentence]] array
    array = []
    for text_file in text_files:
        for line in open(text_file):
            array += re.split('[.?!]',line)
    array = np.array([s.rstrip().replace(",",'').lower().split() for s in array])
    return array

def phraseAnalysis(sentences, enabled=False, threshold=10):
    if not enabled: return sentences
    print "Applying Phrases..."
    bigrams = gensim.models.phrases.Phrases(sentences, threshold = threshold)
    bigram_enabled_sentences = bigrams[sentences]
    return bigram_enabled_sentences

def buildModel(sentences, modelName):
    model = gensim.models.Word2Vec(sentences, min_count=10, size=100, workers=8)
    print "Saving Model..."
    model.save(modelName)
    return model

def results(model):
    print model.similarity('black','white')
    print "WHITE: ", model.most_similar('white')
    print ""
    print "MUSLIM: ", model.most_similar('muslim')
    print ""
    print "CLIMATE: ", model.most_similar('climate')
    print ""
    print "OBAMA: ", model.most_similar('obama')
    print ""

    print "ANALOGY: ", model.most_similar_cosmul(positive=['islam', 'peace'], negative=['christian'])
    print ""
    print "ANALOGY: ", model.most_similar_cosmul(positive=['black', 'officer'], negative=['white'])

def main(data_files, phrase_enabled, phrase_threshold, model_name):
    t1 = time.time()
    print "----PREPROCESSING TEXT----"
    print "Extracting Data..."
    sentences = text_preprocessing(data_files)
    print "Number of sentences: ", len(sentences)
    print "Analyzing Phrases..."
    sentences = phraseAnalysis(sentences,phrase_enabled,phrase_threshold)
    print time.time()-t1
    print ""

    t2 = time.time()
    print "----TRAINING MODEL----"
    model = buildModel(sentences, model_name)
    print time.time()-t2
    print ""

    print "----RESULTS----"
    results(model)


if __name__ == '__main__':
    data_files = ['testText.txt','testText2.txt','testText3.txt']
    phrase_enabled = False
    phrase_threshold = 10
    model_name = "Hannity_Model_1"
    main(data_files, phrase_enabled, phrase_threshold, model_name)
