import os
import requests
from datetime import datetime
from BeautifulSoup import BeautifulSoup

print 'Started scraping.'

presidency_platforms_url = 'http://www.presidency.ucsb.edu/platforms.php'

r = requests.get(presidency_platforms_url)
soup = BeautifulSoup(r.text)

all_links = []
for link in soup.findAll('a'):
    all_links.append(link.get('href'))

valid_links = []
for link in all_links:
    final_url_element = link.split('/')[-1]
    if final_url_element.startswith('index.php?'):
       valid_links.append(link)

if not os.path.exists('output'):
    os.makedirs('output')

request_log_file = open('output/presidency_platforms_scraping.log', 'w') 
# Not really great to do this out of the loop. Forces Python to keep the file open.  Could do in loop and use write-mode 'a' for append instead.
# However, then you'd have to do a test to see if the file existed, so that it is created if not exists and writes header if it's the first time opened.
request_log_file.write('Timestamp\tURL\tStatus Code\n')

for link in valid_links:
	link_r = requests.get(link)
	request_event_string = '{time}\t{link}\t{status}\n'.format(time=datetime.isoformat(datetime.now()), link=link, status=link_r.status_code)
	request_log_file.write(request_event_string) # Note I had to add the line ending "\n" above
    
	page_soup = BeautifulSoup(link_r.text)
	all_p_tags = page_soup.findAll('p')
	filename = link.split('/')[-1].split('=')[-1] + '.txt'
	filename_path = os.path.join('output', filename)
   	
	text_as_list_of_strings = []
	for p in all_p_tags:
		if not p.string is None:
			text_as_list_of_strings.append(p.string)
	#text_as_list_of_strings = [p.get_text() for p in all_p_tags]
	scraped_text = ''.join(text_as_list_of_strings)

	with open(filename_path, 'w') as scraped_text_outfile:
		scraped_text_outfile.write(scraped_text.encode('utf8')) 
		# Encoding is hard!  Why did I do this?  Hint: check "import sys; sys.stdout.encoding
		# Also, try writing a line to request_log_file that indicates whether the file was successfully written.

request_log_file.close()

print 'Finished scraping.'
