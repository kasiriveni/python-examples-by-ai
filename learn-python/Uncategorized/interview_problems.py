"""
Uncategorized: Python interview questions and solutions.
Covers common coding interview topics with clean implementations.
"""
from collections import defaultdict, deque, Counter
from typing import Optional

# ═══════════════════════════════════════════
# String problems
# ═══════════════════════════════════════════

def is_palindrome(s: str) -> bool:
    """Check if string is palindrome (ignore case and spaces)."""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

def longest_palindromic_substring(s: str) -> str:
    """Expand-around-center O(n²) approach."""
    if not s:
        return ""
    start, end = 0, 0

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return l + 1, r - 1

    for i in range(len(s)):
        l1, r1 = expand(i, i)      # odd length
        l2, r2 = expand(i, i + 1)  # even length
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end + 1]

def count_anagram_pairs(words: list[str]) -> int:
    """Count pairs that are anagrams of each other."""
    freq = defaultdict(int)
    for w in words:
        freq[tuple(sorted(w))] += 1
    return sum(n * (n - 1) // 2 for n in freq.values())

def longest_without_repeat(s: str) -> int:
    """Length of longest substring without repeating chars (sliding window)."""
    seen = {}
    max_len = 0
    left = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# ═══════════════════════════════════════════
# Array / List problems
# ═══════════════════════════════════════════

def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Find two indices that sum to target. O(n)."""
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None

def max_subarray(nums: list[int]) -> int:
    """Kadane's algorithm — max sum contiguous subarray."""
    max_sum = curr = nums[0]
    for n in nums[1:]:
        curr = max(n, curr + n)
        max_sum = max(max_sum, curr)
    return max_sum

def product_except_self(nums: list[int]) -> list[int]:
    """Product of all elements except self without division. O(n)."""
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result

def rotate_matrix_90(matrix: list[list[int]]) -> list[list[int]]:
    """Rotate NxN matrix 90° clockwise in-place."""
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()
    return matrix

def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals."""
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# ═══════════════════════════════════════════
# Linked List
# ═══════════════════════════════════════════

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linked(nums: list[int]) -> Optional[ListNode]:
    if not nums: return None
    head = ListNode(nums[0])
    curr = head
    for n in nums[1:]:
        curr.next = ListNode(n)
        curr = curr.next
    return head

def linked_to_list(head: Optional[ListNode]) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

def detect_cycle(head: Optional[ListNode]) -> bool:
    """Floyd's tortoise and hare."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# ═══════════════════════════════════════════
# Trees
# ═══════════════════════════════════════════

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def is_balanced(root: Optional[TreeNode]) -> bool:
    def height(node):
        if not node: return 0
        lh = height(node.left)
        if lh == -1: return -1
        rh = height(node.right)
        if rh == -1: return -1
        if abs(lh - rh) > 1: return -1
        return 1 + max(lh, rh)
    return height(root) != -1

def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left  = lowest_common_ancestor(root.left,  p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right: return root
    return left or right

# ═══════════════════════════════════════════
# Dynamic Programming
# ═══════════════════════════════════════════

def coin_change(coins: list[int], amount: int) -> int:
    """Minimum coins to make amount. Returns -1 if impossible."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

def longest_common_subsequence(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

if __name__ == "__main__":
    print("=== String Problems ===")
    print(f"is_palindrome('racecar'): {is_palindrome('racecar')}")
    print(f"is_palindrome('A man a plan a canal Panama'): {is_palindrome('A man a plan a canal Panama')}")
    print(f"longest_palindromic_substring('babad'): {longest_palindromic_substring('babad')}")
    print(f"longest_without_repeat('abcabcbb'): {longest_without_repeat('abcabcbb')}")

    print("\n=== Array Problems ===")
    print(f"two_sum([2,7,11,15], 9): {two_sum([2,7,11,15], 9)}")
    print(f"max_subarray([-2,1,-3,4,-1,2,1,-5,4]): {max_subarray([-2,1,-3,4,-1,2,1,-5,4])}")
    print(f"product_except_self([1,2,3,4]): {product_except_self([1,2,3,4])}")
    print(f"merge_intervals([[1,3],[2,6],[8,10],[15,18]]): {merge_intervals([[1,3],[2,6],[8,10],[15,18]])}")

    m = [[1,2,3],[4,5,6],[7,8,9]]
    print(f"rotate_matrix_90:\n  input: {m}")
    print(f"  output: {rotate_matrix_90(m)}")

    print("\n=== Linked List ===")
    head = list_to_linked([1, 2, 3, 4, 5])
    rev = reverse_linked_list(head)
    print(f"Reversed: {linked_to_list(rev)}")

    print("\n=== Tree Problems ===")
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(f"max_depth: {max_depth(root)}")
    print(f"is_balanced: {is_balanced(root)}")

    print("\n=== Dynamic Programming ===")
    print(f"coin_change([1,5,6,9], 11): {coin_change([1,5,6,9], 11)}")
    print(f"LCS('abcde', 'ace'): {longest_common_subsequence('abcde', 'ace')}")
