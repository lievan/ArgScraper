# ArgScraper
Mines deliberation graphs from Debatepedia

Requirements: beautifulsoup, numpy, pandas, requests, lxml, csv, json, re


# Mine Arguments

Initialize a list of links from debatepedia (links must be debate links, see link formatting below). Pass the list into get_arguments. get_arguments will automatically write a deliberation map (one per link specified) into a csv file and a json file.

```
debate_topic_links = [ 
 'http://www.debatepedia.org/en/index.php/Debate:_Balanced_budget_amendment_to_US_Constitution',
 'http://www.debatepedia.org/en/index.php/Debate:_EU_elected_president',
 'http://www.debatepedia.org/en/index.php/Debate:_EU_federalism'
]

get_arguments(debate_topic_links)
```
