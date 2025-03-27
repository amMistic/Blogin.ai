from bs4 import BeautifulSoup
import requests
import logging
import json

class HVDiveScrapper:
    def __init__(self):
        self.url = "https://www.hrdive.com/"
        self.HEADERS = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.final_response = {}
    
    def run(self, max : int):
        logging.info('Requested to scrapped the data from platform..')

        # get the request
        response = requests.get(url=self.url, headers=self.HEADERS)
        if response.status_code == 200:
            logging.info('Request Accepted!')
            logging.info('Fetching Top Blogs on Human Resources...')
            soup = BeautifulSoup(response.text,'html.parser')

        #  *********************************** TOP STORIES ****************************************
            # find the section -- TOP STORIES
            top_stories = soup.find('section', class_='top-stories')
            top_hr_stories_topics = top_stories.find_all('h3')
            top_hr_stories_links = top_stories.find_all('a')
            
            top_stories_topics_links = []
            for i in range(len(top_hr_stories_topics)):
                top_stories_topics_links.append(
                   { 'title' : str(top_hr_stories_topics[i].get_text(strip=True)), 
                    'url' : str(top_hr_stories_links[i].get('href'))}
                )
            
            # update the final response
            self.final_response.update({
                'top_stories' : top_stories_topics_links
            })
        
        #  *********************************** LATEST STORIES ****************************************
            logging.info('Fetching Latest Blogs on Human Resources...')
            latest_stories = soup.find_all('li', class_="row feed__item")[:max]
            latest_stories_topics = []
            for story in latest_stories:
                title_div = story.find('div', class_ ="medium-8 columns")
                title = title_div.a.get_text(strip=True)
                link = title_div.a.get('href')
                latest_stories_topics.append({'title' :title, 'url' : link})
            
            
            # update the final response
            self.final_response.update({
                'latest_stories' : latest_stories_topics
            })

            logging.info('Data Scrapped Sucessfully!')
        
            # return 
            return self.final_response
        else:
            logging.error(f'Unable to get the request page. (Status Code: {response.status_code}')
            raise f'Unable to get the request page. (Status Code: {response.status_code})'
    
    
if __name__ == '__main__':
    scrapper = HVDiveScrapper()
    response = scrapper.run(max=5)
    
    print(json.dumps(response, indent=4))
        
        
        
        