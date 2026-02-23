import sys
import requests
from bs4 import BeautifulSoup

# Hash value
def polyhash(word):
    p = 53
    mod = 2**64
    hashvl = 0
    pow= 1
    for i in word:
        ascival= ord(i)
        hashvl = (hashvl+ ascival* pow) % mod
        pow= (pow * p) % mod
    return hashvl

# Simhash
def simhash(txt):

    txt = txt.lower()
    wordslist = []
    curwd = ""
    for i in txt:
        if i.isalnum():
            curwd +=i
        else:
            if curwd != "":
                wordslist.append(curwd)
                curwd= ""

    if curwd != "":
        wordslist.append(curwd)

    # Frequency dictionary
    word_freq = {}

    for i in wordslist:
        if i in word_freq:
            word_freq[i] += 1
        else:
            word_freq[i] = 1

    # Initializing 64-dimension vector
    vec = [0] * 64

    for w, wght in word_freq.items():
        h = polyhash(w)

        for i in range(64):
            bit = (h >> i) & 1

            if bit == 1:
                vec[i]+= wght
            else:
                vec[i] -=wght

    # Fingerprint
    simhsh = 0

    for i in range(64):
        if vec[i] >= 0:
            simhsh |= (1 << i)
    return simhsh


# Counting Common Bits
def commonbits(hsh1, hsh2):
    count = 0

    for i in range(64):
        bit1= (hsh1 >> i) & 1
        bit2= (hsh2 >> i) & 1
        if bit1 ==bit2:
            count += 1
    return count


def main():

    if len(sys.argv) != 3:
        print("Enter in the correct format")
        print("file_name.py   URL1   URL2 ")
        return
        
    url1 = sys.argv[1]
    url2 = sys.argv[2]

    try:
        page1 = requests.get(url1)
        page2 = requests.get(url2)
        if page1.status_code != 200 or page2.status_code != 200:
            print("Error in fetching one of the pages.")
            return
        # Parse HTML
        html1 = BeautifulSoup(page1.text, "html.parser") 
        html2 = BeautifulSoup(page2.text, "html.parser")
        body1 = html1.get_text(separator=" ", strip=True)
        body2 = html2.get_text(separator=" ", strip=True)
        # Simhash finding
        simhsh1 = simhash(body1)
        simhsh2 = simhash(body2)
        # Count common bits
        common_bits = commonbits(simhsh1, simhsh2)

        print("Simhash 1:", simhsh1)
        print("Simhash 2:", simhsh2)
        print("Common bits:", common_bits)

    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()