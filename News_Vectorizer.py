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
import matplotlib.pyplot as plt

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
    array = np.array([s.rstrip().replace(",","").replace(":","").replace("\xc2\xa0",'').lower().split() for s in array])
    return array

def phraseAnalysis(sentences, enabled=False, threshold=10):
    if not enabled: return sentences
    print "Applying Phrases..."
    bigrams = gensim.models.phrases.Phrases(sentences, threshold = threshold)
    bigram_enabled_sentences = bigrams[sentences]
    return bigram_enabled_sentences

def buildModel(sentences, modelName, load):
    if load == True: return gensim.models.Word2Vec.load(modelName)
    model = gensim.models.Word2Vec(sentences, min_count=10, size=300, workers=8)
    print "Saving Model..."
    model.save(modelName)
    return model

def loadGoogleModel():
    t3 = time.time()
    print "Loading Google Model ...."
    googleModel = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
    print "Complete", time.time()-t3, "seconds"
    return googleModel

def accuracyTest(model):
    model_acccuracy = model.accuracy('questions-words.txt')
    for testnum in range(len(model_acccuracy)):
        print "TEST", testnum, ":", float(len(model_acccuracy[testnum]['correct'])/(len(model_acccuracy[testnum]['correct']+model_acccuracy[testnum]['incorrect'])*1.0))

def dimensionAnalysis(model1, model2, v1, v2, list_of_words, list_of_sentiment):
    dim1 = (model1[v1]-model1[v2])/(np.linalg.norm(model1[v1]-model1[v2]))
    dim2 = (model2[v1]-model2[v2])/(np.linalg.norm(model2[v1]-model2[v2]))
    # dim1 = model1[v1]-model1[v2]
    # dim2 = model2[v1]-model2[v2]
    results1 = []
    results2 = []
    labels = []
    sents = []
    skipCount = 0
    for i in range(len(list_of_words)):
        try:
            word = list_of_words[i]
            sentiment = list_of_sentiment[i]
            word_vec1 = model1[word]
            word_vec2 = model2[word]
            projection_on_dim1 = np.dot(dim1, word_vec1)
            projection_on_dim2 = np.dot(dim2, word_vec2)
            results1.append(projection_on_dim1)
            results2.append(projection_on_dim2)
            labels.append(word)
            sents.append(sentiment)
        except:
            skipCount+=1
    print skipCount, " Words Omitted"
    colors = ['g' if x=='positive' else 'r' if x=='negative' else 'y' for x in sents]
    plt.scatter(results2, results1, marker = 'o', color = colors)
    # plt.xlim(-5,5)
    # plt.ylim(-5,5)
    # for word, x, y in zip(labels, results2, results1):
    #     plt.annotate(word, xy = (x,y))
    plt.show()

def results(customModel):
    # print "WHITE: ", googleModel.most_similar('white')
    print "BLACK: ", customModel.most_similar('black')
    print ""
    # print "MUSLIM: ", googleModel.most_similar('muslim')
    print "MUSLIM: ", customModel.most_similar('muslim')
    print ""
    # print "CLIMATE: ", googleModel.most_similar('climate')
    print "CLIMATE: ", customModel.most_similar('climate')
    print ""
    # print "OBAMA: ", googleModel.most_similar('obama')
    print "TRUMP: ", customModel.most_similar('trump')
    print ""
    # print "ANALOGY: ", googleModel.most_similar_cosmul(positive=['muslim', 'peace'], negative=['christian'])
    print "ANALOGY: ", customModel.most_similar_cosmul(positive=['muslim', 'peace'], negative=['christian'])
    print ""
    print "ANALOGY: ", customModel.most_similar_cosmul(positive=['france', 'london'], negative=['england'])
    print ""
    # print "ANALOGY: ", googleModel.most_similar_cosmul(positive=['black', 'officer'], negative=['white'])
    print "ANALOGY: ", customModel.most_similar_cosmul(positive=['black', 'good'], negative=['white'], topn = 30)
    print ""
    print ""
    print "ANALOGY: ", customModel.most_similar_cosmul(positive=['white', 'good'], negative=['black'], topn = 30)


def main(data_files, phrase_enabled, phrase_threshold, model_name, load_model, google_model, word_file):

    print "----PREPROCESSING TEXT----"
    t1 = time.time()
    print "Extracting Data..."
    sentences = text_preprocessing(data_files)
    print "Number of sentences: ", len(sentences)
    print "Analyzing Phrases..."
    sentences = phraseAnalysis(sentences,phrase_enabled,phrase_threshold)
    print time.time()-t1, "seconds"
    print ""

    print "----TRAINING MODEL----"
    t2 = time.time()
    print "Buidling Custom Model ..."
    customModel = buildModel(sentences, model_name, load_model)
    print "Complete", time.time()-t2, "seconds"
    print ""

    if google_model == True:
        googleModel = loadGoogleModel()

    print "----RESULTS----"
    results(customModel)
    print "Accuracy Test Custom Model..."
    accuracyTest(customModel)
    print "Accuracy Test Google Model..."
    accuracyTest(googleModel)

    print "Analyzing dimensionality..."
    list_of_words = []
    list_of_sentiment = []
    wordf = open(word_file, 'r')
    print "testing"
    for line in wordf:
        l = line.split()
        for x in l:
            if x[:5]=="word1":
                list_of_words.append(x[6:])
            if x[:13]=="priorpolarity":
                list_of_sentiment.append(x[14:])

    dimensionAnalysis(googleModel, customModel, "white", "black", list_of_words, list_of_sentiment)
    dimensionAnalysis(googleModel, customModel, "european", "african", list_of_words, list_of_sentiment)
    dimensionAnalysis(googleModel, customModel, "caucasian", "minority", list_of_words, list_of_sentiment)
    dimensionAnalysis(googleModel, customModel, "white", "latino", list_of_words, list_of_sentiment)
    dimensionAnalysis(googleModel, customModel, "muslim", "christian", list_of_words, list_of_sentiment)



if __name__ == '__main__':
    data_files = ['TheFoxFive.txt','Hannity_Corpus.txt']
    phrase_enabled = False
    phrase_threshold = 200
    model_name = "Fox_5_Model_1"
    load_model = False
    google_model = True
    word_file = "Subjectivity_Lexicon.txt"
    main(data_files, phrase_enabled, phrase_threshold, model_name, load_model, google_model, word_file)
