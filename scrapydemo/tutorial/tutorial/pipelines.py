# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WebcrawlerScrapyPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',db='testdb',user='root',passwd='root',charset='utf8',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            use_unicode=False)
        self.set_hospital = set()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        # if item['hospitalname'] in self.set_hospital:
        #     raise DropItem("Duplicate item found: %s" % item)
        # else:
        #     self.set_hospital.add(item['hospitalname'])
        return item

    def _conditional_insert(self, tx, item):
        if item['hospitalname'] in self.set_hospital:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.set_hospital.add(item['hospitalname'])
            hospital = "insert into hospital(name,isSpTime,platformHosId,hosOrgCode,paymode,is_exclusive,url)values(%s,%s,%s,%s,%s,%s,%s)"
            params = (item['hospitalname'], item['isSpTime'], item['platformHosId'], item['hosOrgCode'], item['paymode'],
                            item['is_exclusive'], item['url'])
            tx.execute(hospital, params)


class keshi_pipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='testdb', user='root', passwd='root', charset='utf8',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            use_unicode=False)
        self.set_keshi = set()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_keshi, item)

        return item

    def _insert_keshi(self, tx, item):
        if item['keshi'] in self.set_keshi:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.set_keshi.add(item['keshi'])
            keshi = "insert into keshi(name,hospital,level,phone,address)values(%s,%s,%s,%s,%s)"
            keshiparam = (item['keshi'],item['keshi_hospital'], item['level'], item['phone'], item['address'])
            tx.execute(keshi, keshiparam)


class doctor_pipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',db='testdb',user='root',passwd='root',charset='utf8',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            use_unicode=False)
        self.set_doctor = set()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_doctor, item)

        return item


    def _insert_doctor(self, tx, item):
        if item['doctorname'] in self.set_doctor:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.set_doctor.add(item['doctorname'])
            doctor = "insert into doctor (name,hospital,workkeshi,address,level,phone)values(%s,%s,%s,%s,%s,%s)"
            doctorparam = (item['doctorname'], item['hospital'], item['workkeshi'],item['address'], item['level'], item['phone'])
            tx.execute(doctor, doctorparam)