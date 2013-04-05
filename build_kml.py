# -*- coding: utf-8 -*-

import re
import wiki_parser
import simplekml
from optparse import OptionParser
		

def load_article_urls(url_file):
	print 'Loading urls from %s...' % url_file,
	
	article_urls = []
	
	fl = open(url_file, 'r')
	for line in fl:
		line = line.strip()
		if not line or line[0] == '#': continue # ignore comments
		
		article_urls.append(line)
	
	print 'DONE'
	
	return article_urls
	

def build_kml(urls_file, output_file='output.kml'):
	# get list of articles
	#url_file = 'articles.txt'
	article_urls = load_article_urls(urls_file)
	
	# create KML document
	kml = simplekml.Kml()
	
	print 'Pulling data from urls...'
	for url in article_urls:
		data = wiki_parser.pull_data_for_url(url)
		if not data: continue
		if not data.get('lat') or not data.get('lon'): 
			print 'No gps for %s, skipping' % url
			continue
		
		
		pnt = kml.newpoint()
		pnt.name = data['title']
		if data.get('image'):
			pnt.description = '<img src="%s">' % data['image']
			
		pnt.coords = [(data['lon'], data['lat'])]
		
		
	
	kml.save(output_file)

	
	
	
def main(options):
	if not options or not options.urls_file:
		print 'You must enter the command line options'
		return None;
		
	build_kml(options.urls_file, options.output_file)

if __name__ == '__main__':
	# Options from command line
	parser = OptionParser()
	parser.add_option("-i", '--urls', dest="urls_file", help="Path to file of URLs", type="string")
	parser.add_option("-o", '--output_file', dest="output_file", help="Path to output KML file", type="string", default='output.kml')

	(options, args) = parser.parse_args()
	
	
	main(options)