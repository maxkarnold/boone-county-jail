# boone-county-jail
class web scraper for boone-county-jail detainee information

This web scraper extracts all of the detainees from the boone county jail website and puts them into a SQL database. 
This includes basic info and all of the charges against them.

Steps to running the web scraper:

1. Download/clone the repository
2. Delete the boone_county_jail.db
2. Go to the directory in your terminal/cmd line
3. pip install all of the necessary modules in your directory (not necessary to include any of the Jupyter modules)
4. Run the scraper.py (command is <i>python scraper.py</i>)
5. Should run correctly and say <i>FINALLY DONE SCRAPING!!!</i>
6. The boone_county_jail.db should be updated and in your directory
7. Go ahead and open the database in SQLlite
