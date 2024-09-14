class Solution:
    def isPalindrome_with_str_conversion(self, x: int) -> bool:
        return str(x) == str(x)[::-1]
