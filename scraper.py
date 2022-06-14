import sys
import pdb

from queue import PriorityQueue

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller



chromedriver_autoinstaller.install() # install and add to path
driver = webdriver.Chrome()

def main():
    # TODO: add another command line argument m that means all phrases of size 1 to m
    # will be considered (or add two (n and m) so that all phrases of size n to m are considered)

    if len(sys.argv) not in [4, 5]:
        print("\n")
        print("ERROR: incorrect input")
        sys.exit("Correct usage: python scraper.py (str)link (int)num_keywords (bool)save_or_not ((str)filetype)")

    link = sys.argv[1]
    num_keywords = sys.argv[2]
    save_to_file = sys.argv[3]  # if this is true, we will save the output to a txt file
    if len(sys.argv) == 5:
        file_type = sys.argv[4]  # this should be either txt or csv

    positive_corpus_PQ = get_corpus(link, positive=True)
    negative_corpus_PQ = get_corpus(link, positive=False)
    driver.quit()

    top_n_positive_keywords = get_top_n_keywords(positive_corpus_PQ, num_keywords)
    top_n_negative_keywords = get_top_n_keywords(negative_corpus_PQ, num_keywords)

    save_file(save_to_file, file_type, top_n_positive_keywords, top_n_negative_keywords)
    print_output(top_n_positive_keywords, top_n_negative_keywords)


def get_corpus(link, positive):
    """
    scrape positive reviews and add all words to a priority
    queue where the priority is the num of occurances (MAX-HEAP)
    return the priority queue
    """
    driver.get(link)
    occurrences_per_word = {}
    product_id = extract_product_id(link)
    breakpoint()
    # if positive get all 5 star then 4 star reviews, else get all 2 star then 1 star

    # product_id = 1612680194 # find way to extract this from the link that was passed in
    
    if positive:
        # get 5 and 4 star reviews
        five_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews#reviews-filter-bar"
        four_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=four_star&reviewerType=all_reviews#reviews-filter-bar"
        driver.get(five_star_link)
        breakpoint()
        put_reviews_on_page_into_dictionary(occurrences_per_word)  # pretty sure dict will be passed by reference, so don't need this method to return it
        driver.get(four_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)

    else:
        # get 2 and 1 star reviews
        five_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=two_star&reviewerType=all_reviews#reviews-filter-bar"
        four_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=one_star&reviewerType=all_reviews#reviews-filter-bar"
        driver.get(five_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)  # pretty sure dict will be passed by reference, so don't need this method to return it
        driver.get(four_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)

    return occurrences_per_word


def extract_product_id(link):
    product_id = ""
    for i in range(len(link)):
        try:
            if link[i] == "/" and link[i+1] == "d" and link[i+2] == "p" and link[i+3] == "/":
                i += 4
                while link[i] != "/":
                    product_id += link[i]
                    i += 1
                return product_id
        except:  # meaining we have gone out of bounds, which is only possible if an improperly formatted link was provided
            sys.exit("ERROR: Provided link is not formatted properly. Please double check that you copied the link exactly.")



def put_reviews_on_page_into_dictionary(occurrences_per_word):
    """
    Once we have navigated to a page containing all reviews of a certain star amount, this will comb through every review
    and add the words into the occurrences_per_word dictionary
    """
    pass


def get_top_n_keywords(q, num_keywords, occurrences_per_word):
    """
    should return n tuples, each containing a word and the num of times it occurs in corpus
    """
    #  loop through the items of the dictionary and add each word to a priority queue
    q = PriorityQueue()
    for word, total in occurrences_per_word.items():
        # we use -total to transform it into a max heap
        q.put((-total, word))  # total occurrences is the priority

    top_n_keywords = []
    for _ in range(num_keywords):
        next_word_and_total = q.get()
        top_n_keywords.append((next_word_and_total[1], -next_word_and_total[0]))  # tuple will be of form (word, total occurrences)
    return top_n_keywords


def print_output(top_n_positive_keywords, top_n_negative_keywords):
    """
    prints output of the program for the 
    """
    pass


def save_file(save_to_file, file_type, top_n_positive_keywords, top_n_negative_keywords):
    if not save_to_file:
        return

    if file_type in [".csv", "csv"]:
        save_output_to_csv_file(top_n_positive_keywords, top_n_negative_keywords)
    elif file_type in [".txt", "txt"]:
        save_output_to_txt_file(top_n_positive_keywords, top_n_negative_keywords)
    else:
        raise Exception("filetype should be either csv or txt")

def save_output_to_txt_file(top_n_positive_keywords, top_n_negative_keywords):
    """
    saves output to a txt file
    """
    pass

def save_output_to_csv_file(top_n_positive_keywords, top_n_negative_keywords):
    """
    saves output to a neatly organized csv file
    (organized in a manner that makes it easy to read data in for future projects)
    """
    pass


if __name__ == "__main__":
    main()