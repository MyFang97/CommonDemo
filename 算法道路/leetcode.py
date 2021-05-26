# author_='Fang';
# date: 2021/5/24 11:49
from typing import List


class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        """
        :param baseCosts: [1,7]
        :param toppingCosts: [3,4]
        :param target: 10
        :return:
        """
        ret = baseCosts[0]  # 初始ret为 base 0 满足条件
        for cost in toppingCosts:
            tmp = []
            for c in baseCosts:
                # 循环添加辅料和双倍辅料
                tmp.append(c + cost)
                tmp.append(c + 2 * cost)
            # 将本次遍历的总结过添加入baseCosts
            baseCosts.extend(tmp)
        for i in baseCosts:
            if i == target:
                return target
            # 这里卡了好久，没看到多个相同结果，取最少成本这条内容，刚睡醒脸都没洗简直了...
            if abs(i - target) < abs(ret - target) or abs(i - target) == abs(ret - target) and i < ret:
                ret = i
        return ret

    def singleNumber(self, nums: List[int]) -> int:

        for x in range(len(nums) - 1):
            if nums[x] not in nums[x + 1:] + nums[:x]:
                return nums[x]
        return nums[-1]

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        左下角开始找
        :param matrix:
        :param target:
        :return:
        """
        row = len(matrix) - 1  # 行
        col = 0  # 列
        print(row, col)
        while col <= len(matrix[0]) - 1 and row >= 0:
            if target == matrix[row][col]:
                return True
            elif target < matrix[row ][col]:
                row -= 1
            elif target > matrix[row][col]:
                col += 1
            else:
                print(target, matrix[row][col], matrix[row][col])
                return False
        print("最后")
        return False


# Solution().closestCost([1], [3, 4], 10)
# print(Solution().singleNumber([1, 0, 1]))
print(Solution().searchMatrix(matrix=
                              [[1, 4, 7, 11, 15],
                               [2, 5, 8, 12, 19],
                               [3, 6, 9, 16, 22],
                               [10, 13, 14, 17, 24],
                               [18, 21, 23, 26, 30]], target=1))
