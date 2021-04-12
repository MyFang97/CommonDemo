"""
    字符串转换
"""
import unicodedata
import chardet

# -*- coding=gb2312 -*-
a = u"中文"
print(a)
print(chardet.detect(str.encode(a)))

a_gb2312 = a.encode('gb2312')
print(a_gb2312)


a_unicode = a_gb2312.decode('gb2312')
print(a_unicode)
print(chardet.detect(str.encode(a_unicode)))

assert (a_unicode == a)
a_utf_8 = a_unicode.encode('utf-8')
print(a_utf_8)
