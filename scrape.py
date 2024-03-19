from selenium import webdriver
from selenium.webdriver.common.by import By
import json

class DPAC_Parser():
    def __init__(self, url="https://performingarts.nd.edu/events/"):
        self.url = url
    
    def update(self) -> int:
        driver = webdriver.Chrome()         # Scrapes main page
        driver.get(self.url)

        detail_driver = webdriver.Chrome()  # Scrapes detail page for each event

        data = []                           # Store scraped information

        # Get event divs from main events page
        events = list(driver.find_elements(By.CLASS_NAME, "event-block-innerwrap"))

        for event in events:
            # Obtain basic event information
            title = event.find_element(By.CLASS_NAME, "title").text
            date = event.find_element(By.CLASS_NAME, "date").text
            genre = event.find_element(By.CLASS_NAME, "event-genre").text
            image = event.find_element(By.CLASS_NAME, "event-image")
            image_url = image.get_attribute("data-src")

            # Search event details page for extra information
            detail_url = event.find_element(By.CLASS_NAME, "link").get_attribute("href")

            detail_driver.get(detail_url)
            time = detail_driver.find_element(By.CSS_SELECTOR, ".event-date-time > strong").text
            location = detail_driver.find_element(By.CSS_SELECTOR, ".hero-text > p > a").text
            description = detail_driver.find_element(By.CSS_SELECTOR, ".event-description").text

            # Keep track of event information
            data.append(
                {
                    'title': title,
                    'date': date,
                    'genre': genre,
                    'image_url': image_url,
                    'time': time,
                    'location': location,
                    'description': description,
                    'link': detail_url
                }
            )

        # Write to "database" file
        with open('db.json', 'w') as out:
            out.write(json.dumps(data, indent=4)) 

        # Return number of events
        return len(data)
    
if __name__ == '__main__':
    parser = DPAC_Parser()
    num_events = parser.update()
    print(f'{num_events} saved')