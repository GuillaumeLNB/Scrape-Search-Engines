#!/usr/bin/python
# to run it : python3 scrape_v2.0.py nice+subject -n 30

import requests, re, time, html, random, argparse, sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from termcolor import colored
from datetime import datetime

print("Coded by GuillaumeLNB, version 2.0")

def main():

	START=datetime.now()
	parser = argparse.ArgumentParser(description="Get URLS from Google")
	parser.add_argument('mot',nargs="?", help="The phrase you want to look up. Put a '+' between the terms. eg: paris+the+city+of+love", type=str)

	args = parser.parse_args()

	if len(sys.argv) <= 1:
	    parser.print_help()
	    sys.exit(1)

	url_lis, ignored_link,total=[],0,0
	ua = UserAgent()
	header = {'User-Agent':str(ua.random)}
	#header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
#	header = "{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}"
	print(colored(header, 'yellow'))
	# .ie ou .fr
	page=requests.get("https://scholar.google.fr/scholar?q="+args.mot.lower(),headers=header)

	soup = BeautifulSoup(page.content, 'html.parser')

	out=open("out-"+args.mot.lower()+'-'+str(time.time())+".txt",'w')
	nb_pages=150
	for i in range(nb_pages):
		print(i, 'pages sur', nb_pages)
		time.sleep(round(random.uniform(3,7), 2)) # take it easy, don't get banned...

		#réccupération des descriptions
		descriptions=re.findall('<div class="gs_rs">(.*?)</div>',str(soup))
		for des in descriptions:
			out.write(re.sub("<.*?>","",des)+'\n'*2)
		

		next_url=str(page.content)
		page=next_url

		#we get here the link of the "Next" button
		next_url=re.sub('<a class=','\n<a class=',next_url)

		#ATTENTION : hl=fr ou hl=en
		next_url=re.findall(r'(/scholar\?start=\d+&amp;q=\w+&amp;hl=fr&amp;as_sdt=0,5)"><span class="gs_ico gs_ico_nav_next">',next_url)


		print(colored("La liste des urls trouvée :",'red','on_grey'))
		print(next_url)
		tmp=open('lastPage.html','w')#to store just in case the script goes wrong, so the last page can be seen manually
		tmp.write(str(page))
		tmp.close()

		try:
			next_url="https://scholar.google.fr/"+html.unescape(next_url[0])
		except IndexError:
			print(colored("L'URL n'a pas été trouvée","red"))
		print('\n',colored(next_url, 'green'), sep="")
		page=requests.get(next_url,headers=header)

		soup = BeautifulSoup(page.content, 'html.parser')
		
	out.close()
	print('\n\nOutput file : out.txt')
	END=(datetime.now()-START).total_seconds()
	print(colored("Done in {} secs".format(round(END,2)),'yellow'))

if __name__ == "__main__":
    main()