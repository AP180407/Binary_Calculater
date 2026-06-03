# Viva Preparation Guide
## Arithmetic Micro-Operations in Computer Organization and Architecture

---

## Quick Reference Sheet

### Essential Definitions

| Term | Definition |
|------|------------|
| **Micro-operation** | An atomic, elementary operation performed in one clock cycle |
| **ALU** | Arithmetic Logic Unit - performs arithmetic and logic operations |
| **Register** | Fast storage location within the CPU |
| **Bus** | Communication pathway for data transfer |
| **2's Complement** | Standard method for representing signed integers |

---

## Top 15 Viva Questions and Answers

### Question 1: What are micro-operations?

**Answer**: Micro-operations are the most basic operations that a CPU can perform. They execute in a single clock cycle and control the flow of data between registers, through the ALU, and to/from memory. They are the building blocks of machine instructions.

**Example**: R1 ← R1 + R2 (Add contents of R2 to R1)

---

### Question 2: How does a computer perform subtraction using addition?

**Answer**: Computers use the **2's complement method** to perform subtraction:

1. Take the 2's complement of the subtrahend (number being subtracted)
   - Invert all bits (1's complement)
   - Add 1
2. Add this to the minuend
3. Discard any overflow carry

**Why**: This allows the same hardware (adder) to perform both addition and subtraction, reducing circuit complexity.

**Example**: 7 - 3 = 7 + (-3) = 7 + (2's complement of 3)
```
  0111 (7)
+ 1101 (2's complement of 3)
------
 10100 → 0100 (4) ✓
```

---

### Question 3: What is the difference between 1's complement and 2's complement?

**Answer**:

| Aspect | 1's Complement | 2's Complement |
|--------|---------------|----------------|
| Method | Invert all bits | Invert all bits, then add 1 |
| Zero representation | Two (±0) | One (0) |
| Range (n bits) | -(2^n-1 -1) to +(2^n-1 -1) | -2^n-1 to +(2^n-1 -1) |
| Arithmetic | Complex (end-around carry) | Simple (discard overflow) |
| Hardware | More complex | Simpler |

**Key Point**: 2's complement is used in modern computers because it simplifies arithmetic circuits.

---

### Question 4: Explain the Shift Left operation and its significance.

**Answer**: Logical Shift Left (LSL) moves all bits to the left by n positions, filling the vacated rightmost positions with zeros.

**Effect**: Each left shift multiplies the number by 2.

**Example**: 
```
0101 (5) << 1 = 1010 (10)    // 5 × 2 = 10
0101 (5) << 2 = 10100 (20)   // 5 × 4 = 20
```

**Significance**:
- Very fast multiplication by powers of 2
- Single clock cycle operation
- Used in floating-point arithmetic
- Part of Booth's multiplication algorithm

---

### Question 5: Explain the Shift Right operation and its significance.

**Answer**: Logical Shift Right (LSR) moves all bits to the right by n positions, filling the vacated leftmost positions with zeros.

**Effect**: Each right shift divides the number by 2 (for unsigned numbers).

**Example**:
```
1010 (10) >> 1 = 0101 (5)    // 10 ÷ 2 = 5
1010 (10) >> 2 = 0010 (2)    // 10 ÷ 4 = 2
```

**Note**: For signed numbers, arithmetic shift right preserves the sign bit.

---

### Question 6: How is binary multiplication implemented in hardware?

**Answer**: Binary multiplication uses the **Shift-and-Add** algorithm:

**Hardware Components**:
- Multiplicand register (M)
- Multiplier register (Q)
- Accumulator register (A)
- Control unit

**Algorithm**:
1. Initialize accumulator (A) to 0
2. For each bit of multiplier (LSB to MSB):
   - If bit = 1: A = A + M
   - Shift M left by 1
3. Result is in A

**Example**: 5 × 3
```
M = 0101 (5), Q = 0011 (3), A = 0000

Step 1: Q[0] = 1 → A = A + M = 0101, Shift M left → 1010
Step 2: Q[1] = 1 → A = A + M = 0101 + 1010 = 1111, Shift M left
Step 3-4: Q[2,3] = 0 → No addition

Result: A = 1111 (15) ✓
```

---

### Question 7: What is overflow in binary arithmetic? How is it detected?

**Answer**: Overflow occurs when the result of an arithmetic operation exceeds the range that can be represented with the given number of bits.

**Detection Rules**:
- **Addition**: Overflow occurs if both operands have the same sign but the result has a different sign
- **Formula**: Overflow = Carry_in(MSB) ⊕ Carry_out(MSB)**

**Example** (4-bit signed):
```
  0111 (7)
+ 0110 (6)
------
  1101 (-3) ← Wrong! Overflow occurred
```

**Hardware**: Most CPUs have an overflow flag in the status register.

---

### Question 8: What is the purpose of the Increment and Decrement operations?

**Answer**: These are fundamental micro-operations used extensively in CPU operations:

**Increment (R ← R + 1)**:
- Program Counter update after fetching instruction
- Loop counters
- Stack pointer management
- Memory address generation

**Decrement (R ← R - 1)**:
- Loop countdown
- Stack pointer adjustment
- Counter operations

**Hardware**: Implemented using half-adders (increment) or by adding 2's complement of 1 (decrement).

---

### Question 9: What is a full adder? How does it work?

**Answer**: A full adder is a combinational circuit that adds three bits (two operands and a carry-in) and produces a sum and carry-out.

**Inputs**: A, B, Carry_in
**Outputs**: Sum, Carry_out

**Truth Table**:
| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 |  0  |  0  |   0  |
| 0 | 0 |  1  |  1  |   0  |
| 0 | 1 |  0  |  1  |   0  |
| 0 | 1 |  1  |  0  |   1  |
| 1 | 0 |  0  |  1  |   0  |
| 1 | 0 |  1  |  0  |   1  |
| 1 | 1 |  0  |  0  |   1  |
| 1 | 1 |  1  |  1  |   1  |

**Formulas**:
- Sum = A ⊕ B ⊕ Cin
- Carry_out = AB + Cin(A ⊕ B)

**Implementation**: Multiple full adders are cascaded to create an n-bit adder.

---

### Question 10: Explain the Restoring Division Algorithm.

**Answer**: Restoring division is a method for dividing binary numbers.

**Algorithm**:
1. Initialize remainder (R) = 0
2. For each bit of dividend:
   - Shift R left, bring down next bit of dividend
   - R = R - Divisor
   - If R ≥ 0: Set quotient bit to 1
   - If R < 0: Restore R (add divisor back), set quotient bit to 0
3. Quotient is formed, remainder is in R

**Example**: 13 ÷ 3
```
Dividend: 1101 (13), Divisor: 0011 (3)

Step-by-step execution yields:
Quotient: 0100 (4)
Remainder: 0001 (1)

Verification: 13 = 4 × 3 + 1 ✓
```

---

### Question 11: Why do computers use binary instead of decimal?

**Answer**:
1. **Reliability**: Two states (0/1) are easier to distinguish reliably than 10 states
2. **Implementation**: Electronic switches (transistors) naturally have ON/OFF states
3. **Simplicity**: Boolean algebra is simpler with two values
4. **Error Detection**: Easier to detect errors with fewer states
5. **Cost**: Hardware implementation is simpler and cheaper

---

### Question 12: What is the range of numbers for an n-bit signed integer?

**Answer**:

| Representation | Range |
|---------------|-------|
| Unsigned | 0 to 2^n - 1 |
| Signed Magnitude | -(2^n-1 - 1) to +(2^n-1 - 1) |
| 1's Complement | -(2^n-1 - 1) to +(2^n-1 - 1) |
| 2's Complement | -2^n-1 to +(2^n-1 - 1) |

**Example** (8-bit):
- Unsigned: 0 to 255
- 2's Complement: -128 to +127

---

### Question 13: What is Booth's Algorithm?

**Answer**: Booth's Algorithm is an efficient method for multiplying signed binary numbers in 2's complement form.

**Advantages**:
- Handles both positive and negative numbers
- Reduces number of additions when there are consecutive 0s or 1s
- Used in modern processors

**Key Concept**: Instead of checking each bit individually, it checks bit pairs to determine whether to add, subtract, or shift.

---

### Question 14: What are the types of micro-operations?

**Answer**:

1. **Register Transfer**: R1 ← R2 (Move data)
2. **Arithmetic**: R1 ← R1 + R2, R1 ← R1 - 1, etc.
3. **Logic**: R1 ← R1 ∧ R2, R1 ← R1 ⊕ R2, etc.
4. **Shift**: R1 ← shl(R1), R1 ← shr(R1)

**Control Signals**: Each micro-operation is controlled by specific control signals generated by the control unit.

---

### Question 15: How does this web application demonstrate micro-operations?

**Answer**: This application:

1. **Visualizes**: Shows binary operations step-by-step
2. **Validates**: Ensures correct binary input format
3. **Explains**: Provides detailed explanations with decimal equivalents
4. **Demonstrates**: Shows practical implementation of algorithms
5. **Compares**: Displays relationships between operations (e.g., shift = multiply/divide)

**Technical Implementation**:
- Frontend: HTML/CSS/JavaScript for user interaction
- Backend: Python/Flask for algorithm execution
- API: RESTful endpoints for communication

---

## Presentation Tips

### Opening Statement
"Good morning. Today I will demonstrate arithmetic micro-operations, the fundamental operations that form the basis of all computation in a CPU. These operations include addition, subtraction using 2's complement, multiplication through shift-and-add, and several other operations that execute in a single clock cycle."

### Key Points to Emphasize

1. **Efficiency**: Micro-operations execute in one clock cycle
2. **Hardware Simplicity**: Subtraction using addition (2's complement)
3. **Relationship**: Shift operations are equivalent to multiplication/division
4. **Practical Application**: These operations power all software

### Demonstration Flow

1. Start with simple addition (4-bit numbers)
2. Show subtraction using 2's complement
3. Demonstrate shift operations and their multiplicative effect
4. Explain the algorithms while demonstrating
5. Show the code structure briefly

### Closing Statement
"In conclusion, arithmetic micro-operations are the foundation of CPU computation. Understanding these operations helps us appreciate how computers execute complex programs using simple, elegant algorithms implemented in hardware."

---

## Technical Terms Glossary

| Term | Definition |
|------|------------|
| LSB | Least Significant Bit (rightmost bit) |
| MSB | Most Significant Bit (leftmost bit) |
| XOR | Exclusive OR operation |
| Carry | Overflow bit from addition |
| Overflow | Result exceeds representable range |
| Ripple Carry | Carry propagates through all bits |
| Half Adder | Adds two bits, produces sum and carry |
| Full Adder | Adds three bits (including carry-in) |
| Status Register | Contains flags (zero, carry, overflow, sign) |

---

## Practice Problems

### Problem 1: Binary Addition
Perform: 10110 + 01101

<details>
<summary>Click for Solution</summary>

```
  10110 (22)
+ 01101 (13)
-------
 100011 (35)
```
</details>

### Problem 2: 2's Complement Subtraction
Perform: 25 - 13

<details>
<summary>Click for Solution</summary>

```
25 = 11001
13 = 01101

2's complement of 13:
1's complement: 10010
Add 1: 10011

Add: 11001 + 10011 = 101100
Discard overflow: 01100 = 12 ✓
```
</details>

### Problem 3: Shift Operations
What is 1101 << 2 and 1101 >> 1?

<details>
<summary>Click for Solution</summary>

```
1101 << 2 = 110100 (13 × 4 = 52)
1101 >> 1 = 0110 (13 ÷ 2 = 6)
```
</details>

---

Good luck with your viva presentation! 🎓