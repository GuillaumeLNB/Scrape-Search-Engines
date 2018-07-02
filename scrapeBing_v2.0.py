#!/usr/bin/python
# to run it : python3 scrape_v2.0.py nice+subject -n 30

import requests, re, time, html, random, argparse, sys
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored
from fake_useragent import UserAgent

print("Coded by GuillaumeLNB, version 2.0")

def isValid(link):
    if not re.search("(\.\.\.)|( › )|(^/search\?q)|(^/aclk\?)", link): return True

def main():

    START=datetime.now()
    bad='Our systems have detected unusual traffic from your computer network.  This page checks to see if it&#39;s really you sending the requests, and not a robot.'
    parser = argparse.ArgumentParser(description="Get URLS from Bing")
    parser.add_argument('mot',nargs="?", help="The phrase you want to look up. Put a '+' between the terms. eg: paris+the+city+of+love", type=str)
    parser.add_argument('-n', '--number', default=50, help="Minimum number of links you want (default=50)", type=int)
    args = parser.parse_args()
    nb_links=args.number

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    url_lis, ignored_link,total=[],0,0
    ua = UserAgent()
    header = {'User-Agent':str(ua.random)}
    print(colored(header, 'yellow'))

    page=requests.get("https://www.bing.com/search?q="+args.mot.lower(),headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    out=open("out.txt",'w')

    while len(url_lis)<nb_links:

        time.sleep(round(random.uniform(3,7), 2)) # take it easy, don't get banned...

        # we get the h2 links of the search page
        h2links=soup.findAll("h2")
        good_link=re.findall('<a h="ID=SERP.{7}".href="(http.*?)"', str(h2links))
        for link in good_link:
            total+=1
            if isValid(link) and link not in url_lis:
                out.write(link+'\n')
                print(link)
                url_lis.append(link)
            else: 
                ignored_link+=1
        print(colored('{} links gotten'.format(len(url_lis)), 'red'))
        next_url=str(page.content)
        if re.findall(bad,str(next_url)):
            print(colored("they're coming after you, run !", 'red','on_yellow'))
            sys.exit(0)

        #we get here the link of the "Next" button
		#If you're not searching from francophone areas, you need to change the title of the link eg: Página siguiente, Volgende pagina, Nächste Seite...
        next_url=re.findall('title="Page suivante" href="(.*?)"',next_url)
        try : next_url="https://www.bing.com"+html.unescape(next_url[0])
        except IndexError:
            print(colored('No more results, sorry', 'yellow'))
            sys.exit(0)
        print('\n',colored(next_url, 'green'), sep="")
        page=requests.get(next_url,headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')
    out.close()
    print('\n\nOutput file : out.txt')
    print(colored('links ignored : '+str(ignored_link)+' of '+str(total), 'blue'))
    END=(datetime.now()-START).total_seconds()
    print(colored("Done in {} secs".format(round(END,2)),'yellow'))

if __name__ == "__main__":
    main()