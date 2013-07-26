#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from pattern.vector import *
from pattern.web import Google, Twitter, Facebook, Bing
from epidetect import Evaluator
import nltk
from epi.models import Tweet, Location, LocationType
from pattern.en     import tag, predicative
from pattern.vector import SVM, KNN, NaiveBayes, count, shuffled, Classifier
from pattern.db  import Datasheet, pprint


class NaiveBayes:
    ''' This class implements the Naive Bayes text classifciation algorithm.
    '''
    def __init__(self):
        self.word_features_test =[]

    def buildModel(self):
        ''' Perform model building and intermittent model optimizations based on training corpus.
        '''
        global word_features_train
        global classifier
        global word_features_test

        #Sample documents obtained from corpus.
        train_tweets = []
        test_tweets = []

        pos_event_tweets_train = [('10 cases of h1n1 has been reported in saudi', 'positive'),('5 killed in saudi of h1n1', 'positive'),
        ('10 people have been said to contract h1n1', 'positive'),('25 people infected with h1n1 now in the hospital in argentina', 'positive'),
        ('traces of h1n1 recorded near turkey', 'positive'), ('private hospitals advised to close down because of the noticed h1n1', 'positive'),
         ('2 people dead from h1n1 virus', 'positive'), 
         ('H1N1 flu outbreak in northern Chile kills 11: SANTIAGO - At least 11 people have been killed in an  outbreak', 'positive'),
         (' Why H7N9 bird flu cases arose so quickly.', 'positive'),
         ('H1N1 flu outbreak in northern Chile kills 11', 'positive'),
         ('New case of h1n1 confirmed in China', 'positive')         ]

        neg_event_tweets_train = [('how to take care of h1n1', 'negative'),('h1n1 and how to prevent it', 'negative'),
        ('i\'m having flu', 'negative'),('is h1n1 a deluge in the 21st century ?', 'negative'),
        ('how are we affected by upsurge in the h1n1 recently', 'negative'), ('is this h1n1 or what ?', 'negative'),
        ('what are the symptoms of h1n1 virus', 'negative'),
        ('Thought it was flu. The doctor said no. There are giant lumps in my throat. I have to take a shitload of antibiotics. It\'s rubbish', 'negative'),
        ('Nursing Students Forced To Have Flu Shot ', 'negative'),
        ('EG Flu Tracking News Virus cuts gold kiwifruit crop', 'negative'),
        ('how can we curb the situation of h1n1 ? ', 'negative')]


        pos_event_tweets_test = [('there are 7 reported cases of h1n1 in zambia', 'positive'),('5 reported dead repeated cases of h1n1', 'positive'),
        ('h1n1 outbreak has been discovered near india', 'positive'),('50 people have died so far in middle east over outbreak of h1n1', 'positive'),
        ('detection of h1n1 in turkey', 'positive'), ('many hospitals have been closed down due to outbreak of h1n1', 'positive') ]

        neg_event_tweets_test = [('RT @trutherbot: Protip: Flu shots do not work.', 'negative'),
        ('Retweet this.... doctors are saying there might be a new flu, and that they don\'t have the vaccination..  http://t.co/Apk3QNjFs1', 'negative'),
        ('Nothing seems to be working for this flu...', 'negative'),
        ('EG Flu Tracking News 84 in state die of H1N1 in 6 months - Times of India http://t.co/GaDDrTiDNz', 'negative'),
        ('Flu season comes and goes, but #WordFlu season is here to stay! #NoYouWontGetSick #ItsGoingToBeFine #ItsAGame', 'negative'), 
        ('@Perrie_Ndublet I had the flu so I went to the loo', 'negative')]


        for (words, sentiment) in pos_event_tweets_train + neg_event_tweets_train:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
            train_tweets.append((words_filtered, sentiment))

        for (words, sentiment) in pos_event_tweets_test + neg_event_tweets_test:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
            test_tweets.append((words_filtered, sentiment))

        word_features_train = self.get_word_features(self.get_words_in_tweets(train_tweets))
        word_features_test = self.get_word_features(self.get_words_in_tweets(test_tweets))
        
        training_set = nltk.classify.apply_features(self.extract_train_features, train_tweets)
        test_set = nltk.classify.apply_features(self.extract_test_features, test_tweets)

        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)

        print classifier.show_most_informative_features(32)

        return classifier


    def get_words_in_tweets(self, documents):
        ''' Method to obtain words from documents or tweets obtained 
            from documents corpora, in order to build features from them.
            Word feature names are used to build the classifier/model.
        '''
        all_words = []
        for (words, sentiment) in documents:
            all_words.extend(words)

        return all_words

    def set_word_feature(self, word_features):
        self.word_features_test = word_features

    def get_word_features(self, wordlist):
        ''' Method for extracting word features used to build the classifier/model.
            Classifier gets better with more word features to feed into classifier.
        '''
        wordlist = nltk.FreqDist(wordlist)
        word_features = wordlist.keys()
        return word_features

    def extract_train_features(self, document):
        ''' Method for extracting word features from new documents.
        '''
        document_words = set(document)
        features = {}

        for word in word_features_train:
            features['contains(%s)' % word] = (word in document_words)
        return features    

    def extract_test_features(self, document):
        ''' Method for extracting word features from new documents.
        '''
        document_words = set(document)
        features = {}

        for word in word_features_test:
            features['contains(%s)' % word] = (word in document_words)
        return features  

    def classify(self, *args):
        ''' Performs classification of new documents.
        '''
        label = args[1].classify(self.extract_train_features(args[0].split()))

        return label

    def testModel(self):
        ''' Perform model evaluation in order to obtain F-measure, Accuracy and Precision values.
        '''


class KMeansLeaner:
    ''' This class holds method stubs and some utilities for 
        implementing the k-means algorithm.
    '''
       
    def learn(self, *args, **kwargs):
        ''' Perform learning of a Model from training data.
        '''
        pass

    def buildModel(self, *args, **kwargs):
        ''' Performs model building.
        '''
        pass


class SVMLearner:
    ''' This class holds method stubs and some utilities for 
        implementing the Support Vector Machine (SVM) algorithm.
    '''
        
    global classifier

    def testModel(self, *args):
        if args:
            classifier = Classifier.load('models/svm_model.ept')
            print "Document class is %s" % classifier.classify(Document(args[0]))

        else:
            data = Datasheet.load(os.path.join("databases","epi","svm_source.csv"))
            i = n = 0
            for label, document in data[23:34]:
                if classifier.classify(Document(document)) == (int(score) > 0):
                    i += 1
                n += 1
        
        print float(i) / n

    def buildModel(self, *args, **kwargs):
        ''' Performs model building from training using SVM algorithm.
        '''
        classifier = SVM()

        print "loading document corpus..."
        data = Datasheet.load(os.path.join("databases","epi","svm_source.csv"))
        data = shuffled(data)

        print "training svm model..."

        for label, document in data[:22]:
            classifier.train(Document(document, type=label))

        try:
            print "saving build model..."
            classifier.save('models/svm_model.ept')
        except:
            print "cannot save model file for some reason"

    def classify(self, document):

        try: 
            svm_predictions = Datasheet.load("predictions/svm.csv")
            svm_corpus = Datasheet.load("corpora/svm/svm.csv")

            index_pred = dict.fromkeys(svm_predictions.columns[0], True)
            index_corp = dict.fromkeys(svm_corpus.columns[0], True)
        except:
            svm_predictions = Datasheet()
            svm_corpus = Datasheet()
            index_pred = {}
            index_corp = {}


        classifier = Classifier.load('models/svm_model.ept')
        label = classifier.classify(Document(document))

        print "Document class is %s" % label

        id = str(hash(label + document))

        if ("1" in label):
            if len(svm_predictions) == 0 or id not in index_pred:
                svm_predictions.append([id, label, document])
                index_pred[id] = True
                
        if len(svm_corpus) == 0 or id not in index_corp:
            svm_corpus.append([id, label, document])
            index_corp[id] = True

        svm_predictions.save("predictions/svm.csv")
        svm_corpus.save("corpora/svm/svm.csv")

        print "Total predictions:", len(svm_predictions)
        print "Total documents in corpus:", len(svm_corpus)
