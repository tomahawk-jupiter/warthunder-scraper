# Warthunder plane scraper

NOTE: I have updated `scrape_planes.py` to also list the planes's categories, eg. Bomber, Long range bomber. I haven't run this script yet to update the data. I have tested it on just the first few planes and it seems to work okay.

## Contents

- [Overview](#overview)
- [Libraries and packages used](#libraries-and-packages-used)
- [Example of data it produces](#example-of-data-it-produces)
- [How to run](#how-to-run)

## Overview

A python script for scraping data about all planes from the game Warthunder. It only scrapes a few of the stats/info.

There is a script for scraping and saving to CSV, then a script for cleaning the CSV and saving a copy as JSON.

**NOTE: it will take perhaps 10-15 minutes or so to finish scraping. There are aprox 1000 planes in the game.**

## Libraries and packages used

- BeautifulSoup
- pandas
- requests
- csv
- json
- re

## Example of data it produces

### CSV

```
plane_name,category,nation,rank,battle_rating,max_speed,turn_time,climb_rate,wing_rip_speed,combat_flap_rip_speed,image_url
A-10A,PREMIUM;Strike fighter,USA,VI,10.0,642,29.0,25.3,874,N/A,https://wiki.warthunder.com/images/thumb/0/08/GarageImage_A-10A.jpg/800px-GarageImage_A-10A.jpg
```

### JSON

```json
  {
    "plane_name": "A-10A",
    "category": "PREMIUM;Strike fighter",
    "nation": "USA",
    "rank": "VI",
    "battle_rating": 10.0,
    "max_speed": "642",
    "turn_time": "29.0",
    "climb_rate": "25.3",
    "wing_rip_speed": "874",
    "combat_flap_rip_speed": "",
    "image_url": "https://wiki.warthunder.com/images/thumb/0/08/GarageImage_A-10A.jpg/800px-GarageImage_A-10A.jpg"
  },
```

## How to run

### Activate conda environment (if using):

```sh
conda activate base
```

### Scrape the data:

```sh
python3 scrape_planes.py
```

This will save the data in CSV format in a file called raw-data.csv

### Clean the data and create a JSON copy

```sh
python3 clean_the_data.py
```

The original CSV file won't be overwritten or deleted. There will be a new file with cleaned plane names and a JSON file.

The original plane names have special characters that I wanted to remove.

[Page Top](#contents)
