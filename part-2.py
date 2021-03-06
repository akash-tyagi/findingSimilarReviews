from __future__ import division
from collections import defaultdict
from operator import itemgetter
import math
import re
from utility import TextProcess
from hw1 import Hw1

class Hw2(object):
    def __init__(self):
        pass
    def get_review_tfidf_dict(self, a_document_name):
        # return a dictionary with each key,value pair as review_id and review_content
        hw1 = Hw1()
        review_id_content_dict = {}
        words_lists = []
        review_id_mapper = {}
        # create a map from Review-ID to words_lists in a review
        # store all the stemmed words_lists
        for line in open(a_document_name, 'r'):
            line = hw1.read_line(line)
            review_id_mapper[line['review_id']] = line
            review_id_content_dict[line['review_id']] = dict(hw1.unigram_count(line['text']))
            words_lists.append(Hw1.get_stemmed_words(line['text']))
            
        # get all the unique words in a list
        words = []
        i = 0
        while i < len(words_lists) :
            for word in words_lists[i] :
                words.append(word)
            i = i + 1
        #get the unique words only, using set for that
        words = list(set(words))
 
        # calculate number of reviews in which each term occur
        term_review_freq_dict = {}
        for word in words:
            i = i + 1
            term_review_freq_dict[word] = 0
            for review_id in review_id_content_dict:
                if word in review_id_content_dict[review_id].keys():
                    term_review_freq_dict[word] += 1 
        
        # calculate the TFIDF scores of each term in each review
        tfidf_dict = {}
        total_reviews = len(review_id_content_dict.keys())
        print 'Total' + str(total_reviews)
        for review_id in review_id_content_dict:
            tfidf_dict[review_id] = {}
            for word in review_id_content_dict[review_id]:
                tfidf_dict[review_id][word] = (1 + math.log10(review_id_content_dict[review_id][word])) * (math.log(total_reviews) - math.log(term_review_freq_dict[word]))
           
        i = 0
        for key in tfidf_dict.keys() :
            i = i + 1
            print str(key) + ':' + str(tfidf_dict[key])
            if i > 10:
                break
        
        return tfidf_dict, review_id_mapper
        
    def cosine_similarity_matrix(self, review_tfidf_matrix, review_id_mapper):
        # return a dictionary with each key,value pair as review_id1,[review_id2,cosine_socre]
        # calculate the normal
        print 'total pairs ' + str(len(review_tfidf_matrix.keys()) * len(review_tfidf_matrix.keys())) 
        
        #calculate the magnitude values
        magnitude_values = {}
        for reviewID in review_tfidf_matrix:
            value = 0.0
            for word in review_tfidf_matrix[reviewID]:
                value += review_tfidf_matrix[reviewID][word] * review_tfidf_matrix[reviewID][word]
            value = math.sqrt(value)
            magnitude_values[reviewID] = value
    
        #Normalize the tfidf scores in the matrix
        for reviewID in review_tfidf_matrix:
            for word in review_tfidf_matrix[reviewID]:
                if magnitude_values[reviewID] == 0:
                    continue
                review_tfidf_matrix[reviewID][word] = review_tfidf_matrix[reviewID][word]/magnitude_values[reviewID]
        
        i = 0 
        for key in review_tfidf_matrix.keys() :
            i = i + 1
            print str(key) + ':' + str(review_tfidf_matrix[key])
            if i > 10:
                break
        
        print "Done Step1: Going for Cosine Similarity Matrix"
        
        rank_dict = {}
        cosine_similarity_matrix = defaultdict(dict)
        i = 1
        for review1_id in review_tfidf_matrix:
            for review2_id in review_tfidf_matrix:
                value = 0.0
                if review1_id == review2_id: #or (review1_id, review2_id) in cosine_similarity_matrix.keys() or (review2_id,review1_id) in cosine_similarity_matrix.keys() or magnitude_values[review1_id] == 0 or magnitude_values[review2_id] == 0:
                    cosine_similarity_matrix[review1_id][review2_id] = -1
                    continue
                a = review_tfidf_matrix[review1_id].keys();
                b = review_tfidf_matrix[review2_id].keys();
                intersect = [val for val in a if val in b]
                
                for word in intersect:
                        value += review_tfidf_matrix[review1_id][word] * review_tfidf_matrix[review2_id][word]
                cosine_similarity_matrix[review1_id][review2_id] = value
                rank_dict[review1_id+' '+review2_id] = value
        print "Almost Done"
        top10 = sorted(rank_dict.iteritems(), key=itemgetter(1), reverse=1)[0:20]
        print top10

        i = 0
        last = '',''
        for a,b in top10:
            key,key1=re.split(' ',a)
            if key!=last[1] and key1!=last[0]:
                print b
                print key,key1
                last=key,key1
        return top10
    
    def get_similar_review(self, cosine_similarity_matrix):
        # return most similar review{"r_id_1":"review content", "r_id_2":"review content"}
        min_key = ()
        for review_pair in cosine_similarity_matrix:
            if min_key == ():
                min_key = review_pair
            elif cosine_similarity_matrix[review_pair] < cosine_similarity_matrix[min_key]:
                min_key = review_pair
        i = 0
        
if __name__ == '__main__':
    hw = Hw2()
    review_tfidf_dict,review_id_mapper = hw.get_review_tfidf_dict('review_KcSJUq1kwO8awZRMS6Q49g')
    cosine_similarity_matrix = hw.cosine_similarity_matrix(review_tfidf_dict, review_id_mapper)
