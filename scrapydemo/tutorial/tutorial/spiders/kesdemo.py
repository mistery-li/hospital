# -*- coding:utf-8 -*-

import scrapy

from tutorial.items import hospital_mes
import re
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

class keshidemo(scrapy.Spider):
    name = 'kesdemo'
    #   入口
    allowed_domains = ['yuyue.shdc.org.cn']
    start_urls = ['http://yuyue.shdc.org.cn/']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.get_hospital)

    def get_hospital(self, response):
        hospitals = response.xpath('//*[@id="fl_yiyuan_nr"]//div/ul/li/a')

        # 医院名字,请求参数
        for hospital in hospitals:
            for param in hospital.xpath('@onclick').extract():
                param = param.replace('\r\n', '').replace('\t', '')
                isSpTime = self.re_param(r'isSpTime:\'(.+?)\'', param, 1)
                platformHosId = self.re_param(r'platformHosId:\'(.+?)\'', param, 1)
                hosOrgCode = self.re_param(r'hosOrgCode:\'(.+?)\'', param, 1)
                paymode = self.re_param(r'paymode:\'(.+?)\'', param,1)
                orgname = self.re_param(r'orgname:\'(.+?)\'', param, 1)
                is_exclusive = self.re_param(r'is_exclusive:\'(.+?)\'', param,1)
                url = 'http://yuyue.shdc.org.cn/' + self.re_param(r'searchDeptmentAction.action', param, 0)
                item = hospital_mes()
                item['isSpTime'] = isSpTime
                item['platformHosId'] = platformHosId
                item['hosOrgCode'] = hosOrgCode
                item['paymode'] = paymode
                item['hospitalname'] = orgname
                item['is_exclusive'] = is_exclusive
                item['url'] = url
                item['url'] = url
                url = item['url']
                yield scrapy.FormRequest(url, formdata={
                    'isSpTime': item['isSpTime'],
                    'platformHosId': item['platformHosId'],
                    'hosOrgCode': item['hosOrgCode'],
                    'paymode': item['paymode'],
                    'orgname': item['hospitalname'],
                    'is_exclusive': item['is_exclusive'],
                },meta={'item' : item}, callback=self.get_keshi_mes)

                # break 调试
            #     break
            # break


    #   获取请求参数
    def re_param(self, rege, url, position=0):
        pattern = re.compile(rege)
        matcher = re.search(pattern, url)
        new_param = matcher.group(position)
        return new_param

    def get_keshi_mes(self, response):
        item = response.meta['item']
        keshi = response.xpath('//*[@class="xuanze_keshi"]/ul/li/a/@onclick').extract()
        hospital_descriptions = response.xpath('//*[@class="jieshao_zi"]')
        for hospital_description in hospital_descriptions:
            item['level'] = hospital_description.xpath('p[2]/text()').extract_first()
            item['phone'] = hospital_description.xpath('p[3]/text()').extract_first()
            item['address'] = hospital_description.xpath('p[4]/text()').extract_first()
        for keshi in keshi:
            keshi = keshi.replace('\r\n', '').replace('\t', '').strip()
            item['keshi'] = self.re_param(r'tempDeptName:\'(.+?)\'', keshi, 1)
            item['keshi_hospital'] = self.re_param(r'orgname:\'(.+?)\'', keshi, 1)
        # 请求医生参数
        for doctor_request in response.xpath('//*[@class="xuanze_keshi"]/ul/li/a/@onclick').extract():
            doctor_request.replace('\r\n', '').replace('\t', '')
            platformDeptId = self.re_param(r'platformDeptId:\'(.+?)\'', doctor_request, 1)
            deptname = self.re_param(r'tempDeptName:\'(.+?)\'', doctor_request, 1)
            deptname = deptname.encode('utf8')
            url = 'http://yuyue.shdc.org.cn/ajaxSearchExpert.action'
            yield scrapy.FormRequest(url, formdata={
                'platformHosId': item['platformHosId'],
                'platformDeptId': platformDeptId,
                'platformDoctorId': '',
                'nextNumInfo' : '0',
                'deptname' : deptname,
                'visitLevelCode' : '1',

            }, meta={'item': item},callback=self.doctor_mes)

                # 调试
            # break

    def doctor_mes(self, response):
        item = response.meta['item']
        doctors = response.xpath('//*[@class="f16"]/a/@onclick').extract()
        if doctors != []:
            for doctor in doctors:
                doctor.replace('\r\n', '').replace('\t', '')
                item['doctorname'] = self.re_param(r'doctName:\'(.+?)\'', doctor, 1)
                item['workkeshi'] = self.re_param(r'deptName:\'(.+?)\'', doctor, 1)
                # item['description'] = self.re_param(r'specialty:\'(.+?)\'', doctor, 1)
                # item['worklevel'] = self.re_param(r'visitLevel:\'(.+?)\'', doctor, 1)
                item['hospital'] = self.re_param(r'orgname:\'(.+?)\'', doctor, 1)
            return item
