# NumPy Notes (Quick Syntax Reference)

> Beginner-friendly notes — focus on syntax you'll actually use.

---

## 1. Import

```python
import numpy as np
```

---

## 2. Creating Arrays

| Task | Syntax | Example |
|---|---|---|
| From a list | `np.array(list)` | `np.array([1,2,3])` |
| 2D array | `np.array([[..],[..]])` | `np.array([[1,2],[3,4]])` |
| Zeros | `np.zeros(shape)` | `np.zeros((2,3))` |
| Ones | `np.ones(shape)` | `np.ones((3,3))` |
| Empty (garbage values) | `np.empty(shape)` | `np.empty((2,2))` |
| Identity matrix | `np.eye(n)` | `np.eye(3)` |
| Range of values | `np.arange(start, stop, step)` | `np.arange(0,10,2)` |
| Evenly spaced values | `np.linspace(start, stop, num)` | `np.linspace(0,1,5)` |
| Random floats (0–1) | `np.random.rand(shape)` | `np.random.rand(2,2)` |
| Random ints | `np.random.randint(low, high, size)` | `np.random.randint(0,10,size=5)` |

---

## 3. Array Properties

```python
arr.shape     # dimensions, e.g. (2,3)
arr.ndim      # number of dimensions
arr.size      # total number of elements
arr.dtype     # data type of elements
arr.itemsize  # bytes per element
```

---

## 4. Reshaping & Resizing

```python
arr.reshape(2,3)     # change shape (same total elements)
arr.flatten()        # convert to 1D (returns copy)
arr.ravel()          # convert to 1D (returns view)
arr.T                # transpose
np.resize(arr,(3,3)) # change size (can pad/repeat)
```

---

## 5. Indexing & Slicing

```python
arr[0]          # first element
arr[-1]         # last element
arr[1:4]        # slice (index 1 to 3)
arr[:, 1]       # all rows, column 1 (2D)
arr[1, :]       # row 1, all columns (2D)
arr[arr > 5]    # boolean/conditional indexing
```

---

## 6. Math Operations

```python
arr + 2        # add scalar to all elements
arr * 2        # multiply
arr1 + arr2    # element-wise addition
arr1 * arr2    # element-wise multiplication
np.dot(arr1, arr2)   # matrix multiplication
arr1 @ arr2          # also matrix multiplication
```

### Common Functions

| Function | Meaning |
|---|---|
| `np.sum(arr)` | Sum of all elements |
| `np.mean(arr)` | Average |
| `np.median(arr)` | Median |
| `np.std(arr)` | Standard deviation |
| `np.var(arr)` | Variance |
| `np.min(arr)` / `np.max(arr)` | Min / Max value |
| `np.argmin(arr)` / `np.argmax(arr)` | Index of min / max |
| `np.sqrt(arr)` | Square root |
| `np.abs(arr)` | Absolute value |
| `np.round(arr, n)` | Round to n decimals |

> Add `axis=0` (column-wise) or `axis=1` (row-wise) to most of these for 2D arrays.
> Example: `np.sum(arr, axis=0)`

---

## 7. Sorting & Searching

```python
np.sort(arr)          # sorted copy
np.argsort(arr)       # indices that would sort array
np.where(arr > 5)     # indices where condition is True
np.unique(arr)        # unique values
```

---

## 8. Joining & Splitting

```python
np.concatenate([arr1, arr2])   # join arrays
np.vstack([arr1, arr2])        # stack vertically
np.hstack([arr1, arr2])        # stack horizontally
np.split(arr, 3)               # split into 3 equal parts
```

---

## 9. Copy vs View (Important!)

```python
b = arr.view()   # shares memory with arr (changes affect both)
b = arr.copy()   # independent copy (changes don't affect arr)
```

---

## 10. Useful Checks

```python
np.isnan(arr)      # check for NaN values
np.any(arr > 5)     # True if any element satisfies condition
np.all(arr > 5)     # True if all elements satisfy condition
```

---

## Quick Cheat Sheet Summary

```
Create   -> np.array(), np.zeros(), np.ones(), np.arange(), np.linspace()
Inspect  -> .shape, .ndim, .size, .dtype
Reshape  -> .reshape(), .flatten(), .T
Slice    -> arr[start:stop], arr[condition]
Math     -> +, -, *, /, np.dot(), np.sum(), np.mean()
Sort     -> np.sort(), np.argsort()
```
