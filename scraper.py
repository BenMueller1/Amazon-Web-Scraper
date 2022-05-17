import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

def main():
    # TODO: add another command line argument m that means all phrases of size 1 to m
    # will be considered (or add two (n and m) so that all phrases of size n to m are considered)

    if len(sys.argv) not in [3, 4]:
        sys.exit("Correct usage: python scraper.py (itr)link (int)num_keywords (bool)save_or_not ((str)filetype)")

    link = sys.argv[0]
    num_keywords = sys.argv[1]
    save_to_file = sys.argv[2]  # if this is true, we will save the output to a txt file
    file_type = sys.argv[3]  # this should be either txt or csv

    positive_corpus = get_positive_corpus(link)
    negative_corpus = get_negative_corpus(link)

    top_n_positive_keywords = get_top_n_keywords(positive_corpus, num_keywords)
    top_n_negative_keywords = get_top_n_keywords(negative_corpus, num_keywords)

    if save_to_file:
        if file_type in [".csv", "csv"]:
            save_output_to_csv_file(top_n_positive_keywords, top_n_negative_keywords)
        elif file_type in [".txt", "txt"]:
            save_output_to_txt_file(top_n_positive_keywords, top_n_negative_keywords)
        else:
            raise Exception("filetype should be either csv or txt")

    print_output(top_n_positive_keywords, top_n_negative_keywords)


def get_positive_corpus(link):
    """
    scrape positive reviews and add all words to a priority
    queue where the priority is the num of occurances (MAX-HEAP)
    """
    pass


def get_negative_corpus(link):
    """
    scrape negative reviews and add all words to a priority
    queue where the priority is the num of occurances (MAX-HEAP)
    """
    pass


def get_top_n_keywords(corpus, num_keywords):
    """
    should return n tuples, each containing a word and the num of times it occurs in corpus
    """
    pass


def print_output(top_n_positive_keywords, top_n_negative_keywords):
    """
    prints output of the program for the 
    """
    pass


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