import os
import json
from bs4 import BeautifulSoup
import requests


class Child:
    def __init__(self, name: str, sex: str, age: str, personal_info_dict: dict, image_links_list: list):
        self.name = name
        self.sex = sex
        self.age = age
        self.personal_info_dict = personal_info_dict
        self.image_links_list = image_links_list

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def get_data(pageNo):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    r = requests.get(f'https://www.scallywags.co.uk/models/page/{pageNo}/', headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    persons_list = []

    for person in soup.findAll('div', attrs={'class': 'popup mfp-hide'}):
        name = person.find('h2', attrs={'class': 'title'}).get_text()
        sex = 'Private Profile'
        age = 'Private Profile'
        personal_info_dict = {}
        image_links_list = []
        if name != 'Private Profile':
            name = person.find('h2', attrs={'class': 'title'}).next_sibling.get_text()
            (sex, age) = person.find('span', attrs={'class': 'age'}).get_text().split(" - ")
        if name != 'Private Profile':
            for info in person.find('ul', attrs={'class': 'personal-info-list'}).findAll('li', attrs={}):
                personal_info_dict[info.get_text().split(':')[0]] = info.get_text().split(':')[1]
            for img in person.find_all('img', alt=True):
                image_links_list.append(img['src_old'])
        persons_list.append(Child(name=name, sex=sex, age=age, personal_info_dict=personal_info_dict,
                                  image_links_list=image_links_list))
    return persons_list


countPerson = 0
countPhotos = 0
MaxPhotos = 0

for page in range(1, 49):
    for person in get_data(page):
        if person.name != 'Private Profile':
            if not os.path.exists(f'../test0001/{person.name}'):
                os.system(f'mkdir -p "../test0001/{person.name}"')
                # with open('labels.txt', 'w') as f:
                #     f.write(labels)
                with open(f'../test0001/{person.name}/data.json', 'w') as write_file:
                    write_file.write(person.toJSON())
                countPerson += 1
            countPhotos += len(person.image_links_list)
            if MaxPhotos < len(person.image_links_list):
                MaxPhotos = len(person.image_links_list)
            for i, image_link in enumerate(person.image_links_list):
                os.system(f'wget -O "../test0001/{person.name}/{i}.jpg" {image_link}')

print('countPerson: ' + str(countPerson))
print('countPhotos: ' + str(countPhotos))
print('MaxPhotos: ' + str(MaxPhotos))
