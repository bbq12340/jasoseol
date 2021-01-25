import requests, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class jasoseolScraper:
    def __init__(self):
        self.CALENDAR_URL = "https://jasoseol.com/employment/calendar_list.json"
        self.EMPLOYMENT_URL = "https://jasoseol.com/employment/get.json"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        self.browser = self.start_browser()
        self.wait = WebDriverWait(self.browser, 30)
    
    def extract_calendar_list(self, fromDate, toDate):
        payload = {
            "end_time": toDate+"T15:00:00.000Z",
            "start_time": fromDate+"T15:00:00.000Z"
        }
        r = requests.post(self.CALENDAR_URL, data=payload, headers=self.headers).json()
        id_list = []
        for e in r['employment']:
            id_list.append(e['id'])
        return id_list
    
    def extract_employment_json(self, id):
        payload = {
            "employment_company_id": id
        }
        r = requests.post(self.EMPLOYMENT_URL, data=payload, headers=self.headers).json()
        # with open ("employment.json", "w", encoding="utf-8-sig") as f:
        #     f.write(json.dumps(r, indent=4, sort_keys=True, ensure_ascii=False))
        return r
    
    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        return browser
    
    def extract_employment_popup(self, id):
        POPUP_URL = f"https://jasoseol.com/recruit/{id}"
        RESUME = By.CLASS_NAME, "write-resume"
        self.browser.get(POPUP_URL)
        self.wait.until(EC.presence_of_element_located(RESUME))
        html = self.browser.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        resume = soup.find('div',{'class':'write-resume'})
        # print(resume)
        # resume = r.html.find('.write-resume', first=True).html
        rows = resume.find_all('tr')
        employments = [ t.find('td').text for t in rows ]
        employments = (',').join(list(dict.fromkeys(employments)))
        return employments
