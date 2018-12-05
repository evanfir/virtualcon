import requests
from bs4 import BeautifulSoup

class VirtualCrawler:
    def __init__(self, toCollege, fromCollege = "PASADENA"):
        self.__fromCollege = fromCollege
        self.__toCollege = toCollege

    def getInfo(self):        
        sourceCode = requests.get("http://web2.assist.org/web-assist/report.do?agreement=aa&reportPath=REPORT_2&reportScript=Rep2.pl&event=19&dir=1&sia=PASADENA&ria=UCB&ia=PASADENA&oia=UCB&aay=16-17&ay=16-17&dora=CS-AB")
        plainText = sourceCode.text
        soup = BeautifulSoup(plainText, "html.parser")
        iframe = soup.find('iframe')
        iframeLink = iframe['src']
        iframeSource = requests.get(iframeLink)
        iframeText = iframeSource.text
        return iframeText


def main():
    vc = VirtualCrawler("test1", "test2")
    print(vc.getInfo())

# main()