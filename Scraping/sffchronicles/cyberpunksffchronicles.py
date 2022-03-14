import requests
from lxml import etree
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
def funa():
    global liq, l1, text,message, na, tl, da, forum, ui, data, list1, fum, name,t1l,t1, na1,tl1, x, item
    m = 0
    ll = []

    til = []
    list1 = []


    for ul in range(1, 11):
        url = f'https://www.sffchronicles.com/search/175402/?page={ul}&q=cyberpunk&o=date'
        response = requests.get(url, headers=headers).text
        # print(response)
        data = etree.HTML(str(response))
        href = data.xpath("//div[@class='contentRow-main']/h3[@class='contentRow-title']/a/@href")
        name = data.xpath('//ul[@class="listInline listInline--bullet"]/li[1]//text()')
        title = data.xpath("//div[@class='contentRow-main']/h3[@class='contentRow-title']/a")
        nl = len(name)
        # 把标题字符串拼接起来
        for x in range(0, nl):
            t1l = []
            ui = title[x].xpath('string(.)').strip()
            list1.append(ui)
        if m < nl:
            t1 = list1[m]
            m += 1

            t1l.append(t1)


            print(t1l, ':This is the title')
            # //li[@data-author="{a}"]/div/div/div[2]/ul/li[*]/a/text()
            # print(ui)


            # l1.append(list1[x])


        hl = len(href)
        for i in range(0, hl):
            fum = []
            na1 = []
            lik = []
            tl1 = []

            na = name[i]
            # print(na, '这是na')

            time1 = data.xpath(
                f'//li[@data-author="{na}"]/div/div/div[2]/ul/li[*]//text()')
            # print(time1)
            tl = time1[1]

            hrefs = data.xpath("//div[@class='contentRow-main']/h3[@class='contentRow-title']/a/@href")

            link = hrefs[i]
            lik.append(link)
            for lki in lik:

                lk = lki.split('/')
                # print(lk)
                liq = lk[-1]


            forum = data.xpath(f'//li[@data-author="{na}"]/div/div/div[2]/ul/li[*]/a/text()')


            response1 = requests.get('https://www.sffchronicles.com' + link).text
            da = etree.HTML(str(response1))
            # print(response1)
            na1.append(na)
            print(na1, 'NAME')
            til.append(tl)
            fu = forum[-1]
            fum.append(fu)
            text = da.xpath(f"//div[@data-lb-id='{liq}']/article[@class='message-body js-selectToQuote']/div[@class='bbWrapper']/text()")
            print(text)
            print('TEXT')
            message = da.xpath(f"//article[@data-content='{liq}']/div/div[1]/section/div[3]/dl[2]/dd/text()")
            print(message)
            print('This is number of message')
            print(fum)
            print('This is the address')
            tl1.append(tl)
            print(tl1, ':this is the time')
            item = {}
            for zm in zip(t1l, na1, til, fum, text, message):
                item['title'] = zm[0]
                item['name'] = zm[1]
                item['time'] = zm[2]
                item['forum'] = zm[3]
                item['text'] = zm[4]
                item['message'] = zm[5]
                ll.append(item)
                print(ll)
    with open('test2.json', 'a', encoding='utf-8')as fi:
        # for zm in zip(, na1, til, fum, text, message):
        str_data = json.dumps(ll, ensure_ascii=False)
        fi.write(str_data)


if __name__ == '__main__':
    funa()