# author_='Fang';
# date: 2021/5/26 14:57
"""
    插入排序
"""

li = [5, 3, 9, 23, 6, 3]


def insert_sort(li):
    for j in range(1, len(li)):
        key = li[j]
        i = j - 1
        while i >= 0 and li[i] > key:
            li[i + 1] = li[i]
            i -= 1
        li[i + 1] = key
    print(li)
    return li


def selection_sort(li):
    for i in range(0, len(li)):
        for j in range(i, len(li)):
            if li[i] > li[j]:
                li[i], li[j] = li[j], li[i]
    return li


print(selection_sort(li))
