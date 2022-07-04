#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import re
import time


from WebCraw import WebRequest
from SqlDBS import MySqlSys as sql
from Phrases import WordStatistic
from DataImporter import Word2Vector, DataLoader
from Algorithm.NBayes import NBayesClassifier, MultiNBayesClassifier
from Algorithm import NBayes


class movie(object) :

    tempalte = 'https://movie.douban.com/subject/{0}/comments?status=P'

    class sort() :
        hot = '&sort=new_score'
        time = '&sort=time'

    class type() :

        bad = '&percent_type=l'
        good = '&percent_type=h'

    def __init__(self, id) :

        self.id = id

    def getName(self) :

        response = WebRequest.get(self.tempalte.format(self.id))

        if (response.status_code != 200):

            raise Exception('Net Exception Code:{0}'.format(response.status_code))

            return -1

        data = WebRequest.selectElement(response.text,
                                        '#content > h1')

        result = data[0].get_text()

        result = re.findall('(.*) 短评', result)[0]

        return result

    def getType(self) :

        response = WebRequest.get('https://movie.douban.com/subject/{0}/'.format(self.id))

        if (response.status_code != 200):

            raise Exception('Net Exception Code:{0}'.format(response.status_code))

            return -1

        data = WebRequest.selectElement(response.text,
                                        '#info > span')

        result = []

        for i in data :

            if('property' in i.attrs and i.attrs['property'] == 'v:genre') : result.append(i.get_text().strip())

        return result

    def getDesc(self) :

        response = WebRequest.get('https://movie.douban.com/subject/{0}/'.format(self.id))

        if (response.status_code != 200):

            raise Exception('Net Exception Code:{0}'.format(response.status_code))

            return -1

        data = WebRequest.selectElement(response.text,
                                        '#link-report > span')

        result = data[0].get_text().strip()

        return result


    def getComments(self, offset, sort = '', type = '') :

        response = WebRequest.get(self.tempalte.format(self.id) + type + sort + '&start={0}'.format(offset))

        print(self.tempalte.format(self.id) + type + sort + '&start={0}'.format(offset))

        if (response.status_code != 200) :
            raise Exception('Net Exception Code:{0}'.format(response.status_code))

            return -1

        data = WebRequest.selectElement(response.text,
                                        '#comments > div > div.comment > p > span')

        result = []

        i = 0

        while(i < len(data)) :

            data2 = WebRequest.selectElement(response.text, '#comments > div:nth-child({0}) > div.comment > h3 > span.comment-info > span'.format(i + 1))

            if(len(data2) != 3) :

                i += 1

                continue

            result.append({
                "rating" : int(re.findall('\d+', data2[1]['class'][0])[0]),
                "text" : data[i].get_text()
            })

            i += 1;

        return result

    def _getCommentsAmount(self, response) :

        data = WebRequest.selectElement(response.text, '#content > div > div.article > div.clearfix.Comments-hd > ul > li.is-active > span')

        result = data[0].get_text()

        result = int(re.findall('(\d+)', result)[0])

        return result

    def getCommentsAmount(self) :

        response = WebRequest.get(self.tempalte.format(self.id))

        if(response.status_code != 200) :

            raise Exception('Net Exception Code:{0}'.format(response.status_code))

            return -1

        data = WebRequest.selectElement(response.text, '#content > div > div.article > div.clearfix.Comments-hd > ul > li.is-active > span')

        result = data[0].get_text()

        result = int(re.findall('(\d+)', result)[0])

        return result


