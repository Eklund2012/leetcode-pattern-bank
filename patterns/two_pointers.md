# Two Pointers (Shrink from Both Ends)

**When to use:**  
- You have a sorted array or a range where you compare both ends.  
- You want to find pairs or maximize/minimize a value depending on distance.

**Idea:**  
Keep two indices (`i`, `j`) and move the one pointing to the smaller/lower value.  
This often reduces an O(n²) brute force to O(n).

<details>
<summary><b>Solution template (click to expand)</b></summary>

```python
i, j = 0, len(arr) - 1
best = 0
while i < j:
    val = min(arr[i], arr[j]) * (j - i)
    best = max(best, val)
    if arr[i] < arr[j]:
        i += 1
    else:
        j -= 1
return best
```
</details>
<br>

**Typical problems:**
- [011. Container With Most Water](../problems/011_container_with_most_water.md)

**Notes**

- Always move the pointer on the smaller side.
- Continue while left < right
- Use when both ends interact (sum, area, distance, etc.).
- Time O(n), Space O(1)