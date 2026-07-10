[[Solving Notes]][[Pumbaa]]

### Concept of Mapping

1. **Initial Setup**:
    
    - **Row Mapping**: `row_mapping[i] = i` initially, meaning row `i` is at position `i`.
    - **Column Mapping**: `column_mapping[j] = j` initially, meaning column `j` is at position `j`.
2. **Swapping Rows**:
    
    - When you swap row `xi` with row `yi`, instead of physically moving the data, you just update the indices in `row_mapping`.
    - For example, if `row_mapping[xi]` was `5` and `row_mapping[yi]` was `10`, after the swap, `row_mapping[xi]` would be `10` and `row_mapping[yi]` would be `5`.
3. **Swapping Columns**:
    
    - Similarly, when you swap column `xi` with column `yi`, you update `column_mapping`.
    - For example, if `column_mapping[xi]` was `2` and `column_mapping[yi]` was `7`, after the swap, `column_mapping[xi]` would be `7` and `column_mapping[yi]` would be `2`.
4. **Getting a Value**:
    
    - When you need to get the value from a specific position `(xi, yi)`, you use the current mappings to find the actual position in the original matrix.
    - If `row_mapping[xi]` is `a` and `column_mapping[yi]` is `b`, the value at `(xi, yi)` in the current configuration is `matrix[a][b]`.

### Example

Imagine a 3x3 matrix:

Copy code

`1 2 3 
  4 5 6
  7 8 9`

Initial mappings are:

- `row_mapping = [0, 1, 2]` (0-based indexing)
- `column_mapping = [0, 1, 2]`

If we swap row 1 with row 2:

- `row_mapping` becomes `[1, 0, 2]`

If we swap column 1 with column 3:

- `column_mapping` becomes `[2, 1, 0]`

To get the value at (1, 3):

- According to `row_mapping`, row 1 maps to the original row 2.
- According to `column_mapping`, column 3 maps to the original column 0.
- So the value at (1, 3) is `matrix[1][2]`, which is `6`.