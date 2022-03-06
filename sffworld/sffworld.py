import requests
from lxml import etree
import json
import threading

# 线程锁 lock
Lock = threading.Lock()

# json数据
json_data = []

# 记录爬取过的网址 write process
old = []

# 请求头
headers = {
    'authority': 'www.sffwoaaaaaam',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': '_ga=GA1.2.120231870.1644871883; _gid=GA1.2.1039629421.1644871883; __gads=ID=eafa065113eb0639-227280d89fd000b6:T=1644871881:RT=1644871881:S=ALNI_MYdYvhuLRq3bNPjUl4FKHVzubMXCg; 93bedc3a83e7cc930f7acd424ef9ad82=1644871881; xf_csrf=1YA0XU4O6Z5K0eWk; _gat_gtag_UA_8006732_1=1',
}

# 网址映射对应页数  Nombre de pages correspondant au mappage de l'URL
website_dict = {}
website_dict['https://www.sffworld.com/forum/board/fantasy-horror.6/page-'] = 568
website_dict['https://www.sffworld.com/forum/board/science-fiction.7/page-'] = 283
website_dict['https://www.sffworld.com/forum/board/general-fiction.45/page-'] = 27

# 爬取函数，传入网址  Fonction Crawl, passer dans l'URL
def crawl(url, headers):
    global json_data
    # 请求详情数据进行解析   Demande de données détaillées pour l'analyse syntaxique
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=6)
            break
        except:
            pass
    html = etree.HTML(response.text)
    text = html.xpath("//*[@class='message-body js-selectToQuote']")[0].xpath("string()").strip()
    # 看关键词是否包含  Voir si le mot clé contient
    xxx = '—cyberpunk\n— Dystopia\n— Future\n— black novel\n— Cyberspace\n— Cybernetics\n— Scifi\n— retrofuturism\n— William Gibson\n— Stephenson\n— Richard Morgan\n— Bruce Sterling\n— Neuromancer'
    for key in [i.replace('—', '').strip() for i in xxx.split('\n')]:
        if key in text:
            # 写入数据结束  Fin de l'écriture des données
            # 解析数据   Analyse syntaxique des données
            username = html.xpath("//*[@class='username ']")[0].xpath("string()").strip()
            date = html.xpath("//time")[0].xpath("string()").strip()
            title = html.xpath("//*[@class='p-title-value']")[0].xpath("string()").strip()
            reply = ele.xpath(".//*[@class='pairs pairs--justified']//dd")[0].xpath("string()").strip()
            liulan = ele.xpath(".//*[@class='pairs pairs--justified structItem-minor']//dd")[0].xpath(
                "string()").strip().replace('K', '000').replace('.', '')
            neirong = text
            # 插入json
            data = {}
            data['username'] = username
            data['date'] = date
            data['title'] = title
            data['replies'] = reply
            data['views'] = liulan
            data['text'] = neirong
            json_data.append(data)
            Lock.acquire()
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f)
            Lock.release()
            break

# 遍历网址和总页数  Traversée des URLs et nombre total de pages
for web, totalpage in website_dict.items():
    # 遍历页数
    for page in range(1, totalpage):
        # 请求列表页解析
        while True:
            try:
                response = requests.get(web + str(page), headers=headers, timeout=6)
                break
            except:
                pass
        html = etree.HTML(response.text)
        eles = html.xpath("//*[contains(@class, 'structItem structItem--thread js-inlineModContainer')]")
        # urls = ['https://www.sffworld.com' + i for i in html.xpath("//*[@class='structItem-title']/a/@href")]
        # 遍历列表节点
        for ele in eles:
            # 提取url
            url = 'https://www.sffworld.com' + ele.xpath(".//*[@class='structItem-title']/a/@href")[0]
            # 爬过跳过
            if url in old:
                continue
            old.append(url)
            print('正在爬取页数', page, '有效数量', len(json_data), url)
            # crawl(url, headers)
            threading.Thread(target=crawl, args=(url, headers)).start()
            # 大于500条结束爬取
            if len(json_data) > 500:
                break
        # 大于500条结束爬取
        if len(json_data) > 500:
            break
    # 大于500条结束爬取
    if len(json_data) > 500:
        break

input()