# California-Oregon-fires-Real-time-Tweet-Analytics
This project analyzes tweets streamed in real time about Currently Ongoing California-Oregon wildfires, with the help of real-time visualizations in order to gain valuable insights. Performs twitter data streaming, cleaning, processing, NLP, sentiment analysis, and visuzalizations 


As we know, Wildfires in USA raced through more than a dozen Western states Thursday, incinerating homes, forcing hundreds of thousands of evacuations, and burning a swath of land almost the size of New Jersey.

At least 23 people have died as of Friday and hundreds of homes have been destroyed by more than 100 major fires that have consumed nearly 7,000 square miles. Authorities in Oregon say more than 500,000 people statewide have been forced to evacuate because of wildfires - over 10% of the state’s 4.2 million population.

At such crucial times, it becomes important for the government authorities to get complete picture from  the public which can be done through social media,
but the problem with that is social media is an ocean of huge unstructured text corpus, which is why it becomes difficult to analyze such data, this is where natural language processing & text analytics comes to rescue

In this project, I streamed live twitter data with the help of twitter's streaming library tweepy, I filtered it for 3 keywords which are ['oregon','oregon wildfires','california fires']

After which I stored incoming live tweets id, text, location, created_at (post upload time), and sentiment (positive, negative, neutral) in sqlite3

In order to analyze sentiment, I used VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. VADER uses a combination of A sentiment lexicon is a list of lexical features (e.g., words) 
which are generally labeled according to their semantic orientation as either positive or negative. VADER not only tells about the Positivity and Negativity score but also tells us about how positive or negative a sentiment is!

After which I categoried the probability values given by VADER into positive, negative & neutral classes

Then next, I wanted to plot a line-scatter plot of changing count of sentiments in tweets with respect to time. I choose to track for every 15 minutes
Next, I conducted Topic Tracking with the help of NLTK, before that i needed to clean data to contain only lowercase text & thus performed text cleaning with python's re library,
filtered out special characters, emoji's, links & urls. Then I used Punkt Sentence Tokenizer, which is used to divide a text into a list of sentences by using an unsupervised algorithm & also removed stopwords.

Finally, I visualized all of this using dash, 

1. Live Scatter Plot of no. of positive, negative & neutral tweets wrt to time (every 15 mins) <br>
![Img](https://github.com/chelseafernandes2000/California-Oregon-fires-Real-time-Tweet-Analytics/blob/master/Realtimetweeteranalysis/Output%20Snapshots/snap_1.JPG)

2. Live Bar Plot - Topic Trackking (Most Popular words) <br>
![Img](https://github.com/chelseafernandes2000/California-Oregon-fires-Real-time-Tweet-Analytics/blob/master/Realtimetweeteranalysis/Output%20Snapshots/snap_2.JPG)

3. Live Pie plot of aggregate sentiment analysis <br>
![Img](https://github.com/chelseafernandes2000/California-Oregon-fires-Real-time-Tweet-Analytics/blob/master/Realtimetweeteranalysis/Output%20Snapshots/snap_3.JPG)


Please find inside realtimetweeteranalysis:
1. tweet_streamer.py: Streams live tweets as per keywords & stores in sqlite3
2. analytics.py: Retrives live data, performs analytics and plots using dash
3. OregonFiretwitter: sqlite3 database
