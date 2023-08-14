'''
给定一个由 n 个整数组成的数组编号，在数字中是否存在元素 a、b、c 使得 a + b + c = 0？在数组中找到所有唯一的三元组，给出零的总和。

'''


def threeSum(nums: list):
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue

        left, right = i + 1, len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1

                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


if __name__ == '__main__':
    nums = [-1, 0, 1, 2, -1, -4]
    res = threeSum(nums)
    print(res)
