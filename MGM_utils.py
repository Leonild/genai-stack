from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from webdriver_manager.chrome import ChromeDriverManager

def get_webpage_with_selenium(url):
    # Setup Selenium to use Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # Waiting for the page to load dynamically generated content
    try:
        element_present = EC.presence_of_element_located((By.ID, 'SomeId'))
        WebDriverWait(driver, 10).until(element_present)
    except:
        pass  # Just proceed if the specific element isn't found within 10 seconds

    html_content = driver.page_source
    driver.quit()
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    return html_content

def convert_to_json(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    questions = soup.select('a.faq-question')
    answers = soup.select('div.faq-answer')

    if not questions or not answers:
        return {}

    faq_list = []
    count_ID = 0
    for q, a in zip(questions, answers):
        question_id = "Aria" + str(count_ID)
        question_data = {
            'question_id': question_id,
            'title': q.get_text(strip=True),
            'body': q.get_text(strip=True),
            'tags': ["Aria Hotel", "Aria Resort", "Aria MGM Resorts"],  # If there are tags related to the questions, fill them in here
            'answers': [{
                'answer_id': hash(a.get_text(strip=True)),  # Using hash of answer text as a unique ID
                'is_accepted': True,  # Adjust as necessary
                'body_markdown': a.get_text(strip=True),
                'embedding': None  # Adjust as necessary
            }]
        }
        faq_list.append(question_data)
        count_ID = count_ID + 1

    return faq_list
