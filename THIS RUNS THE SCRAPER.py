import praw								#library for interacting with and scraping reddit
import csv                              #library for writing to a csv file
import datetime                         #library to convert UTC time into normal time and date


# this block of code authenticates the scraper through OAuth
reddit = praw.Reddit(client_id='tG7jQGYZ3ncjJQ',
                     client_secret='BLAW',            #Password is incorrect here, you can make your own bot through Reddit
                     user_agent='BitcoinScraperv1')



# this line of code decides which subreddit(s) the scraper goes to
subreddit = reddit.subreddit('bitcoin+cyrptocurrency+cyrptomarkets+BitcoinDiscussion')



# the commented-out code below allows you to search through posts by ethier using 'top' for the month or 'hot' posts with a limit of 3. 
# this scaper is currently using a time range of two months instead of seraching through top/hot. The location of this code is in the 'for submisson line'

# top = subreddit.top('month')
# hot_python = subreddit.hot(limit=3)


# this block of code indicates which comments we will write into our csv file. We only get comments with the keywords below.
words_to_match = ['bitcoin gold','BTG', 'Bitcoin Gold', 'Bitcoin gold', 'bitcoingold', 'btc gold', 'BTC fork', 'bitcoin fork']		


# creates a new csv file with the name new_file
with open('new_reddit.csv', 'w', encoding='utf-8') as new_file:
			csv_writer = csv.writer(new_file, delimiter=',')

# begins searching through the submisson. The numbers in the first line of code indicate the UTC time start and end, these numbers can be gotten online.
# be careful here, there can be a lot posts within a given UTC time range (here it is 150681599 and 1509947204). Look up new UTC values through google. 
for submission in subreddit.submissions(1506815999, 1509947204):

	# as we begin mining, the scraper first ignores the 'stickied' posts. Then it begins printing in the console the title of every thread we scrape.
	if not submission.stickied:
		print('Title: {}, ups: {}'.format(submission.title, submission.ups))

		#opens the csv file we created
		with open('new_reddit.csv', 'a', encoding='utf-8') as new_file:
			csv_writer = csv.writer(new_file, delimiter=',')


			#this line of code helps format the comments into a form that the scraper can read
			submission.comments.replace_more(limit=0)

			#we begin looking in every single comment in a thread
			for comment in submission.comments.list():

				#checks if the comment matches our keywords
				comment_text = comment.body.lower()
				isMatch = any(string in comment_text for string in words_to_match)
				#writes the comment and the date to the csv file if the keywords match
				if isMatch:
					date = datetime.datetime.fromtimestamp(comment.created_utc)
					csv_writer.writerow([comment.body,date])





