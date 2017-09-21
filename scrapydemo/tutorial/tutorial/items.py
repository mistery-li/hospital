# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class hospital_mes(scrapy.Item):
    hospitalname = scrapy.Field()
    platformHosId = scrapy.Field()  # 发送的id
    isSpTime = scrapy.Field()
    hosOrgCode = scrapy.Field()
    paymode = scrapy.Field()
    is_exclusive = scrapy.Field()
    url = scrapy.Field()
    keshi = scrapy.Field()  # 所有科室
    keshi_hospital = scrapy.Field()
    address = scrapy.Field()
    level = scrapy.Field()
    phone = scrapy.Field()
    # 医生信息字段
    doctorname = scrapy.Field()
    hospital = scrapy.Field()
    workkeshi = scrapy.Field()   #所在医院科室






