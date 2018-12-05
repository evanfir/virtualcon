import requests
from bs4 import BeautifulSoup

class VirtualCrawler:
    def __init__(self, toCollege, fromCollege = "PASADENA"):
        self.__fromCollege = fromCollege
        if toCollege == "UCB": #UC Berkeley
            self.__toCollege = "UCB"
            self.__major = "CS-AB"
        if toCollege == "UCD": #UC Davis
            self.__toCollege = "UCD"
            self.__major = "COMP.SCI.B.S."
        if toCollege == "UCLA": #UC Los Angeles
            self.__toCollege = "UCLA"
            self.__major = "COMP+SCI"
        if toCollege == "UCI": #UC Irvine
            self.__toCollege = "UCI"
            self.__major = "CS"

    ## getiFrameLink retrieve the iframe link from the assist.org page
    # @return: link to the iFrame
    def getiFrameLink(self):     
        url = "http://web2.assist.org/web-assist/report.do?agreement=aa&reportPath=REPORT_2&reportScript=Rep2.pl&event=19&dir=1&sia=PASADENA&ria=" + self.__toCollege + "&ia=PASADENA&oia=" + self.__toCollege + "&aay=16-17&ay=16-17&dora=" + self.__major  
        sourceCode = requests.get(url)
        plainText = sourceCode.text
        soup = BeautifulSoup(plainText, "html.parser")
        iframe = soup.find('iframe')
        iframeLink = iframe['src']
        # iframeSource = requests.get(iframeLink)
        # iframeText = iframeSource.text
        return iframeLink


def main():
    vc = VirtualCrawler("UCLA")
    print(vc.getiFrameLink())

main()