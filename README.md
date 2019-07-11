# InfinityChan (8ch.net) Board Log Scraper

This tool uses the Python requests library to crawl, scrape, and process any board's moderation log into a CSV file. 

## Prerequisites 

All you need to use this tool is an internet connection and a Python interpreter. 

## Using the tool

Git clone the repo into a local directory on which you have read and write privileges. 
To use the scraper, run `python scraper.py <board name>`, where `<board name>` is the board you wish to scrape the mod log of ('pol', 'tech', etc).
To use the dataprocess.py script on an existing scrapefile, run the script with the filename as the first argument and the board name as the second argument

## Tool output file formats

Running the scraper.py script will produce 2 output files - a 'scraperfile' which contains the raw text of the scraped board log, and a 'resultfile', which is a CSV file of board actions, with the post ID and thread ID extracted into their own column. 

The analysis of the scraperfile is handled by the processdata.py script, which uses a series of regex statements followed by a sequence of elif statements to categorize the actions. This is called automatically by scraper.py.

## Tests

As of yet there are no tests.

## Contributing

Feature requests are welcome, as are tests for different boards.

## Authors

Anonymous for now.

## License

MIT License