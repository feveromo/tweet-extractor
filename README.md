# Tweet Text Extractor

A Python script to extract plain text content from Twitter's data export format (tweets.js) into a clean text file suitable for analysis or use with language models.

## Features

- Extracts only tweet text content, removing metadata and formatting
- Creates clean, readable output with proper spacing
- Filters out:
  - Retweets (starting with "RT @")
  - Tweets containing links (http://t.co/ or https://t.co/)
  - Empty tweets
- Configurable maximum number of tweets to extract
- Detailed logging of the extraction process
- Error handling and reporting
- Summary statistics of processed tweets
- Support for large tweet archives

## Prerequisites

- Python 3.6 or higher
- Your Twitter data export file (`tweets.js`)

## Installation

1. Save the script file to your local machine:
   - `extract_tweets.py`

2. Place the script in the same directory as your `tweets.js` file.

## Usage

Basic usage:
```bash
python extract_tweets.py
```

With command line arguments:
```bash
# Extract only 100 tweets
python extract_tweets.py --max-tweets 100

# Specify input and output files
python extract_tweets.py --input my_tweets.js --output my_output.txt

# Combine options
python extract_tweets.py --max-tweets 50 --input custom.js --output result.txt
```

### Command Line Arguments

- `--max-tweets`: Maximum number of tweets to extract (optional)
- `--input`: Input file path (default: 'tweets.js')
- `--output`: Output file path (default: 'tweets_text_only.txt')

## Output Files

The script creates two files:
- `tweets_text_only.txt` - Contains only the text content of your tweets
- `tweet_extraction.log` - Detailed log of the extraction process

## Output Format

The extracted tweets will be saved in the output file with:
- One tweet per line
- UTF-8 encoding to preserve special characters
- No retweets or tweets containing links

## Logging

The script maintains a single log file (`tweet_extraction.log`) that includes:
- Process start and end times
- Number of tweets processed
- Number of valid tweets extracted
- Number of skipped tweets (broken down by reason)
- Any errors or issues encountered
- Final summary statistics

## Example Log Output
```
2024-03-24 14:30:22 - INFO - Starting tweet extraction script
2024-03-24 14:30:22 - INFO - Reading input file...
2024-03-24 14:30:23 - INFO - Successfully parsed JSON data containing 1000 tweets
2024-03-24 14:30:23 - INFO - Extracted 950 valid tweets
2024-03-24 14:30:23 - INFO - Skipped 20 invalid or empty tweets
2024-03-24 14:30:23 - INFO - Skipped 15 tweets containing links
2024-03-24 14:30:23 - INFO - Skipped 15 retweets
2024-03-24 14:30:23 - INFO - Successfully wrote tweets to output file
```

## Error Handling

The script includes error handling for common issues:
- File not found errors
- JSON parsing errors
- Writing permission errors
- Encoding issues

All errors are logged with detailed messages to help troubleshoot issues.

## Troubleshooting

If you encounter issues:

1. Check the log file for detailed error messages
2. Verify your tweets.js file is in the correct location
3. Ensure you have write permissions in the directory
4. Verify your tweets.js file is properly formatted

## Limitations

- The script expects the standard Twitter data export format
- Very large files may require additional memory
- The script only extracts tweet text (no media, links, or metadata)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For support, please:
1. Check the log file for error messages
2. Review the Troubleshooting section
3. Submit an issue on the project repository
