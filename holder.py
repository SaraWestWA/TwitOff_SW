# # For twitter.py
# def add_user_history(name):
#     '''Add max tweet history (API limit of 3200) to database'''
#     try:
#         twitter_user = TWITTER.get_user(name)
#         db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=name)
#         tweets = twitter_user.timeline(count=200,
#                                         exclude_replies=True,
#                                         include_rts=False,
#                                         since_id=db_user.newest_tweet_id)        
#         oldest_max_id = tweets[-1].id - 1
#         tweet_history = []
#         tweet_history += tweets
#         # Add newest_tweet_id to the User table
#         if tweets:
#             db_user.newest_tweet_id = tweets[0].id
#         # Continue to collect tweets using max_id and update until 3200 tweet max
#         while True:
#             tweets = twitter_user.timeline(count=200,
#                                         exclude_replies=True,
#                                         include_rts=False,
#                                         tweet_mode='extended',
#                                         max_id=oldest_max_id)
#             if len(tweets) == 0:
#                 break
#             oldest_max_id = tweets[-1].id - 1
#             tweet_history += tweets 
#         print(f'Total Tweets collected for {username}: {len(tweet_history)}')
#         # Loop over tweets, get embedding and add to Tweet table
#         for tweet in tweet_history:
#             # Get an examble basilica embedding for first tweet
#             embedding = vectorize_tweet(nlp, tweet.full_text)
#             # Add tweet info to Tweet table
#             db_tweet = Tweet(id=tweet.id,
#                              tweet=tweet.full_text[:300],
#                              embedding=embedding)
#             db_user.tweet.append(db_tweet)

#         DB.session.add(db_user)
#     except Exception as e:
#         print('Error processing {}: {}'.format(username, e))
#         raise e
#     else:
#         # If no errors happened than commit the records
#         DB.session.commit()
#         print('Successfully saved tweets to DB!')





# ### For app.py


#     @app.route('/history/<name>', methods=['GET'])
#     def history():
#         add_user_history()
#         return render_template('base.html', title='All tweets updated!', users=User.query.all())

