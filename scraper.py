import sys
import pdb
import nltk
import time

from queue import PriorityQueue

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from nltk.tokenize import word_tokenize

import chromedriver_autoinstaller



chromedriver_autoinstaller.install() # install and add to path
driver = webdriver.Chrome()
WAIT_TIME = 3 # MAKE THIS HIGHER if we are getting "element is not attached to page doument" error

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
    scrape positive reviews and add all words to a dictionary
    that maps each word to how many times it occurs
    """
    occurrences_per_word = {}
    product_id = extract_product_id(link)
    product_name = extract_product_name(link)

    # if positive get all 5 star then 4 star reviews, else get all 2 star then 1 star
    if positive:
        # get 5 and 4 star reviews
        five_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews#reviews-filter-bar"
        four_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=four_star&reviewerType=all_reviews#reviews-filter-bar"
        driver.get(five_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)  # pretty sure dict will be passed by reference, so don't need this method to return it
        breakpoint()
        driver.get(four_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)
        

    else:
        # get 2 and 1 star reviews
        two_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=two_star&reviewerType=all_reviews#reviews-filter-bar"
        one_star_link = f"https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_5?ie=UTF8&filterByStar=one_star&reviewerType=all_reviews#reviews-filter-bar"
        driver.get(two_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)  # pretty sure dict will be passed by reference, so don't need this method to return it
        driver.get(one_star_link)
        put_reviews_on_page_into_dictionary(occurrences_per_word)

    # remove things like punctuation and function words (find a library of function words and punctuation online and put it into a set)
    occurrences_per_word = purge(occurrences_per_word)


    return occurrences_per_word


def put_reviews_on_page_into_dictionary(occurrences_per_word):
    """
    Once we have navigated to a page containing all reviews of a certain star amount, this will comb through every review
    and add the words into the occurrences_per_word dictionary
    """
    finished = False
    while not finished:
        time.sleep(WAIT_TIME)  # allow page to load

        # if reviews are not in english, translate them
        try:
            driver.find_element(
                By.LINK_TEXT,
                "Translate all reviews to English"
            ).click()
            time.sleep(WAIT_TIME)
        except:
            pass

        reviews_container = driver.find_element(
            By.ID,
            "cm_cr-review_list"
        )
        reviews = reviews_container.find_elements(
                By.XPATH,
                "./*"   # this finds all DIRECT children
        )

        # need to trim off each item in review that doesn't have the class named "review" (take out everything that isn't actually a review)
        r = []
        for review in reviews:
            if " review " in review.get_attribute('class'):
                r.append(review)
        reviews = r

        # get text from the 10 interviews on the page
        for review in reviews:
            text = review.find_element(
                By.CSS_SELECTOR,
                "div > div > div > span > span"
            ).text
            occurrences_per_word = put_tokens_into_dict(text, occurrences_per_word)

        
        # now click the next page button if it shows up, else we have finished getting the corpus and can end (set finished = True)
        pagination_bar = driver.find_element(
            By.ID,
            "cm_cr-pagination_bar"
        )
        next_page_button = pagination_bar.find_elements(
            By.CSS_SELECTOR,
            "ul > li"
        )[1]
        # check if we are currently on the last page and end if so
        if "a-disabled" in next_page_button.get_attribute('class'):
            finished = True
            break
        next_page_button.click()

    return occurrences_per_word

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

def purge(occurrences_per_word):
    """
    get rid of punctuation and function words
    """
    pass


def print_output(top_n_positive_keywords, top_n_negative_keywords):
    """
    prints output of the program
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


def extract_product_name(link):
    product_name = ""
    for i in range(len(link)):
        try:
            if link[i:i+15] == "www.amazon.com/":
                i += 15
                while link[i] != "/":
                    product_name += link[i]
                    i += 1
                return product_name
        except:  # meaining we have gone out of bounds, which is only possible if an improperly formatted link was provided
            sys.exit("ERROR: Provided link is not formatted properly. Please double check that you copied the link exactly.")


def put_tokens_into_dict(text, occurrences_per_word):
    try:
        words = word_tokenize(text)
    except:  # download the needed tokenizer if it is not found on machine
        nltk.download('punkt')
        words = word_tokenize(text)

    for word in words:
        if word in occurrences_per_word.keys():
            occurrences_per_word[word] += 1
        else:
            occurrences_per_word[word] = 1
    return occurrences_per_word

if __name__ == "__main__":
    main()