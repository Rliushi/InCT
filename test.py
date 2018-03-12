# coding:utf-8

import urllib.request
import re
import collections
import json


# <td class="cxxt-title">   </td>
def getHtmlContent(url):
    page = urllib.request.urlopen(url)
    return bytes.decode(page.read(), encoding='utf-8')


def getDetailInfo(page, page_num):
    detail_main = list()
    break_flag = False
    res_tr = r'<td class="cxxt-title">(.*?)</td>'
    m_tr = re.findall(res_tr, page, re.S | re.M)
    res_tr = r'<td class="text-left cxxt-holdtime">(.*?)</td>'
    m_tr_time = re.findall(res_tr, page, re.S | re.M)
    if len(m_tr) == 0:
        break_flag = True
        return break_flag
    for idx in range(len(m_tr)):
        res_tr = r'title="(.*?)"'
        tmp_info = re.findall(res_tr, m_tr[idx], re.S|re.M)
        res_tr = r'<span class="hold-ymd">(.*.?)</span>'
        time = re.findall(res_tr, m_tr_time[idx], re.S|re.M)
        if tmp_info[0] == '该信息已被官方认证':
            continue
        for item in tmp_info:
            detail_one = collections.defaultdict(str)
            detail_one['Company'] = item.split('\n')[0]
            detail_one['School'] = item.split('\n')[1]
            detail_one['location'] = item.split('\n')[2]
            detail_one['time'] = time[0].split('</span>')[0]
            detail_main.append(detail_one)
    file_name = page_num + '.json'
    with open(file_name, 'w') as fh:
        json.dump(detail_main, fh, ensure_ascii=False)
    return break_flag


if __name__ == '__main__':
    print(type(getHtmlContent('https://xjh.haitou.cc/nj')))
    # print(getHtmlContent('https://xjh.haitou.cc/nj'))
    # https://xjh.haitou.cc/nj/page-2
    i = 0
    while 1:
        i += 1
        url_str = 'https://xjh.haitou.cc/nj/' + 'page-' + str(i)
        print(i)
        if getDetailInfo(getHtmlContent(url_str), 'page_' + str(i)):
            break

