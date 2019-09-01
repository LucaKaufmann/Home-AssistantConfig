from bs4 import BeautifulSoup
import regex as re
import requests
# Here, we're just importing both Beautiful Soup and the Requests library
page_link = 'https://www.wowhead.com/news=294747/classic-wow-server-queue-times-eu'
# this is the url that we've already determined is safe and legal to scrape from.
page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library
page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.
textContent = []
div = str(page_content.find_all("div", class_="news-post-content"))
# In my use case, I want to store the speech data I mentioned earlier.  so in this example, I loop through the paragraphs, and push them into an array so that I can manipulate and do fun stuff with the data.
# result = re.search("(?<=(\[td\]Gehennas\[\\\/td\]\[td align=center\]\[span class=icon-rated(up|down)\]\[\\\/span\])).+?(?=\[\\\/td\])", div)
result2 = re.search("(?<=(\[td\]Gehennas\[\\\/td\]\[td align=center\]\[span class=icon-rated(up|down)\]\[\\\/span\].*\[\\\/td\]\[td align=center\])).+?(?=\[\\\/td\]\[\\\/tr\])", div)
# print(result.group(0))
print(result2.group(0))