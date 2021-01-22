import requests, json

class jasoseolScraper:
    def __init__(self):
        self.CALENDAR_URL = "https://jasoseol.com/employment/calendar_list.json"
        self.EMPLOYMENT_URL = "https://jasoseol.com/employment/get.json"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
    
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
        