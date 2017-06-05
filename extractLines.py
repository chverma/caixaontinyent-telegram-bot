from bs4 import BeautifulSoup
import re
def getLines():
    lines=[]
    html_doc = open("movs.html", "r").read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    for tr in soup.find_all('tr'):
        line=[]
        for td in tr.find_all('td'):
            val = td.string
            if val is not None:
		lineStr = re.sub(r'\d{16}.', '', td.string)
                line.append(lineStr)
            else:
               line.append(tr.find_all('a')[0].string.replace('TRANSF.SEPA ', ''))
        lines.append(line)
    return lines[1:]

def getFormatedLines():
    lines = getLines()
    strMsg = ''
    for l in lines:
        if len(l)==6:
            strMsg += '*%s* %s `%s`\n' % (l[0], l[3], l[4])
    return strMsg
if __name__=='__main__':
    print getFormatedLines()
