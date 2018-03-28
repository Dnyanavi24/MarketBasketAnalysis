# -*- coding: utf-8 -*-

"""
@author dnyan
"""
#importing all the libraries used in the program
import requests
import csv
from collections import Counter
from operator import itemgetter
import itertools
import copy

#declaring lists and a dictionary
tupleList=[]
mainList=[]
freqList=[]
finalList=[]
dictFreq = {}

#assigning URLs used to fetch data
urlTrain="http://kevincrook.com/utd/market_basket_training.txt"
urlTest="http://kevincrook.com/utd/market_basket_test.txt"

l = requests.get(urlTrain)
m = requests.get(urlTest)

#assigning the file names
trainFilename = "market_basket_training.txt"
testFilename = "market_basket_test.txt"

#getting files to local directory
trf = open(trainFilename,"wb")
trf.write(l.content)
trf.close()
tef = open(testFilename,"wb")
tef.write(m.content)
tef.close()

#create dictionary for training data
def create_traindata_dictionary():
    with open(trainFilename, "rt", encoding="utf8") as f:
        for line in csv.reader(f):
            tupleList.append(line[1::])
        count = Counter(tuple(x) for x in iter(tupleList))
        for key,val in count.items():
            dictFreq[key] = val

#create product recommendations
def create_recommendation():
    
    with open(testFilename, "rt", encoding="utf8") as f:
        for line in csv.reader(f):
            mainList=[]
            #accessing dictionary
            for key, value in dictFreq.items():
                #checking if length of tuple and list is equal
                if len(key)==len(line):
                    if all(x in key for x in line[1::]):
                        #getting set difference
                        reco_prod = set(key) - set(line[1::])
                        freqList=[line[0],reco_prod.pop(),value]
                        mainList.append(freqList)
                        final_copy=copy.deepcopy(mainList)
            #if product is not in training dat set
            if not mainList:
                chunks = list(itertools.combinations(line[1::], len(line)-2))
                chunk_list= [list(elem) for elem in chunks]
                tempList=[]
                for line1 in chunk_list:
                    mainList=[]
                    #accessing the dictionary
                    for key, value in dictFreq.items():
                        #checking if the length of tuple and list is equal
                        if len(key)==len(line1)+1:
                            if all(x in key for x in line1):
                                #getting the set difference
                                reco_prod = set(key) - set(line1)
                                freqList=[line[0],reco_prod.pop(),value]
                                mainList.append(freqList)
                                tempList.append(freqList)
                                final_copy=copy.deepcopy(mainList)
                    #if  product in not found in the training dat set
                    if not tempList:
                        chunks_n = list(itertools.combinations(line1, len(line1)-1))
                        chunk_list_n= [list(ele) for ele in chunks_n]
                        for line2 in chunk_list_n:
                            for key, value in dictFreq.items():
                                #checking if the length of tuple and list is equal
                                if len(key)==len(line2)+1:
                                    if all(x in key for x in line2):
                                        #getting the set difference
                                        reco_prod = set(key) - set(line2)
                                        freqList=[line[0],reco_prod.pop(),value]
                                        mainList.append(freqList)
                                        final_copy=copy.deepcopy(mainList)
            #sorting list based on frequencies
            mainList = sorted(final_copy, key=itemgetter(2), reverse=True)
            finalList.append(mainList[0])
        
#calling functions to create training data and reccomendation 
create_traindata_dictionary()
create_recommendation()

#delete unwanted column
for li in finalList:
    del li[-1]
	
#write data to new file created for reccomendation               
with open("market_basket_recommendations.txt", "w+") as f:
    writer = csv.writer(f)
    writer.writerows(finalList)
