from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import sys
import urllib2

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="TduAGVlPHWdN8qnUUann4ODAc"
consumer_secret="E1YXRzLxoSUA2Zev70USJm9zQ8OUbY8DeSQP6m4gIlnTeDwIoN"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="528679234-67r4yXT7cfGT5SBPa5DqkuuLSlqPKX4qzG2NnEWm"
access_token_secret="SMgEXc4mco4F0oShUhJ0RtUgtTP9EnhGBM5D6vo8FDqrf"

current_dir = ""


def save_pic_from_url(url):
	file_name = url.split('/')[-1]

	media = urllib2.urlopen(url)
	with open(current_dir + file_name,'wb') as localFile:
		localFile.write(media.read())


class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream.

	"""
	def on_data(self, data):
		json_data = json.loads(data)
		# Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
		print 'tweet -> @%s: %s' % (json_data['user']['screen_name'], json_data['text'].encode('ascii', 'ignore')) 
		
		#checks if there is any media-entity
		if 'entities' in json_data and 'media' in json_data['entities']:
			for med in json_data['entities']['media']:
				# checks if the entity is of the type "photo"
				mediaurl = med['media_url']
				print '     PHOTO_URL:%s ' % mediaurl

				save_pic_from_url(mediaurl)

		print ''
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':

	tagname = '#Pistorius'

	if not tagname:
		if len(sys.argv)>1:
			tagname = sys.argv[1]
		else :
			print "Enter a tag name as argument"
			sys.exit()


	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	if not os.path.exists(tagname):
		os.makedirs(tagname)
	current_dir = tagname + '/'
	stream = Stream(auth, l)
	stream.filter(track=[tagname])
