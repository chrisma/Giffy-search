"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, abort, send_file
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from werkzeug import DebuggedApplication
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

import urllib
import urllib2
import io
import random
from google_gif_search import gif_search

@app.route('/<path:query>/<dominant_color>/<int:index>')
@app.route('/<path:query>/<dominant_color>')
@app.route('/<path:query>/<int:index>')
@app.route('/<path:query>')
def handle_query(query, dominant_color=None, index=0):

	query = query.replace('_', '')

	gif_urls = gif_search(query, dominant_color=dominant_color)
	index = index if index<len(gif_urls) else len(gif_urls)-1

	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'
	headers = {'Referer':'https://www.google.com/', 'User-Agent': user_agent}

	for url in gif_urls[index:]:
		try:
			req = urllib2.Request(url, headers=headers)
			image_data = urllib2.urlopen(req).read()
			if '<html' in image_data:
				app.logger.warning('Got HTML' + url)
			else:
				return send_file(io.BytesIO(image_data),
						attachment_filename=query+'.gif',
						mimetype='image/gif')
		except urllib2.URLError, e:
			app.logger.warning('Google response', e, url)
		else:
			continue
	else:
		app.logger.error('All URLs failed', query, index)
		abort(404)

