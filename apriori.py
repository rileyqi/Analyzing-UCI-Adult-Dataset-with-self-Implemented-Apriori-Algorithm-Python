import sys
from collections import defaultdict
from optparse import OptionParser
import csv

def has_infreq_subset(c, Lk_1):
    for item in c:
        k_1_set = c - frozenset([item])
        if((k_1_set in Lk_1)==False):
            return True
    return False

def apriori_gen(Lk_1, k):
    Ck = []
    for i in Lk_1:
        for j in Lk_1:
            c = i.union(j)
            if(len(c) == k):
                if(has_infreq_subset(c,Lk_1)==False):
                    Ck.append(c)
    remove_duplicate = set(Ck)

    return list(remove_duplicate)


def find_freq_1_itemsets(D, min_sup):
    S = []
    for row in D:
        S.append(set(row))#remove duplicate

    item_count = defaultdict(int)
    for row in S:
        for item in row:
            item_count[item]+=1
    length = len(D)

    L = []
    for key, value in item_count.items():
        I = []
        if float(value)/length >= min_sup:
            print(key)
            print(float(value)/length)
            I.append(key)
            L.append(frozenset(I))
    return L


def apriori(database, min_sup):
    D = []
    for row in database:
        D.append(row)

    S = []
    for row in D:
        S.append(frozenset(row))

    L = []
    L.append(frozenset())#L[0]
    L.append(find_freq_1_itemsets(D, min_sup))#L[1]
    k = 2
    C = []
    C.append(frozenset())#C[0]
    C.append(frozenset())#C[1]
    number_of_transaction = len(S)
    while(len(L[k-1])!=0):
        C.append(apriori_gen(L[k-1],k))#C[k]
        c_count = defaultdict(int)
        for c in C[k]:
            for s in S:
                if c.issubset(s):
                    c_count[c] += 1
        I = []
        for key, value in c_count.items():
            if float(value)/number_of_transaction >= min_sup:
                print(key)
                print(float(value)/number_of_transaction)
                I.append(key)
        L.append(frozenset(I))#L[k]
        k += 1
    return L


def main():
    opt_parser = OptionParser()
    opt_parser.add_option(
        '-f',
        '--inputFile',
        dest='input',
        help='filename containing csv',
        default=None)
    opt_parser.add_option(
        '-s',
        '--minSupport',
        dest='minS',
        help='minimum support value',
        default=0.15,
        type='float')
    (options, args) = opt_parser.parse_args()
    infile = open(options.input, 'r')
    min_sup = options.minS
    csv_infile = csv.reader(infile)
    L = apriori(csv_infile, min_sup)
    print(L)

if __name__ == '__main__': main()
