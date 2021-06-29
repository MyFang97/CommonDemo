# author_='Fang';
# date: 2021/6/3 10:56

"""
1880. 检查某单词是否等于两单词之和
"""

# class Solution:
#     def isSumEqual(self, firstWord: str, secondWord: str, targetWord: str) -> bool:
#         return self.f(firstWord) + self.f(secondWord) == self.f(targetWord)
#
#     def f(self, s):
#         res = 0
#         for c in range(len(s)):
#             res += (ord(s[c]) - ord("a")) * (10 ** (len(s) - c - 1))
#         return res


# print(Solution().isSumEqual(firstWord="acb", secondWord="cba", targetWord="cdb"))

"""
1881. 插入后的最大值
"""

# class Solution:
#     def maxValue(self, n: str, x: int) -> str:
#         l1 = list(n)
#         l1.append(str(x))
#         if int(n) > 0:
#             l1 = sorted(l1, reverse=True)
#             res = 0
#             for num in range(len(l1)):
#                 res += int(l1[num]) * (10 ** (len(l1) - 1 - num))
#             return str(res)
#         else:
#             l2 = sorted(l1[1:])
#             res = 0
#             for num in range(len(l2)):
#                 res += int(l2[num]) * (10 ** (len(l2) - 1 - num))
#             res = l1[0] + str(res)
#             return str(res)
# class Solution:
#     def maxValue(self, s: str, x: int) -> str:
#         N = len(s)
#         if s[0] == '-':
#             for i in range(1, N):
#                 if int(s[i]) > x:
#                     res = s[:i] + str(x) + s[i:]
#                     return res
#             return s + str(x)
#         else:
#             for i in range(N):
#                 if int(s[i]) < x:
#                     res = s[:i] + str(x) + s[i:]
#                     return res
#             return s + str(x)
#
#
# print(Solution().maxValue(s="-132", x=3))

"""
    1249.移除无效的括号
    "lee(t(c)o)de)"
    [  ]
"""

# class Solution:
#     def minRemoveToMakeValid(self, s: str) -> str:
#         stack = []
#         for i, j in enumerate(s):
#             if j == "(":
#                 stack.append((i, j))
#             elif j == ")":
#                 if stack and stack[-1][1] == "(":
#                     stack.pop()
#                 else:
#                     stack.append((i, j))
#         print(stack)
#         li_s = list(s)
#         for z in stack:
#             li_s[z[0]] = ""
#         res = ""
#         for item in li_s:
#             res += item
#         return res
#
#
# print(Solution().minRemoveToMakeValid("lee(t(c)o)de)"))

"""
165. 比较版本号
"""

# class Solution:
#     def compareVersion(self, version1: str, version2: str) -> int:
#         l1 = version1.split(".")
#         l2 = version2.split(".")
#         res = 0
#         for x in range(min(len(l2), len(l1))):
#             if int(l1[x]) > int(l2[x]):
#                 res = 1
#                 break
#             elif int(l1[x]) == int(l2[x]):
#                 res = 0
#             else:
#                 res = -1
#                 break
#         if res == 0:
#             if len(l1) > len(l2):
#                 for y in range(len(l2), len(l1)):
#                     if int(l1[y]) != 0:
#                         res = 1
#             elif len(l1) < len(l2):
#                 for z in range(len(l1), len(l2)):
#                     if int(l2[z]) != 0:
#                         res = -1
#         return res
#
#
# print(Solution().compareVersion(version1="1.01", version2="1.001"))

"""
    
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        if not headA or not headB:
            return None
        ap = headA
        bp = headB
        while ap != bp:
            ap = ap.next if ap else headB
            bp = bp.next if bp else headA
        return ap

    """
    4 1 8 4 5   // 5 0 1 8 4 5
    5 0 1 8 4 5 //   4 1 8 4 5
    遍历完自己的就去遍历另一个，会在交点相遇
    """



