import sys
import os
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')
import numpy as np
import pylab as pl
import string
import time


start = time.time()


def file_analyze(input_file):
    d = dict()
    punct = set(string.punctuation)
    digits_digit = set(string.digits)
    delim = set.union(punct, digits_digit)
    naked_word = ""
    total = 0
    text = open(input_file, 'r')

    for line in text:
        line = line.strip()
        # line = line.lower()
        words = line.split(" ")

        for word in words:
            naked_word = word
            for w in naked_word:
                if w in delim:
                    naked_word = naked_word.replace(w, '')
            if naked_word in d:
                # print('NAKED WORD FINAL->', naked_word)
                d[naked_word] = d[naked_word] + 1
                total = total + 1
            else:
                d[naked_word] = 1
                total = total + 1
    # print('REAL TOTAL WORDS COUNTING->', total)
    return d






def histogram_result(input_parsed_file, current_file_name_passed_in):
    total_words_per_file = 0
    current_file_name_passed_in = current_file_name_passed_in.replace('.txt', '')
    print('CURRENT FILE PROCESSING ->', current_file_name_passed_in)

    for c in input_parsed_file.keys():
        total_words_per_file = total_words_per_file + input_parsed_file[c]
    # print(total_words_per_file)
    for key, value in input_parsed_file.items():
        value1 = value / total_words_per_file
        input_parsed_file[key] = value1
    # print(input_parsed_file)
    # print(len(input_parsed_file.keys()))

    plt.title('Discrete Distribution \\ ' + current_file_name, fontsize=12, color='b')
    plt.barh(list(input_parsed_file.keys()), sorted(list(input_parsed_file.values())), align='center', color='#fb3250')
    figure = plt.gcf()
    figure.set_size_inches(10, 30)
    plt.savefig(current_file_name_passed_in + '.png')
    plt.close()


number_of_arguments = list(sys.argv[1:])
length_list_of_arguments = len(number_of_arguments)
file_num = 0

for x in number_of_arguments:
    for dirpath, subdir, filename in os.walk(x):
        os.chdir(dirpath)

        for y in filename:
            if y.endswith('.txt'):
                file_num = file_num + 1
                list_of_analyzed_files = file_analyze(y)
                current_file_name = y
                histogram_result(list_of_analyzed_files, y)

end = time.time()
print('TIME :^D', end - start)
