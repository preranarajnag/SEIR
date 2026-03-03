import sys
import requests
from bs4 import BeautifulSoup


def main():    
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        print("Enter in the correct format!")
        print("file_name.py  URL")
        return

    try:
        sendRequest = requests.get(url)

        if sendRequest.status_code == 200:
            print("Successfully page is fetched")

            HTMLcontent = BeautifulSoup(sendRequest.text, "html.parser")

            if HTMLcontent.title is not None and HTMLcontent.title.string is not None:
                print(HTMLcontent.title.string.strip())
            else:
                print("No Titles in the page")

            bdytxt = HTMLcontent.get_text(separator=" ", strip=True)

            if bdytxt:
                print(bdytxt)
            else:
                print("No Body Content in the page")
                return

            lks = HTMLcontent.find_all("a")

            if len(lks) > 0:
                for link in lks:
                    if link.get("href") is not None:
                        print(link.get("href"))
            else:
                print("No Links Found in the page")

        else:
            print("Failed to fetch page")

    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()
