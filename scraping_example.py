import os
import requests
import BeautifulSoup

if not os.path.exists('output'):
    os.makedirs('output')

request_log_file = open('output/presidency_platforms_scraping.log', 'w')
request_log_file.write('Timestamp\tURL\tStatus Code\n')

print 'Starting scraping.'
for link in valid_links:
    r = requests.get(link)
    request_event_string = '{time}\t{link}\t{status}\n'.format(time=datetime.isoformat(datetime.now()), link=link, status=r.status_code)
    request_log_file.write(request_event_string) # Note I had to add the line ending "\n" above
    
    soup = BeautifulSoup(r.text)
    all_p_tags = soup.findAll('p')
    filename = link.split('/')[-1].split('=')[-1] + '.txt'
    filename_path = os.path.join('output', filename)
    
    with open(filename_path, 'w') as scraped_text_outfile:
        text_as_list_of_strings = [p.get_text() for p in all_p_tags]
        scraped_text = ''.join(text_as_list_of_strings)
        scraped_text_outfile.write(scraped_text.encode('utf8')) 
        # Encoding is hard!  Why did I do this?  Hint: check "import sys; sys.stdout.encoding"
request_log_file.close()
print 'Finished scraping.'