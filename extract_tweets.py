import json
import re
import logging
import argparse
from datetime import datetime

# Set up logging
def setup_logging():
    """Configure logging to both file and console"""
    # Use a fixed log filename
    log_filename = 'tweet_extraction.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),  # 'w' mode overwrites the file each time
            logging.StreamHandler()
        ]
    )
    return log_filename

def clean_tweets_file(input_file, output_file, max_tweets=None):
    """
    Extract just the tweet text from a tweets.js file and save to txt
    Skips:
    - tweets containing links (http://t.co/ or https://t.co/)
    - retweets (starting with "RT @")
    - empty tweets
    
    Args:
        input_file (str): Path to input tweets.js file
        output_file (str): Path to output text file
        max_tweets (int, optional): Maximum number of tweets to extract. None means extract all.
    """
    logging.info(f"Starting tweet extraction process from {input_file}")
    if max_tweets:
        logging.info(f"Will extract up to {max_tweets} tweets")
    
    try:
        # Read the input file
        logging.info("Reading input file...")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        logging.info(f"Successfully read {len(content)} characters from input file")
        
        # Remove the JavaScript wrapper
        logging.info("Removing JavaScript wrapper...")
        json_str = content.replace('window.YTD.tweets.part0 = ', '')
        logging.info("JavaScript wrapper removed")
        
        # Parse the JSON
        logging.info("Parsing JSON data...")
        try:
            tweets = json.loads(json_str)
            logging.info(f"Successfully parsed JSON data containing {len(tweets)} tweets")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {str(e)}")
            raise
        
        # Extract tweet texts
        logging.info("Extracting tweet texts...")
        tweet_texts = []
        skipped_tweets = 0
        skipped_tweets_with_links = 0
        skipped_retweets = 0
        
        for i, tweet in enumerate(tweets, 1):
            if max_tweets and len(tweet_texts) >= max_tweets:
                logging.info(f"Reached maximum tweet limit of {max_tweets}")
                break
            
            if 'tweet' in tweet and 'full_text' in tweet['tweet']:
                text = tweet['tweet']['full_text'].strip()
                # Skip tweets that are:
                # - empty
                # - contain t.co links
                # - are retweets (start with RT @)
                if text and "://t.co/" not in text and not text.startswith("RT @"):
                    tweet_texts.append(text)
                    if max_tweets and len(tweet_texts) >= max_tweets:
                        break
                else:
                    if "://t.co/" in text:
                        skipped_tweets_with_links += 1
                        logging.debug(f"Skipped tweet with link at index {i}")
                    elif text.startswith("RT @"):
                        skipped_retweets += 1
                        logging.debug(f"Skipped retweet at index {i}")
                    else:
                        skipped_tweets += 1
                        logging.debug(f"Skipped empty tweet at index {i}")
            else:
                skipped_tweets += 1
                logging.debug(f"Skipped malformed tweet at index {i}")
                
        logging.info(f"Extracted {len(tweet_texts)} valid tweets")
        logging.info(f"Skipped {skipped_tweets} invalid or empty tweets")
        logging.info(f"Skipped {skipped_tweets_with_links} tweets containing links")
        logging.info(f"Skipped {skipped_retweets} retweets")
        
        # Write the cleaned tweets to the output file
        logging.info(f"Writing tweets to {output_file}...")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for text in tweet_texts:
                    f.write(text + '\n')  # Changed from '\n\n' to '\n'
            logging.info("Successfully wrote tweets to output file")
        except IOError as e:
            logging.error(f"Failed to write output file: {str(e)}")
            raise
        
        # Final statistics
        logging.info("=== Extraction Summary ===")
        logging.info(f"Total tweets processed: {len(tweets)}")
        logging.info(f"Valid tweets extracted: {len(tweet_texts)}")
        logging.info(f"Skipped tweets (empty/malformed): {skipped_tweets}")
        logging.info(f"Skipped tweets (containing links): {skipped_tweets_with_links}")
        logging.info(f"Skipped tweets (retweets): {skipped_retweets}")
        logging.info(f"Output file: {output_file}")
        
        return len(tweet_texts)
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Extract tweets from Twitter archive')
    parser.add_argument('--max-tweets', type=int, help='Maximum number of tweets to extract')
    parser.add_argument('--input', default='tweets.js', help='Input tweets.js file path')
    parser.add_argument('--output', default='tweets_text_only.txt', help='Output text file path')
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = setup_logging()
    logging.info("Starting tweet extraction script")
    
    try:
        tweets_extracted = clean_tweets_file(args.input, args.output, args.max_tweets)
        logging.info(f"Script completed successfully. Log file: {log_file}")
        
    except Exception as e:
        logging.error("Script failed with error")
        logging.error(str(e))
        raise
