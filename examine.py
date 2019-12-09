import sys
import os
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')
import numpy as np
import pylab as pl
import string
import time
from scipy.spatial import distance

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
    return d


def files_analyze_many(input_many_files):
    double_d = dict()
    punct = set(string.punctuation)
    digits_digit = set(string.digits)
    delim = set.union(punct, digits_digit)
    naked_words = ""
    total = 0
    print('input many files->>', input_many_files)
    for u in input_many_files:
        # print('U->', u)
        text = open(u, 'r')
        for line in text:
            line = line.strip()
            # line = line.lower()
            words = line.split(" ")
            for word in words:
                naked_words = word
                for w in naked_words:
                    if w in delim:
                        naked_words = naked_words.replace(w, '')
                if naked_words in double_d:
                    double_d[naked_words] = double_d[naked_words] + 1
                    total = total + 1
                else:
                    double_d[naked_words] = 1
                    total = total + 1
    return double_d


def histogram_result(input_parsed_file, current_file_name_passed_in):
    total_words_per_file = 0
    total_words_per_file1 = 0

    current_file_name_passed_in = current_file_name_passed_in.replace('.txt', '')
    print('CURRENT FILE PROCESSING ->', current_file_name_passed_in)

    for c in input_parsed_file.keys():
        total_words_per_file = total_words_per_file + input_parsed_file[c]

    for key, value in input_parsed_file.items():
        # print('KEY:', key, 'VALUE:', value)
        value1 = value / total_words_per_file
        input_parsed_file[key] = value1

    result = input_parsed_file
    plt.title('Discrete Distribution \\ ' + current_file_name, fontsize=12, color='b')
    plt.barh(list(input_parsed_file.keys()), sorted(list(input_parsed_file.values())), align='center', color='#fb3250')
    figure = plt.gcf()
    figure.set_size_inches(10, 30)
    plt.savefig(current_file_name_passed_in + '.png')
    plt.close()

    return result


def histogram_result_per_group(input_parsed_file):
    total_words_per_file = 0

    for c in input_parsed_file.keys():
        total_words_per_file = total_words_per_file + input_parsed_file[c]
    # print(total_words_per_file)
    for key, value in input_parsed_file.items():
        value1 = value / total_words_per_file
        input_parsed_file[key] = value1


    # print(input_parsed_file)
    # print(len(input_parsed_file.keys()))
    result = input_parsed_file
    plt.title('Discrete Distribution \\ ' + 'summary_meanDist', fontsize=12, color='b')
    plt.barh(list(input_parsed_file.keys()), sorted(list(input_parsed_file.values())), align='center', color='#FFD700')
    figure = plt.gcf()
    figure.set_size_inches(10, 30)
    plt.savefig('summary_meanDist' + '.png')
    plt.close()

    return result


"""""  
             Jensen-Shannon distance     
        JSD(P, Q) = 1/2(D(P||R) + D(Q||R))
        R = 1/2(P + Q)
"""""


# def jsd(single_file, many_files):


    # p = np.asarray(single_file.values())
    # q = np.asarray(many_files.values())
    # print('P->', p)
    # print('Q->', q)
    # # m = (p + q) / 2
    # # print('m->', m)
    # plt.scatter(single_file[0], many_files.keys())
    # figure = plt.gcf()
    # figure.set_size_inches(30, 30)
    # plt.savefig('summary' + '.png')
    # plt.close()

    # m = (p + q) / 2.0
    # js = np.sum()
    # p = np.array(single_file.values())
    # q = np.array(many_files.values())
    # p = p / np.sum(p, axis=0)
    # q = q / np.sum(q, axis=0)
    # m = (p + q) / 2.0
    #
    # js = np.sum(left, axis=0) + np.sum(right, axis=0)
    # js /= np.log(2)
    # return np.sqrt(js / 2.0)


number_of_arguments = list(sys.argv[1:])
length_list_of_arguments = len(number_of_arguments)
files_to_be_analyzed = []
file_num = 0
list_of_result_from_single_files = []
list_of_analyzed_files = ""
l1 = []
l2 = dict()

for x in number_of_arguments:
    hom_path = os.getcwd()
    print(x)
    print(os.getcwd())
    if x in os.listdir(os.getcwd()):
        os.chdir(os.path.abspath(x))
        print('Just changed dir->')
        print(os.getcwd())
        files_to_be_analyzed.clear()
        for y in os.listdir(os.getcwd()):
            if y not in files_to_be_analyzed and y.endswith('.txt'):
                files_to_be_analyzed.append(y)
            if y.endswith('.txt'):
                file_num = file_num + 1
                list_of_analyzed_files = file_analyze(y)
                list_of_result_from_single_files.append(list_of_analyzed_files)
                current_file_name = y
                l1.append(histogram_result(list_of_analyzed_files, y))

        result_many = files_analyze_many(files_to_be_analyzed)
        l2 = histogram_result_per_group(result_many)
        jsd(l1, l2)
        l1.clear()
    os.chdir(hom_path)

end = time.time()
print('TIME :^D', end - start)
