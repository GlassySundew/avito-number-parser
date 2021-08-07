#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://chrome.google.com/webstore/detail/export-historybookmarks-t/dcoegfodcnjofhjfbhegcgjgapeichlf?hl=en

import requests
from bs4 import BeautifulSoup
import csv
import os
import bot
from tkinter import *
from tkinter import messagebox as mb



def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all(
        'a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)
    # find('div', )

    # find_all


def write_csv(data):

    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(
            (data['title'], data['price'], data['metro'], data['url'], data['number']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='catalog-list').find_all('div',
                                                           class_='item_table')
    for ad in ads:
        name = ad.find('div',
                       class_='description').find('h3').text.strip().lower()

        try:
            title = ad.find('div',
                            class_='description').find('h3').text.strip()
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ad.find(
                'div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''

        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''

        try:
            metro = ad.find('div',
                            class_='data').find_all('p')[-1].text.strip()
        except:
            metro = ''
            
           
           
        try:
            number = bot.Bot().parse(url)
            print(number)
        except:
            number = ''

        data = {
            'title': title,
            'price': price,
            'metro': metro,
            'url': url
            # 'number': number
        }

        write_csv(data)


def main():
    def check():
        url = entry.get()
        entry.delete(0, END)
        base_url = url.split('?')[0] + '?'
        page_part = 'p='
        query_part = '&' + url.split('?')[1]
        total_pages = get_total_pages(get_html(url))

        for i in range(1, total_pages):
            url_gen = base_url + page_part + str(i) + query_part
            html = get_html(url_gen)
            get_page_data(html)

    root = Tk()
    root.minsize(500, 200)
    entry = Entry(width=80)
    entry.pack(pady=20)
    Button(text='Парсить', command=check).pack()
    root.mainloop()

    # url = 'https://www.avito.ru/krasnodarskiy_kray/ptitsy?q=%D0%BA%D1%83%D1%80%D0%B8%D1%86%D1%8B'


if __name__ == '__main__':
    if os.path.exists('avito.csv'):
        os.remove("avito.csv")

    main()