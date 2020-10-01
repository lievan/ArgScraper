# ArgScraper
Mines deliberation graphs from Debatepedia

Requirements: beautifulsoup4, numpy, pandas, requests, lxml, csv, json, re


# Mine Arguments

Initialize a list of links from debatepedia (links must be debate links, see link formatting below). Pass the list into get_arguments. get_arguments will automatically write a deliberation map (one per link specified) into a csv file and a json file.

```
from ArgScraper import ArgScraper

debate_topic_links = [ 
 'http://www.debatepedia.org/en/index.php/Debate:_Balanced_budget_amendment_to_US_Constitution',
 'http://www.debatepedia.org/en/index.php/Debate:_EU_elected_president',
 'http://www.debatepedia.org/en/index.php/Debate:_EU_federalism'
]

ArgScraper.get_arguments(debate_topic_links)
```

And you will see
```
{
	"type": "ISSUE",
	"name": "Is EU federalization a good idea? Should the EU become the United States of Europe?",
	"description": "",
	"children": [{
		"type": "IDEA",
		"name": "Is it justifiable to give away the national sovereignty of the European states?",
		"description": "",
		"children": [{
			"type": "PRO",
			"name": "National sovereignty is a relic.",
			"description": "At the time of globalization, at the time when international relations are becoming more and more complicated, the view of state sovereignty  - the supremacy of political power a nation has over its own actions - is eroding as our elected leaders are giving away their nations' sovereignty by placing more and more authority in supranational organizations like the UN which are not accountable to voters. New international actors have risen as a result of improved communications and transportation. Multiple channels of communications, which involve numerous transnational alliances, are making the essential borders of sovereignty obsolete.",
			"children": []
		}
  ...
```
