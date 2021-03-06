# Scrape-Search-Engines
The scripts get urls from Google and soon other search engines.

To run it from terminal : `python3 scrapeGoogle_v2.1.py how+to+get+a+good+job+after+graduation -n 400`

You may need to install the following modules :
* fake_useragent   -> `(sudo) pip3 install fake_useragent`
* termcolor        -> `(sudo) pip3 install termcolor`

_**Consider not running the programm too often. A delay of a few hours might be requierd sometimes**._

If you run the programm too often, you may see the following lines:

*Our systems have detected unusual traffic from your computer network.  This page checks to see if it&#39;s really you sending the requests, and not a robot.  
Why did this happen?
This page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the Terms of Service.
The block will expire shortly after those requests stop.  In the meantime, solving the above CAPTCHA will let you continue to use our services.
This traffic may have been sent by malicious software, a browser plug-in, or a script that sends automated requests.  If you share your network connection, ask your administrator for help &mdash; a different computer using the same IP address may be responsible.  
Learn more
Sometimes you may be asked to solve the CAPTCHA if you are using advanced terms that robots are known to use, or sending requests very quickly.*

You will then need to wait (sometimes a few hours) before re running the script.

If you get the following error : 
*AttributeError: module 'html5lib.treebuilders' has no attribute '_base'*, 
You may need to upgrade the bs4 and html5lib modules by running the following commands :

* `(sudo) pip3 install --upgrade beautifulsoup4`
* `(sudo) pip3 install --upgrade html5lib`
