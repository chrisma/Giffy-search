import re
import json
import random
import urllib
import urllib2

def gif_search(query, dominant_color=None):
	"""
	Return a list of URLs of animated gifs corresponding to the query.

	dominant_color must be one of ['orange','red','yellow','green','teal','blue',
	'purple','pink','white','gray','black','brown'].
	The URLs are sorted the way that google ranked them (first one most relevant).
	The URLs are not guaranteed to be valid (i.e. return HTTP 200).

	Uses the "unofficial" endpoint which is also used by the Google image search
	website because the official API does not support the "animated" imgType 
	(https://developers.google.com/custom-search/json-api/v1/reference/cse/list)
	as of Feb. 2015 and filtering only for gifs does not guarantee animation.
	As side effects, this also allows returning more than 10 results and 
	gets around rate limits.
	"""

	allowed_colors = ['orange','red','yellow','green','teal','blue',
					'purple','pink','white','gray','black','brown']
	if dominant_color not in allowed_colors:
		dominant_color = None

	base_url = 'https://www.google.com/search?'
	tbs = 'itp:animated,ift:gif'
	if dominant_color:
		tbs = tbs + ',ic:specific,isc:' + dominant_color
	search_url = base_url + urllib.urlencode({
			'q': query,
			'tbs': tbs, #only animated gifs
			'tbm':'isch', #image search
			'fp': '%016x' % random.randrange(16**16),
			'tch':1,
			'ech':1 })

	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'
		headers = {'Referer':'https://www.google.com/', 'User-Agent': user_agent}
		req = urllib2.Request(search_url, headers=headers, origin_req_host="www.google.com")
		data = urllib2.urlopen(req).read().decode('string_escape').decode('string_escape')
	except urllib2.URLError, e:
		print "ERROR", __name__, e
		return []

	regex = re.compile("imgres\?imgurl=(.{0,200}?\.gif)")
	lst = regex.findall(data)
	lst = [url.replace('\\/', '/') for url in lst]

	return lst
