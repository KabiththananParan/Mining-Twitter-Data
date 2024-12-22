import tweepy
import config  # Import credentials from the config file
import json
import logging
import sys
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authenticate with Twitter
client = tweepy.Client(
    bearer_token=config.bearer_token,
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token=config.access_token,
    access_token_secret=config.access_secret
)


def verify_credentials():
    """Verify Twitter API credentials."""
    try:
        client.get_me()
        logging.info("Authentication successful")
    except tweepy.TweepyException as e:
        logging.error(f"Error during authentication: {e}")
        sys.exit()


def fetch_home_timeline(max_results=10):
    """Fetch tweets from the home timeline. Accepts max_results as a parameter."""
    try:
        response = client.get_home_timeline(
            max_results=max_results,
            tweet_fields=['created_at', 'text', 'author_id'],
            user_auth=True
        )

        if response.data:
            tweets = []
            for tweet in response.data:
                tweets.append({
                    'Tweet ID': tweet.id,
                    'Author ID': tweet.author_id,
                    'Created At': tweet.created_at,
                    'Text': tweet.text
                })
                logging.info(f"Fetched Tweet ID: {tweet.id}")

            return tweets
        else:
            logging.info("No tweets available in the home timeline.")
            return []
        
    except tweepy.TweepyException as e:
        logging.error(f"Error fetching tweets: {e}")
        return []


def save_tweets_to_file(tweets, filename="tweets.json"):
    """Save tweets to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(tweets, file, indent=4)
        logging.info(f"Tweets saved to {filename}")
    except IOError as e:
        logging.error(f"Error saving tweets to file: {e}")


def main():
    """Main execution."""
    print("Verifying Twitter API credentials...")
    verify_credentials()

    max_results = 10
    if len(sys.argv) > 1:
        try:
            max_results = int(sys.argv[1])
        except ValueError:
            logging.error("Invalid number of tweets specified. Using default (10).")

    print(f"Fetching {max_results} tweets from your home timeline...")
    tweets = fetch_home_timeline(max_results)

    if tweets:
        save_tweets_to_file(tweets)
        print(f"{len(tweets)} tweets fetched and saved to file.")
    else:
        print("No tweets fetched.")


if __name__ == "__main__":
    main()



