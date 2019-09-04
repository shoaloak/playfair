#!/usr/bin/env python3
import sys
import string
import argparse
from collections import OrderedDict

def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='What to do (encrypt/decrypt)')
    parser.add_argument('file', help='The file to be encrypted')
    parser.add_argument('key', help='The key to encrypt/decrypt')
    return parser.parse_args()

def create_key(key):
    key = list(key.replace(' ', '').upper() + string.ascii_uppercase)
    
    for i, c in enumerate(list(key)):
        if c == 'J':
            key[i] = 'I'
            break

    # remove duplicates
    key = list(OrderedDict.fromkeys(key))
    return key

def read_data(filename):
    with open(filename, 'r') as f:
        try:
            data = f.read()
            data = ''.join([c for c in data if c.isalpha()])
            data = data.upper()
            return data.replace('J', 'I')
        except:
            print('Error during reading.')
            sys.exit()

def create_bigrams(data, pad):
    bigrams = []
    i = 0
    while i < len(data):
        x1 = data[i]
        x2 = pad

        if i != len(data)-1:
            x2 = data[i+1]
        if x1 == x2:
            x2 = pad
            i -= 1
        bigrams.append(x1 + x2)
        i += 2

    return bigrams

def find_location(table, char):
    for y in range(5):
        for x in range(5):
            if char == table[y][x]:
                return (y,x)

def rule_row(table, loc_a, loc_b):
    y = loc_a[0]
    xa = (loc_a[1]+1) % 5
    xb = (loc_b[1]+1) % 5
    return table[y][xa] + table[y][xb]
    
def rule_column(table, loc_a, loc_b):
    x = loc_a[1]
    ya = (loc_a[0]+1) % 5
    yb = (loc_b[0]+1) % 5
    return table[ya][x] + table[yb][x]

def rule_rectangle(table, loc_a, loc_b):
    return table[loc_a[0]][loc_b[1]] + table[loc_b[0]][loc_a[1]]

def encrypt(data, table, args):
    bigrams = create_bigrams(data, 'X')

    newgrams = []
    for bigram in bigrams:
        print(bigram)
        loc_a = find_location(table, bigram[0])
        loc_b = find_location(table, bigram[1])

        if loc_a[0] == loc_b[0]:
            newgrams.append(rule_row(table, loc_a, loc_b))
        elif loc_a[1] == loc_b[1]:
            newgrams.append(rule_column(table, loc_a, loc_b))
        else:
            newgrams.append(rule_rectangle(table, loc_a, loc_b))
        
    print('encrypted: ' + ''.join(newgrams))
    with open('enc_' + args.file, 'w') as f:
        f.write(''.join(newgrams))

def revrule_row(table, loc_a, loc_b):
    y = loc_a[0]
    xa = loc_a[1]-1 % 5
    xb = loc_b[1]-1 % 5
    if xa == -1:
        xa = 4
    if xb == -1:
        xb = 4
    return table[y][xa] + table[y][xb]

def revrule_column(table, loc_a, loc_b):
    x = loc_a[1]
    ya = loc_a[0]-1
    yb = loc_b[0]-1
    if ya == -1:
        ya = 4
    if yb == -1:
        yb = 4
    return table[ya][x] + table[yb][x]

def decrypt(data, table, args):
    bigrams = create_bigrams(data, 'X')

    newgrams = []
    for bigram in bigrams:
        loc_a = find_location(table, bigram[0])
        loc_b = find_location(table, bigram[1])

        if loc_a[0] == loc_b[0]:
            newgrams.append(revrule_row(table, loc_a, loc_b))
        elif loc_a[1] == loc_b[1]:
            newgrams.append(revrule_column(table, loc_a, loc_b))
        else:
            newgrams.append(rule_rectangle(table, loc_a, loc_b))

    print('decrypted: ' + ''.join(newgrams))
    with open('dec_' + args.file, 'w') as f:
        f.write(''.join(newgrams))

def main():
    args = check_args()

    key = create_key(args.key)
    table = [key[i:i+5] for i in range(0, 25, 5)]

    data = read_data(args.file)
    if args.action.startswith('enc'):
        encrypt(data,table, args)
    else:
        decrypt(data, table, args)

if __name__ == "__main__":
    main()
