#!/usr/bin/python3.7
# to run it : python3 scrape_v2.0.py nice+subject -n 30

import requests, re, time, html, random, argparse, sys
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored
from fake_useragent import UserAgent

print("Coded by GuillaumeLNB, version 2.2")

def isValid(link):
    if not re.search(r"(\.\.\.)|( › )|(^/search\?q)|(^/aclk\?)|webcache.googleusercontent.com", link): return True

def getSoup(url:str, header):
    "download the page and return the soup object"
    page=requests.get(url, headers=header)
    soup=BeautifulSoup(page.text, 'html.parser')
    return soup

def getURLSfromPage():
    "return the urls of the page"
    pass

def getNextURL():
    "return the next url of the page (the 'next' link)"
    pass

def process():
    "carry on the scrapping"
    pass


def main(word:str):

    START=datetime.now()
    bad='Our systems have detected unusual traffic from your computer network. This page checks to see if it&#39;s really you sending the requests, and not a robot.'

    nb_links=args.number

    url_lis, ignored_link,total=[],0,0
    ua = UserAgent()
    header = {'User-Agent':str(ua.random)}
    print(colored(header, 'yellow'))
    
    
    
    initialPage=f"https://www.google.fr/search?q={args.mot.lower()}&num=100&filter=0"
    out=open("out_"+args.mot+"_"+re.sub(r'\W+', '_', str(datetime.now()))[:19]+".txt",'w')



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
        try : next_url="http://www.google.fr/"+html.unescape(next_url[0])
        except IndexError:
            print(colored('No more results, sorry', 'yellow'))
            sys.exit(1)
        print('\n',colored(next_url, 'green'), sep="")
        page=requests.get(next_url,headers=header)

        soup = BeautifulSoup(page.content, 'html.parser')
        
    out.close()
    print(f'\n\nOutput file : {out.name}')
    print(colored(f'links ignored : {ignored_link} of {total}', 'blue'))
    END=(datetime.now()-START).total_seconds()
    print(colored("Done in {} secs".format(round(END,2)), 'yellow'))






if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get URLS from Google")
    parser.add_argument('mot',nargs="?", help="The phrase you want to look up. Put a '+' between the terms. eg: paris+the+city+of+love", type=str)
    parser.add_argument('-n', '--number', default=50, help="Minimum number of links you want (default=50)", type=int)
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
  
  
    # main()




    # I chose to accept the filter=0 :
    # google choses by default to display the more relevant results
    # you can disable this by removing the 'filter=0' of the url, but you may get less urls...
    # If you want a large number of URLs, you could try increasing the 'num=10' string : eg: 'num=100'
    # Watch out, you might then be kicked out of the server quicker...

    """
    def main_entry_point(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('corpus_path', metavar='dossier_corpus', type=str,
                            help='Le dossier contenant le corpus (un sous-dossier par étiquette)')
        parser.add_argument('out_path', metavar='fichier_sortie',
                            nargs='?', type=str, default=None,
                            help='Le chemin du fichier de sortie')
        parser.add_argument('--mots-vides', metavar='fichier_mots_vides', type=str, default=None,
                            help='Un fichier contenant une liste de mots vides (un par ligne)')
        parser.add_argument('--lexicon', metavar='fichier_lexique', type=str, default=None,
                            help='Un fichier contenant un lexique (un mot par ligne)')
        parser.add_argument('--boolean', action='store_true',
                            help='Utiliser des représentations booléennes')

        args = parser.parse_args(argv)
        return process(args.corpus_path, args.out_path, args.boolean, args.mots_vides, args.lexicon)

    # Legacy interactive mode
    print('Mode interactif (legacy). Utiliser `vectorisation.py -h` pour le mode CLI.`')
    corpus_path = input("Nom du dossier contenant le corpus : ")
    fichier_mots_vides = input("Nom du fichier de mots vides (se terminant par .txt) : ")

    choix = None
    while choix not in ('1', '2'):
        choix = input("Représentation booléenne (taper 1) ou en nombre d'occurrences (taper 2) ? ")
    process(corpus_path, boolean=choix == 1, fichier_mots_vides=fichier_mots_vides)


if __name__ == '__main__':
    sys.exit(main_entry_point(sys.argv[1:]))
    """