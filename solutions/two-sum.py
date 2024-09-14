class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        indices = {}
        for i, num in enumerate(nums):
            indices[num] = i
        for i, num in enumerate(nums):
            if target - num in indices and indices[target - num] != i:
                return [i, indices[target - num]]
