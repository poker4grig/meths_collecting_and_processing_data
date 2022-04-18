from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy_1804

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = \
                self.process_salary_hh(item['salary'])
            del item['salary']
        elif spider.name == 'superjob':
            item['min_salary'], item['max_salary'], item['currency'] = \
                self.process_salary_superjob(item['salary'])
            del item['salary']

        collection = self.mongobase[spider.name]
        if collection.find_one({'link': item['url']}):
            print(f'Document with url = {item["url"]} already exist')
        else:
            collection.insert_one(item)
            print(f'Insert link {item["url"]} complete')
        return item

    def process_salary_hh(self, salary):
        for n, elem in enumerate(salary):
            salary[n] = elem.strip().replace("\xa0", '')
        if salary[0] == 'до':
            max_salary = int(salary[1])
            vacancy_salary_min = None
            currency = salary[3]
        elif salary[0] == 'от':
            min_salary = int(salary[1])
            if salary[2] == 'до':
                max_salary = int(salary[3])
                currency = salary[5]
            else:
                max_salary = None
                currency = salary[3]
        else:
            min_salary = None
            max_salary = None
            currency = None
        return min_salary, max_salary, currency

    def process_salary_superjob(self, salary):
        for n, elem in enumerate(salary):
            salary[n] = elem.strip().replace("\xa0", '')
        if salary[0] == 'от':
            min_salary = int(salary[2][:-4])
            max_salary = None
            currency = salary[2][-4:]
        elif salary[0] == 'до':
            min_salary = None
            max_salary = int(salary[2][:-4])
            currency = salary[2][-4:]
        elif len(salary) > 4:
            min_salary = int(salary[0])
            max_salary = int(salary[4])
            currency = salary[6]
        elif len(salary) == 3:
            min_salary = int(salary[0])
            max_salary = int(salary[0])
            currency = salary[2]
        else:
            min_salary = None
            max_salary = None
            currency = None
        return min_salary, max_salary, currency
