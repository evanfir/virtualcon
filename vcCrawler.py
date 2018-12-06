"""
This is the first version of our crawler that crawls assist.org to 
get information on courses that are necessary for each CS student prior 
to transfer to a 4 year university. 
Currently this program only can retrieve information for PCC students 
that wanna transfer to UCI, UCD, UCSD, and UCLA.
For future, this program can be expanded to other schools and universities 
and majors.

"""
import requests
from bs4 import BeautifulSoup

class VirtualCrawler:
    def __init__(self, toCollege, fromCollege = "PASADENA"):
        self.__fromCollege = fromCollege
        self.iframeLink = ""
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
        self.iframeLink = iframe['src']
        # iframeSource = requests.get(iframeLink)
        # iframeText = iframeSource.text
        return self.iframeLink
    
    def getText(self):
        sourceCode = requests.get(self.iframeLink)
        plainText = sourceCode.text
        return plainText


def main():
    vc = VirtualCrawler("UCLA")
    print(vc.getiFrameLink())

# main()