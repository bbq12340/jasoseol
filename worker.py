import time, json

from PySide6.QtCore import QThread, QObject, Signal

from jasoseolScraper import jasoseolScraper

class Worker(QObject):
    finished = Signal()
    progress = Signal(float)

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def run(self):
        # """Long-running task."""
        # for i in range(100):
        #     time.sleep(1)
        #     self.progress.emit(i + 1)
        # self.finished.emit()
        app = jasoseolScraper()
        extracted={}
        id_list=app.extract_calendar_list(self.date_from, self.date_to)
        for id in id_list:
            print(f'{id_list.index(id)+1} - {id}')
            time.sleep(1)
            data = app.extract_employment_json(id)
            end_time = data['end_time'].split('T')[0].replace('-','')
            url = data['employment_page_url']
            name = data['name']
            try:
                employments = app.extract_employment_popup(id)
                extracted[f'{end_time}'].update({f'{name}({employments})': url})
            except KeyError:
                extracted[f'{end_time}'] = {}
                extracted[f'{end_time}'].update({f'{name}({employments})': url})
            except:
                continue
            if "신입" in employments or not employments:
                extracted[f'{end_time}'][f'{name}'] = extracted[f'{end_time}'].pop(f'{name}({employments})')
            with open('result.json', 'w', encoding='utf-8-sig') as f:
                f.write(json.dumps(extracted, sort_keys=True, indent=4, ensure_ascii=False))
