#!/usr/bin/python
# to run it : python3 scrape_v2.0.py nice+subject -n 30

import requests, re, time, html, random, argparse, sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from termcolor import colored
from datetime import datetime

print("Coded by GuillaumeLNB, version 2.0")

def isValid(link):
	if not re.search("(\.\.\.)|( › )|(^/search\?q)|(^/aclk\?)", link): return True

def main():

	START=datetime.now()
	bad='Our systems have detected unusual traffic from your computer network.  This page checks to see if it&#39;s really you sending the requests, and not a robot.'
	parser = argparse.ArgumentParser(description="Get URLS from Google")
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

	# I chose to accept the filter=0 :
	# google choses by default to display the more relevant results
	# you can disable this by removing the 'filter=0' of the url, but you may get less urls...
	# If you want a large number of URLs, you could try increasing the 'num=10' string : eg: 'num=100'
	# Watch out, you might then be kicked out of the server quicker...

	page=requests.get("https://www.google.fr/search?q="+args.mot.lower()+"&num=10&filter=0",headers=header)
	soup = BeautifulSoup(page.content, 'html.parser')

	out=open("out.txt",'w')

	while len(url_lis)<nb_links:

		time.sleep(round(random.uniform(3,7), 2)) # take it easy, don't get banned...

		# we get the h3 links of the search page
		h3links=soup.findAll("h3")
		good_link=re.findall('href="(.*?)"', str(h3links))
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
		next_url=re.sub('<a class=','\n<a class=',next_url)
		next_url=re.findall('<a class=(?:=)?"(?:pn|fl)".*?href="(.*?)" .*?>Suivant</span></a>',next_url)
		next_url="http://www.google.fr/"+html.unescape(next_url[0])
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