import tweepy
import config    # Import credentials from the config file


# Authenticate with Twitter

client = tweepy.Client(
    bearer_token=config.bearer_token,
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token=config.access_token,
    access_token_secret=config.access_secret
)   

# Check API authentication

def verify_credentials():
    """Verify Twitter API credentials."""
    try:
        client.get_me()
        print("Authentication successful")
    except tweepy.TweepyException as e:
        print(f"Error during authentication: {e}")
        exit()


def fetch_home_timeline():
    """Fetch and print tweets from the home timeline."""
    try:
        response = client.get_home_timeline(
            max_results = 10,
            tweet_fields=['created_at', 'text', 'author_id'],
            user_auth=True
        )

        if response.data:
            for tweet in response.data:
                print(f"Tweet ID: {tweet.id}\nAuthor ID: {tweet.author_id}\nText: {tweet.text}\n")
        
        else:
            print("No tweets available in the home timeline.")
    
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")



# Main execution

if __name__ == "__main__":
    print("Verifying Twitter API credentials...")
    verify_credentials()

    print("Fetching tweets from your home timeline...")
    fetch_home_timeline()