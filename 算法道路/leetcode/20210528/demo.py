# author_='Fang';
# date: 2021/5/28 10:11

# 汉明距离
from typing import List

ans = 0
nums = [2, 4, 7]
for i in range(30):
    c = sum(((val >> i) & 1) for val in nums)
    ans += c * (len(nums) - c)


# 1537. 最大得分
def maxSum(nums1: List[int], nums2: List[int]) -> int:
    m, n = len(nums1), len(nums2)
    best1 = best2 = 0
    i = j = 0
    while i < m and j < n:
        if nums1[i] < nums2[j]:
            best1 += nums1[i]
            i += 1
        elif nums1[i] > nums2[j]:
            best2 += nums2[j]
            j += 1
        else:
            best1 = best2 = max(best2, best1) + nums1[i]
            i += 1
            j += 1
    best1, best2 = best1 + sum(nums1[i:]), best2 + sum(nums2[j:])
    return max(best2, best1) % (10 ** 9 + 7)


# print(maxSum([2, 4, 5, 8, 10], [4, 6, 8, 9]))

# 1002 查找常用字符串
def commonChars(words: List[str]) -> List[str]:
    res = []
    root = min(words, key=len)
    for char in root:
        poi = False
        for item in words:
            if char in item:
                poi = True
            else:
                poi = False
                break
        if poi:
            res.append(char)
            words = [c.replace(char, '', 1) for c in words]
    return res


# print(commonChars(["cool", "lock", "cook"]))

# 368. 最大整除子集  动态规划
def largestDivisibleSubset(nums: List[int]) -> List[int]:
    nums.sort()
    f = [[x] for x in nums]  # answer at nums[i]
    for j in range(len(nums)):
        for i in range(j):
            if nums[j] % nums[i] == 0 and len(f[i]) + 1 > len(f[j]):
                f[j] = f[i] + [nums[j]]
    return max(f, key=len)


print(largestDivisibleSubset([1, 2, 4, 8]))