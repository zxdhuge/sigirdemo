import urllib2
import sys
from get_information import get_item_specifics, get_items_by_keyword


def main(keyword):
	items = eval(get_items_by_keyword(keyword))
	if items["findItemsByKeywordsResponse"][0]["ack"][0] != "Success":
		print items
	else:
		for item in items["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
			print item["title"]

if __name__ == "__main__":
	main(sys.argv[1])

