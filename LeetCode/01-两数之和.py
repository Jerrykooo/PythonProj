class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
            lens = len(nums)
            j = -1

            for i in range(lens):
                if (target - nums[i]) in nums:
                    if (nums.count(target - nums[i]) == 1)&(target - nums[i] == nums[i]):   # 如果nums[i]仅出现一次，且nums[i]=nums[i]，说明找到的是nums[i]本身
                        continue
                    else:
                        j = nums.index(target - nums[i], i + 1) # 从i+1开始找
                        break
            if j > 0:
                return [i, j]
            else:
                return 'not found'