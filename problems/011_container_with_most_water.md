
## Problem file template (`/problems/011_container_with_most_water.md`)

# 11. Container With Most Water

**Pattern:** [Two Pointers](../patterns/two_pointers.md)

**Difficulty:** Medium  
**Status:** ✅ Solved  
**Date:** 2025-11-09

**Approach Summary:**  
Move left/right pointers inward based on the smaller height.  
At each step calculate `min(height[i], height[j]) * (j - i)` and update max.

**Key Insight:**  
The area is limited by the shorter line, not the longer one.

**Code:**
```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        i, j = 0, len(height) - 1
        max_water = 0
        while i < j:
            max_water = max(max_water, min(height[i], height[j]) * (j - i))
            if height[i] < height[j]:
                i += 1
            else:
                j -= 1
        return max_water
