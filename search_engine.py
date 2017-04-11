import os
import math
import re

def extract_corpus(corpus_dir = "articles"):
    """
    Returns a corpus of articles from the given directory.

    Args:
        corpus_dir (str): The location of the corpus.

    Returns:
        dict: A dictionary with key = title of the article, 
		value = list of words in the article
    """
    corpus = {}
    for filename in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, filename)) as f:
            corpus[filename] = re.sub("[^\w]", " ",  f.read()).split()
    return corpus

class SearchEngine(object):
    """
    Represents an instance of a search engine. Instances of the search engine are 
    initialized with a corpus.

    Args:
        corpus (dict): A dictionary of (article title, article text) pairs.
    """
    def __init__(self, corpus):
        # The corpus of (article title, article text) pairs.
        self.corpus = corpus
        #master_dict={}
        #for article in self.corpus:
            #master_dict[article]=self.master_dict_generator()
        self.master_dict=self.master_dict_generator()
    def dict_dproduct(self, tf_dict_1, tf_dict_2):
        dproduct=0.0
        for word in tf_dict_1:
            if tf_dict_2.get(word, False):
                dproduct+=tf_dict_1[word]*tf_dict_2[word]
        return dproduct
    def dict_mag(self, tf_dict):
        mag=0.0
        for word in tf_dict:
            mag+=(tf_dict.get(word))**2
        mag=math.sqrt(mag)
        return mag
    def get_doc_dist(self, tf_dict_1, tf_dict_2):
        numerator = self.dict_dproduct(tf_dict_1,tf_dict_2)
        #print(self.dict_dproduct(tf_dict_1, tf_dict_1), self.dict_dproduct(tf_dict_2, tf_dict_2), 'hello')
        denominator = math.sqrt(self.dict_dproduct(tf_dict_1, tf_dict_1)*self.dict_dproduct(tf_dict_2, tf_dict_2))
        if denominator == 0:
            print('hello')
        #print(denominator)
        doc_dist=math.acos(numerator/denominator)        
        #print("1", tf_dict_1,tf_dict_2)
        #print("2", self.dict_dproduct(tf_dict_1,tf_dict_1))
        #print("3", self.dict_dproduct(tf_dict_2,tf_dict_2))
        return doc_dist
    def tf_dict_generator(self,d_i):
        tf_dict = {}
        d_words=self.corpus.get(d_i)
        for word in d_words:
            if tf_dict.get(word.lower(), False) is False:
                tf_dict[word.lower()]=1
            else:
                tf_dict[word.lower()]+=1
        return tf_dict
    def master_dict_generator(self): 
        master_dict={}
        for article in self.corpus:
            master_dict[article]=self.tf_dict_generator(article)
        return master_dict
    def docs_with_word(self, t):
        #master_dict=self.master_dict_generator()
        num_docs=0
        #print(dict((list(self.master_dict.items())[:1])[::-1]))
        for article in self.master_dict:
            #print(self.master_dict[article])
            #print(t)
            if t in self.master_dict[article]:
                num_docs+=1
        return num_docs     
    def tfidf_dict_generator(self,d_i):
        tfidf_dict = {}
        d_words=self.corpus.get(d_i)
        for word in d_words:
            if tfidf_dict.get(word.lower(), False) is False:
                tfidf_dict[word.lower()]=1
            else:
                tfidf_dict[word.lower()]+=1
        for word in tfidf_dict:
            num_docs=self.docs_with_word(word)
            if num_docs!=0:
                tfidf_dict[word]=tfidf_dict[word]*math.log(len(self.corpus)/num_docs)
            else:
                tfidf_dict[word]=0
        return tfidf_dict
    def tfidf_master_dict_generator(self): 
        master_dict={}
        for article in self.corpus:
            master_dict[article]=self.tfidf_dict_generator(article)
        return master_dict
    def get_relevant_articles_doc_dist(self, title, k):
        """
        Returns the articles most relevant to a given document, limited to at most
        k results. Uses the normal document distance score.

        Args:
            title (str): The title of the article being queried (assume it exists). 


        Returns:
            An array of the k most relevant (article title, document distance) pairs, ordered 
            by decreasing relevance. 

        		Specifications:
                      * Case is ignored entirely
                      * If two articles have the same distance, titles should be in alphabetical order
            """
            # TODO: Implement this for part (a)
        master_dict=self.master_dict_generator()
        #print(dict((list(master_dict.items())[:3])[::-1]))
        sorted_list={}
        for article in master_dict:
            if article!=title:
                sorted_list[article]=self.get_doc_dist(master_dict[title],master_dict[article])
        output=sorted(sorted_list.items(), key=lambda x: x[1])
        #print(output[:k])
        return output[:k]
    def get_relevant_articles_tf_idf(self, title, k):
        master_dict=self.tfidf_master_dict_generator()
        #print(dict((list(master_dict.items())[:3])[::-1]))
        sorted_list={}
        for article in master_dict:
            if article!=title:
                #print(master_dict[article])
                #print(master_dict[title])                
                sorted_list[article]=self.get_doc_dist(master_dict[title],master_dict[article])
        output=sorted(sorted_list.items(), key=lambda x: x[1])
        #print(output[:k])
        return output[:k]
    def search(self, query, k):
        """
        Returns the articles most relevant to a given query, limited to at most
        k results.

        Args:
            query (str): The query for the search engine. Doesn't contain any special characters.

            Returns:
                An array of the k best (article title, tf-idf score) pairs, ordered by decreasing score. 
                Specifications: 
                    * Only consider articles with a positive tf-idf score. 
                    * If there are fewer than k results with a positive tf-idf score, return those results.
				  If there are more, return only the k best results.
                    * If two articles have the same score, titles should be in alphabetical order
		"""
		# TODO: Implement this for part (c)
        master_dict=self.master_dict_generator()
        query_list=set(query.lower().split(" "))
        query_dict={}
        for article in master_dict:
            for word in master_dict[article]:
                if word in query_list:
                    query_dict[article]=query_dict.get(article,0)+master_dict[article][word]
        output=sorted(query_dict.items(), key=lambda x: x[1], reverse=True)
        #print(output[:k])
        return output[:k]
                    
        return []
		
if __name__ == '__main__':
	corpus = extract_corpus()
	e = SearchEngine(corpus)
	print("Welcome to 6006LE! We hope you have a wonderful experience. To exit, type 'exit.'")
	print("\nSuggested searches: the yummiest fruit in the world, child prodigy, operating system, red tree, coolest algorithm....")
	while True:
		query = input('\nEnter query here: ').strip()
		if query == "exit":
			print("Good bye!")
			break
		results = e.search(query, 5)
		if len(results) == 0:
			print("There are no results for that query. :(")
		else:
			print("Top results: ")
			for title, score in e.search(query, 5):
				print ("    - %s (score %f)" % (title, score))
