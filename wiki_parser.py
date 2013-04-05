from bs4 import BeautifulSoup
import urllib2
import re
import os

def get_html(url):	
	print 'Pulling data for: %s' % url
	#url = url.lower()

	user_agent = "Mozilla/5 (Solaris 10) Gecko"
	headers = {'User-agent' : user_agent}
	request = urllib2.Request(url, '', headers)

	try: 
		html = urllib2.urlopen(request).read()
		return html
	except urllib2.URLError, e:
	    print "No such url: %s" % url
	except urllib2.HTTPError, e:
		print "No such url: %s" % url
	except ValueError, e:
		print "no such url: %s" % url

	exit()
	return None

	#html = urllib.urlopen(url).read()
	#return html


def get_from_cache(url):
	key = url.split('/')[-1]
	key = key.lower()
	
	
	cache_file = 'cache/%s.html' % key
	try :
		fl = open(cache_file, 'r')
		html = fl.read()
		fl.close()
		return html
	except:
		pass
	
	
	html = get_html(url)
	if not html: return None
		
	# save cached file (make directory if needed)
	cache_directory = os.path.dirname(cache_file)
	if not os.path.exists(cache_directory):
		print 'Creating cache directory at: %s' % cache_directory
		os.makedirs(cache_directory)
	
	fl = open(cache_file, 'w+')
	fl.write(html)
	fl.close()

	return html


def pull_data_for_url(url):
	html = get_from_cache(url)
	if not html: return None

	try:
		soup = BeautifulSoup(html)
	except:
		print 'Bad HTML found for: %s' % url
		return None
	
	
	
	# title
	title = soup.find('h1')
	title = title.string
	data = {'title': title}

	# geo coordinates
	geo = soup.find('span', attrs={'class':'geo'})
	if geo:
		coor = geo.string.split(';')
		(lat, lon) = [float(c.strip()) for c in coor]
		data['lat'] = lat
		data['lon'] = lon
		
		
	# Infobox
	infobox = soup.find('table', attrs={'class':'infobox'})
	if infobox:
		img = infobox.find('img')
		src = 'http:%s' % img['src']
		data['image'] = src
		
		
	return data
		
