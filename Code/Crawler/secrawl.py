from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys
from bs4 import BeautifulSoup
import json
import io
from tqdm import tqdm
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from selenium.webdriver.chrome.options import Options

Result = {}

def Search(Hypernym, Occupation):
    for k, vs in tqdm(Hypernym.items()):
        name = k.replace('_', '+')
        name = name.replace(' ', '+')
        if k.replace('_', ' ') not in Result:
            Result[k.replace('_', ' ')] = {}
        for occu in Occupation:
            if occu not in Result[k.replace('_', ' ')]:
                Result[k.replace('_', ' ')][occu] = []
            url = 'http://cn.bing.com/search?q=' + name + '+' + occu + '&first=20'
            # print(url)
            while True:
                try:
                    driver.get(url)
                    driver.find_element_by_id("est_en").click()

                    html = driver.page_source       # get html
                    page = BeautifulSoup(html, 'lxml')

                    ps = page.find_all(name='p')[:10]
                    for p in ps:
                        news = p.find(name='span', attrs={'class': 'news_dt'})

                        if news is not None:
                            news_text = news.text
                            p_text = p.text[len(news_text) + 3:]
                        else:
                            p_text = p.text
                        Result[k.replace('_', ' ')][occu].append(p_text)
                    if len(Result) % 20 == 0:
                        s = json.dumps(Result, indent=1)
                        with open('Result.json', 'w', encoding='utf-8') as fw:
                            fw.write(s)
                except NoSuchElementException as e:
                    continue
                break
    return Result

chrome_options = Options()
chrome_options.add_argument("--headless")       # define headless
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()     # 打开 Chrome 浏览器

with open('./Hypernym.json', 'r') as fr:
    Hypernym = json.load(fr)

Occupation = ['politics', 'religion', 'economy', 'nature',
              'society', 'humanity', 'engineering', 'culture', 'sports']

Search(Hypernym, Occupation)
