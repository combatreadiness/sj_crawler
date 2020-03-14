from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


def findMyNews(press_name: "cnn", keywords: []) -> {}:
    with open('site_info.json') as json_file:
        json_data = json.load(json_file)
        try:
            website = json_data[press_name]["url"]
            link_url = json_data[press_name]["link_url"]
            title_tag = json_data[press_name]["title_tag"]
            title_class = json_data[press_name]["title_class"]

        except KeyError:
            print("I can't find your input in the Press List.")
            exit(1)
        my_news_list = {}

        html = urlopen(website)
        bsObject = BeautifulSoup(html, "lxml")
        results = bsObject.findAll(title_tag, class_=title_class)
        #print(results)
        for r in results:
            title = r.text
            for keyword in keywords:
                if keyword in title:
                    my_news_list[title] = [press_name,link_url + r.find('a').get('href')]
                    break
    return my_news_list


final_results=(findMyNews('fox', ["Trump"]))
for k,v in final_results.items():
    print(v[0],":",k)
