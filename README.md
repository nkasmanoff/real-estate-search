Contained in this repository is my work scraping and analyzing Zillow.com for potential real estate investment/living opportunities. 

Listings are based off of geographic location, where in the main python file FetchApts.py, one of the parameters included are the latitude and longitude boundaries for the real estate search. The current conditions imposed are for listings located below 86th street in Manhattan, but this is easily adjustable just by changing those values. Unfortunately I don't have a better means of doing this since this project was fairly simple, but to get listings in a region you would need to hard code in those points by looking them up online using a resource such as https://www.latlong.net/convert-address-to-lat-long.html. 


Dependencies
------------

A lot of this scraping is done using the python zillow wrapper at https://github.com/seme0021/python-zillow. After creating a developer key for zillow, using this site allows you to easily download and search through listings. 


Description
-----------

Building off of the zillow api, my code then takes the json acquired from zillow and then builds a dataset with meaningful features about a listing in order to inform the user. Included in the results folder is one example result, a csv containing one such condo along with the scraped information from FetchApts.py. Further documentation is provided in code, along with the write to csv function to output results immediately. 


To run this code, simply download the entire directory, and run type "python FetchApts.py" in the terminal after setting the desired parameters. 



Update  8/13
-------------

The current zillow listing id's I've used to iterate over are no longer valid, so to update this you must go to Zillow.com, and once you're in the desired region you need to find one of the zillow ID's listed there and change the base id (zid0) in the code to iterate over similar listings. 