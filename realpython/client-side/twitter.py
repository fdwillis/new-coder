import tweepy

consumer_key = "DkjdoEbzW3wodiM1bFMDuIH5q"
consumer_secret = "NnzSa09B0GkO9OgnoZ3rhpfdI7GAVleTV0ifd2FwHF1PIGlwZv"
access_token = "461798811-vTzV3eUUxn8QtZ4BIsAnTGDnCZrRmC2LoY6hKIZ3"
access_secret = "7lZ65iUiiE3OoaVKikAMzg5TR0Lnpnhm8vSEMI5VfclAW"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

search_for = raw_input("What To Search Twitter For?: \n ")
tweets = api.search(q=search_for, result_type="popular", count=100)

for tweet in tweets:
	print "Username: ", tweet.user.name
	print "User Location:", tweet.user.location
	print "Tweet: ", tweet.text
	print "Tweet Location: ", tweet.place
	print "Retweet Count: ", tweet.retweet_count
	print "Created:", tweet.created_at.strftime("%B %d, %Y"), '\n'
