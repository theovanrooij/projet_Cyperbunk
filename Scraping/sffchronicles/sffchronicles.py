# import
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options
import json
from lxml import etree
import time

# ouvrir web,je utilise Edge，打开无痕浏览器
options = Options()

options.add_argument('--incognito')


driver = webdriver.Edge(executable_path=r'E:\pycharm\pythonProject\msedgedriver', options=options)
driver.maximize_window()

time.sleep(1)
# 打开指定网页,Ouvrir la page spécifiée
driver.get('https://www.sffchronicles.com/search/174617/?page=1&q=cyberpunk&o=date')
time.sleep(1)
js = "window.open('http://www.sogou.com')"
time.sleep(1)
driver.execute_script(js)
time.sleep(1)
window = driver.window_handles
driver.switch_to.window(window[0])
time.sleep(1)

def funb():
    # Boucle morte，死循环，参考ipad笔记
    while True:
        try:
            # 这里点击下一页
            driver.find_element(By.XPATH, "//a[text()='Next']").click()
            funa()
            # 如果出现这个报错就直接关闭浏览器
        except NoSuchElementException:

            driver.close()
            time.sleep(1)
            driver.quit()
            time.sleep(1)

def funa():
    # Obtenir le code source web,这里获取网页源码--看知乎收藏爬虫第二个
    data = driver.page_source
    html = etree.HTML(data)
    # xpath get title,xpath，获取标题
    title = html.xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div/div/div[1]/ol/li[*]/div/div/h3/a')

    list1 = []
    # Couper la chaîne de titres ensemble，把标题字符串拼接起来
    for x in range(0, 20):
        ui = title[x].xpath('string(.)').strip()

        print(ui)
        list1.append(ui)

    # xpath获取每个名字,obtenir le nom
    name = html.xpath('//ul[@class="listInline listInline--bullet"]/li[1]//text()')
    lie = []
    # Récupérer chaque forum par son nom et l'ajouter à la liste,通过名字获取每个论坛并添加到列表内
    for a in name:
        name_ = html.xpath(f'//li[@data-author="{a}"]/div/div/div[2]/ul/li[*]/a/text()')
        name1 = name_[-1]
        lie.append(name1)
    print(lie, 'this is lie')
    print(name)
    # xpath获取每个发布时间,xpath obtient l'heure de chaque version
    time_ = html.xpath("//ul[@class='listInline listInline--bullet']/li[3]/time/text()")
    print(time_)

    list2 = []
    #  Obtenez chaque étiquette a et ensuite chaque lien，获取每个标签a然后获取每个链接

    for za in range(0, 21):
        links = driver.find_elements(By.XPATH, "//h3[@class='contentRow-title']/a")
        print(links)
        print('this is links')
        link = links[za]
        print(link)

        print('this is link')
        url = link.get_attribute('href')
        list2.append(url)
        print(list2)
        print(url)
        print('this is url')
        driver.get(url)
        time.sleep(1)
        # Obtenez le lien pour chaque boucle afin d'obtenir un clic circulaire，获取每次循环的链接实现循环点击进入
        data1 = driver.page_source
        html1 = etree.HTML(data1)
        window0 = driver.window_handles
        driver.switch_to.window(window0[1])
        time.sleep(1)
        driver.switch_to.window(window0[0])
        time.sleep(1)

        li = []
        li1 = []
        li1_ = []

        dict0 = []
        dict1 = {}
        test = html1.xpath("//div[@class='bbWrapper']/text()")

        message = html1.xpath("//section/div[3]/dl[2]/dd/text()")
        # dict_ = dict(message)
        for mess in message:

            li1_.append(mess)
        mess_ = str(li1_)
            # dict0['message'] = mess_
        li1.append(mess_)

        # Remplacer le début de chaque texte par un saut de ligne vers la ligne suivante，把每次的文本的\n替换成换行符换到下一行
        li_ = [x.strip() for x in test if x.strip() != '\n']
        print(li_)
        for lis_ in li_:
            dict0.append(lis_)
        # dict1['test'] = li_
        lis = str(dict0)
        li.append(lis)
        print(li)

        print(li1)
        # 以json形式按顺序写入文件，ecrit ficher par json
        with open('test4.json', 'a', encoding='utf-8')as fi:
            for zm in zip(list1, lie, time_, name, li1, li):
                item = {}
                ls = []
                item['title'] = zm[0]
                item['forum'] = zm[1]
                item['time'] = zm[2]
                item['name'] = zm[3]
                item['message'] = zm[4]
                item['test'] = zm[5]
                ls.append(item)
                str_data = json.dumps(ls, ensure_ascii=False, indent=2)
                fi.write(str_data + ",\n")
        # return dernier page,进行一次循环返回上一页
        driver.back()
        time.sleep(1)
        # delete,删除每次列表的第一个值
        list1.pop(0)
        lie.pop(0)
        time_.pop(0)
        name.pop(0)
        print(list1)
        print(lie)
        print(time_)
        print(name)
        # change a page prochain，当列表内长度为零，就点击下一页
        if len(list1) == 0:

            funb()


if __name__ == '__main__':
    funa()
