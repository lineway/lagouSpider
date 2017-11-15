# coding: utf-8
import time
import requests
from bs4 import BeautifulSoup
import pymongo
import multiprocessing

conn = pymongo.MongoClient('localhost', 27017)
db = conn.go_db
work_detail = db.work_detail

headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    'Cookie':
    'user_trace_token=20171111180708-13cd9a85-c6c8-11e7-892a-525400f775ce; LGUID=20171111180708-13cd9df9-c6c8-11e7-892a-525400f775ce; TG-TRACK-CODE=search_banner; JSESSIONID=ABAAABAAAIAACBI31774B722C9481A56A3EC1D0DBE7B827; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FfilterOption%3D3; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; X_HTTP_TOKEN=9e6943684079336a99903063bd8c501d; _putrc=D20F2F8BD51E8055; login=true; unick=%E5%BC%A0%E4%B8%80%E9%93%AD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510394829; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510424706; _gid=GA1.2.2025569608.1510394829; _ga=GA1.2.694666877.1510394829; LGSID=20171112021831-b90b7f83-c70c-11e7-898f-525400f775ce; LGRID=20171112022505-a3f48f81-c70d-11e7-8990-525400f775ce; SEARCH_ID=d56180577ef04ccb8e2e9166c8c59597; index_location_city=%E5%85%A8%E5%9B%BD',
    'Referer':
    'https://www.lagou.com/jobs/list_Python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
    'Host':
    'www.lagou.com',
    'X-Anit-Forge-Code':
    '0',
    'X-Anit-Forge-Token':
    None,
    'X-Requested-With':
    'XMLHttpRequest'
}

main_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'


def get_work_id(url, headers=headers, number=31, position='go'):
    work_id = []
    for nu in xrange(1, number):
        form_data = {'first': True, 'pn': nu, 'kd': position}
        web_data = requests.post(main_url, headers=headers, data=form_data)
        data = web_data.json()['content']
        work_list = data['positionResult']['result']
        for i in work_list:
            print i
            work_id.append(i['positionId'])
        time.sleep(0.5)
    return work_id


def get_detail_info(work_id):
    for detail_id in work_id:
        url = 'https://www.lagou.com/jobs/{}.html'.format(detail_id)
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        name = soup.select(
            'body > div.position-head > div > div.position-content-l > div > span'
        )
        company = soup.select('#job_company > dt > a > div > h2')
        info = soup.select(
            'body > div.position-head > div > div.position-content-l > dd > p > span'
        )
        description = soup.select('#job_detail > dd.job_bt')

        data = {
            'name': name[0].text,
            'company': company[0].text,
            'salary': info[0].text,
            'city': info[1].text,
            'workYear': info[2].text,
            'education': info[3].text,
            'jobNature': info[4].text,
            'description': description[0].text
        }
        print data
        db.work_detail.save(data)
    print 'over'


if __name__ == '__main__':
    work_id = get_work_id(main_url)
    # print get_detail_info(work_id)
    p = multiprocessing.Pool(8)
    p.apply_async(get_detail_info(work_id))
    p.close()
    p.join()