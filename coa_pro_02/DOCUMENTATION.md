<h1>Arithmetic Micro-Operations Calculator</h1><h2>Web Application for Computer Organization and Architecture</h2><hr><h2>Table of Contents</h2><ol> <li><a href="#project-overview">Project Overview</a></li> <li><a href="#project-structure">Project Structure</a></li> <li><a href="#installation-and-running">Installation and Running</a></li> <li><a href="#arithmetic-micro-operations-explained">Arithmetic Micro-Operations Explained</a></li> <li><a href="#algorithms-and-implementation">Algorithms and Implementation</a></li> <li><a href="#api-reference">API Reference</a></li> <li><a href="#viva-preparation-guide">Viva Preparation Guide</a></li> </ol><hr><h2>Project Overview</h2><p>This web application demonstrates fundamental <strong>arithmetic micro-operations</strong> used in computer organization and architecture. It provides an interactive interface to perform various binary operations, making it an excellent tool for understanding how computers execute arithmetic at the hardware level.</p><h3>Features</h3><ul> <li><strong>Basic Arithmetic Operations</strong>: Addition, Subtraction, Multiplication, Division</li> <li><strong>Shift Operations</strong>: Logical Shift Left, Logical Shift Right</li> <li><strong>Complement Operations</strong>: 1's Complement, 2's Complement</li> <li><strong>Counter Operations</strong>: Increment, Decrement</li> <li><strong>Real-time Decimal Conversion</strong>: Instant binary-to-decimal display</li> <li><strong>Detailed Explanations</strong>: Step-by-step operation breakdowns</li> <li><strong>Input Validation</strong>: Ensures only valid binary input</li> </ul><hr><h2>Project Structure</h2><pre><code>arithmetic-micro-operations/
│
├── app.py                    # Flask backend with all algorithms
├── DOCUMENTATION.md          # This documentation file
├── VIVA_PREPARATION.md       # Viva preparation notes
│
├── templates/
│   └── index.html            # Main HTML interface
│
└── static/
    └── styles.css            # Professional CSS styling
</code></pre><h3>File Descriptions</h3><table class="e-rte-table"> <thead> <tr> <th>File</th> <th>Purpose</th> </tr> </thead> <tbody><tr> <td><code>app.py</code></td> <td>Flask backend containing all micro-operation algorithms, API endpoints, and server logic</td> </tr> <tr> <td><code>templates/index.html</code></td> <td>Main web interface with input fields, operation buttons, and JavaScript for interactivity</td> </tr> <tr> <td><code>static/styles.css</code></td> <td>Professional styling suitable for academic presentations</td> </tr> </tbody></table><hr><h2>Installation and Running</h2><h3>Prerequisites</h3><ul> <li>Python 3.7 or higher</li> <li>pip (Python package manager)</li> </ul><h3>Step-by-Step Installation</h3><ol> <li><p><strong>Navigate to the project directory:</strong></p> <pre><code class="language-bash">cd /workspace
</code></pre> </li> <li><p><strong>Install Flask (if not already installed):</strong></p> <pre><code class="language-bash">pip install flask
</code></pre> </li> <li><p><strong>Run the application:</strong></p> <pre><code class="language-bash">python app.py
</code></pre> </li> <li><strong>Access the application:</strong> <ul> <li>Open your web browser</li> <li>Go to: <code>http://localhost:5000</code></li> <li>The calculator interface will be displayed</li> </ul> </li> </ol><h3>Troubleshooting</h3><p>If you encounter any issues:</p><ol> <li><strong>Port already in use:</strong> <ul> <li>Change the port in <code>app.py</code>: <code>app.run(port=5001)</code></li> </ul> </li> <li><strong>Flask not found:</strong> <ul> <li>Install Flask: <code>pip install flask</code></li> </ul> </li> <li><strong>Template not found:</strong> <ul> <li>Ensure the <code>templates</code> folder exists with <code>index.html</code></li> </ul> </li> </ol><hr><h2>Arithmetic Micro-Operations Explained</h2><h3>What are Micro-Operations?</h3><p>Micro-operations are the <strong>atomic, lowest-level operations</strong> performed by a computer's CPU. They are the fundamental building blocks of instruction execution, controlling data flow between registers, ALU (Arithmetic Logic Unit), and memory.</p><h3>Types of Micro-Operations</h3><ol> <li><strong>Register Transfer</strong>: Move data between registers</li> <li><strong>Arithmetic</strong>: Perform mathematical operations</li> <li><strong>Logic</strong>: Perform bitwise operations (AND, OR, NOT, XOR)</li> <li><strong>Shift</strong>: Move bits left or right</li> </ol><p>This application focuses on <strong>Arithmetic Micro-Operations</strong>.</p><hr><h3>1. Binary Addition</h3><p><strong>Definition</strong>: Adding two binary numbers bit by bit from LSB (Least Significant Bit) to MSB (Most Significant Bit).</p><p><strong>Truth Table for Full Adder</strong>:</p><table class="e-rte-table"> <thead> <tr> <th>A</th> <th>B</th> <th>Carry In</th> <th>Sum</th> <th>Carry Out</th> </tr> </thead> <tbody><tr> <td>0</td> <td>0</td> <td>0</td> <td>0</td> <td>0</td> </tr> <tr> <td>0</td> <td>0</td> <td>1</td> <td>1</td> <td>0</td> </tr> <tr> <td>0</td> <td>1</td> <td>0</td> <td>1</td> <td>0</td> </tr> <tr> <td>0</td> <td>1</td> <td>1</td> <td>0</td> <td>1</td> </tr> <tr> <td>1</td> <td>0</td> <td>0</td> <td>1</td> <td>0</td> </tr> <tr> <td>1</td> <td>0</td> <td>1</td> <td>0</td> <td>1</td> </tr> <tr> <td>1</td> <td>1</td> <td>0</td> <td>0</td> <td>1</td> </tr> <tr> <td>1</td> <td>1</td> <td>1</td> <td>1</td> <td>1</td> </tr> </tbody></table><p><strong>Formula</strong>:</p><ul> <li>Sum = A ⊕ B ⊕ Carry_in</li> <li>Carry_out = (A · B) + (Carry_in · (A ⊕ B))</li> </ul><p><strong>Example</strong>:</p><pre><code>  1011 (11)
+ 0110 (6)
------
 10001 (17)
</code></pre><hr><h3>2. Binary Subtraction</h3><p><strong>Definition</strong>: Subtracting one binary number from another using the <strong>2's Complement Method</strong>.</p><p><strong>Why 2's Complement?</strong></p><ul> <li>Computers cannot directly subtract; they perform subtraction by adding the negative</li> <li>A - B = A + (-B)</li> <li>-B is represented as 2's complement of B</li> </ul><p><strong>Steps for Subtraction</strong>:</p><ol> <li>Find 2's complement of subtrahend (B)<ul> <li>Invert all bits (1's complement)</li> <li>Add 1</li> </ul> </li> <li>Add minuend (A) to the 2's complement of B</li> <li>Discard any overflow carry</li> </ol><p><strong>Example</strong>: 7 - 3</p><pre><code>7 in binary:  0111
3 in binary:  0011

Step 1: 1's complement of 3 = 1100
Step 2: Add 1 → 1101 (2's complement)

Step 3: Add 7 + (-3)
  0111
+ 1101
------
 10100

Discard overflow carry → 0100 = 4 ✓
</code></pre><hr><h3>3. Binary Multiplication</h3><p><strong>Definition</strong>: Multiplying two binary numbers using the <strong>Shift and Add</strong> algorithm.</p><p><strong>Algorithm</strong>:</p><ol> <li>Initialize product to 0</li> <li>For each bit of multiplier (right to left):<ul> <li>If bit is 1, add multiplicand to product (shifted appropriately)</li> <li>Shift multiplicand left by one position for next iteration</li> </ul> </li> </ol><p><strong>Example</strong>: 5 × 3</p><pre><code>Multiplicand: 0101 (5)
Multiplier:   0011 (3)

Bit 0 (LSB) = 1: Add 0101 shifted 0 times → Product = 0101
Bit 1 = 1:       Add 0101 shifted 1 time  → Product = 0101 + 1010 = 1111
Bit 2 = 0:       Skip
Bit 3 = 0:       Skip

Final Product: 1111 (15) ✓
</code></pre><p><strong>Time Complexity</strong>: O(n²) where n is the number of bits</p><hr><h3>4. Binary Division</h3><p><strong>Definition</strong>: Dividing one binary number by another using the <strong>Restoring Division Algorithm</strong>.</p><p><strong>Algorithm</strong>:</p><ol> <li>Initialize quotient to 0</li> <li>For each bit of dividend:<ul> <li>Shift remainder left, bring down next bit</li> <li>Subtract divisor from remainder</li> <li>If result ≥ 0: set quotient bit to 1</li> <li>If result &lt; 0: restore remainder, set quotient bit to 0</li> </ul> </li> <li>Return quotient and remainder</li> </ol><p><strong>Example</strong>: 13 ÷ 3</p><pre><code>Dividend: 1101 (13)
Divisor:  0011 (3)

Quotient: 0100 (4)
Remainder: 0001 (1)

Verification: 13 = 4 × 3 + 1 ✓
</code></pre><hr><h3>5. Logical Shift Left (LSL)</h3><p><strong>Definition</strong>: Shift all bits to the left by n positions, filling vacated positions with 0s.</p><p><strong>Effect</strong>: Multiplies the number by 2^n</p><p><strong>Example</strong>:</p><pre><code>Original:    0101 (5)
Shift left 1: 1010 (10) = 5 × 2
Shift left 2: 10100 (20) = 5 × 4
</code></pre><p><strong>Hardware Implementation</strong>: Direct connection shift register, very fast (single clock cycle)</p><hr><h3>6. Logical Shift Right (LSR)</h3><p><strong>Definition</strong>: Shift all bits to the right by n positions, filling vacated positions with 0s.</p><p><strong>Effect</strong>: Divides the number by 2^n (for unsigned numbers)</p><p><strong>Example</strong>:</p><pre><code>Original:     1010 (10)
Shift right 1: 0101 (5) = 10 ÷ 2
Shift right 2: 0010 (2) = 10 ÷ 4
</code></pre><hr><h3>7. 1's Complement</h3><p><strong>Definition</strong>: Invert all bits (0→1, 1→0)</p><p><strong>Use Cases</strong>:</p><ul> <li>Representing negative numbers (older method)</li> <li>Bitwise NOT operation</li> <li>Network checksums</li> <li>Step in calculating 2's complement</li> </ul><p><strong>Example</strong>:</p><pre><code>Original:     0101 (5)
1's Complement: 1010 (-5 in 1's complement)
</code></pre><p><strong>Limitation</strong>: Has two representations of zero (+0 and -0)</p><hr><h3>8. 2's Complement</h3><p><strong>Definition</strong>: Add 1 to 1's complement</p><p><strong>Why It's Preferred</strong>:</p><ul> <li>Only one representation of zero</li> <li>Arithmetic operations work naturally</li> <li>Most significant bit indicates sign (0=positive, 1=negative)</li> </ul><p><strong>Example</strong>:</p><pre><code>Original:     0101 (5)
1's Complement: 1010
Add 1:          1011 (-5 in 2's complement)

Range for 4 bits: -8 to +7
</code></pre><hr><h3>9. Increment</h3><p><strong>Definition</strong>: Add 1 to the binary number</p><p><strong>Micro-operation Notation</strong>: R ← R + 1</p><p><strong>Use Cases</strong>:</p><ul> <li>Program Counter (PC) update</li> <li>Loop counters</li> <li>Stack pointer management</li> <li>Memory address calculation</li> </ul><p><strong>Example</strong>:</p><pre><code>Original:  0101 (5)
Increment: 0110 (6)
</code></pre><hr><h3>10. Decrement</h3><p><strong>Definition</strong>: Subtract 1 from the binary number</p><p><strong>Micro-operation Notation</strong>: R ← R - 1</p><p><strong>Use Cases</strong>:</p><ul> <li>Loop countdown</li> <li>Stack pointer decrement</li> <li>Counter operations</li> </ul><p><strong>Example</strong>:</p><pre><code>Original:  0101 (5)
Decrement: 0100 (4)
</code></pre><hr><h2>Algorithms and Implementation</h2><h3>Backend Architecture (app.py)</h3><p>The Flask backend implements each micro-operation as a separate function:</p><pre><code class="language-python"># Example: Binary Addition using Full Adder Logic
def binary_addition(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    result = []
    carry = 0
    
    for i in range(max_len - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])
        
        sum_bit = bit_a ^ bit_b ^ carry
        carry = (bit_a &amp; bit_b) | (carry &amp; (bit_a ^ bit_b))
        
        result.insert(0, str(sum_bit))
    
    if carry:
        result.insert(0, '1')
    
    return ''.join(result), carry
</code></pre><h3>Frontend Architecture (index.html)</h3><p>The frontend uses:</p><ul> <li><strong>HTML</strong>: Structure and content</li> <li><strong>CSS</strong>: Styling and visual design</li> <li><strong>JavaScript</strong>: Interactivity and API communication</li> </ul><h3>Data Flow</h3><pre><code>User Input → JavaScript Validation → API Request → 
Flask Backend → Algorithm Execution → JSON Response → 
UI Update with Result and Explanation
</code></pre><hr><h2>API Reference</h2><h3>POST /calculate</h3><p>Performs the specified arithmetic micro-operation.</p><p><strong>Request Body</strong>:</p><pre><code class="language-json">{
    "operation": "addition",
    "operand1": "1010",
    "operand2": "0011",
    "positions": 1
}
</code></pre><p><strong>Response (Success)</strong>:</p><pre><code class="language-json">{
    "success": true,
    "result": "1101",
    "explanation": "Binary Addition: 1010 + 0011 = 1101\nDecimal: 10 + 3 = 13"
}
</code></pre><p><strong>Response (Error)</strong>:</p><pre><code class="language-json">{
    "success": false,
    "error": "Invalid binary input. Please enter only 0s and 1s."
}
</code></pre><h3>Supported Operations</h3><table class="e-rte-table"> <thead> <tr> <th>Operation</th> <th>Required Parameters</th> </tr> </thead> <tbody><tr> <td>addition</td> <td>operand1, operand2</td> </tr> <tr> <td>subtraction</td> <td>operand1, operand2</td> </tr> <tr> <td>multiplication</td> <td>operand1, operand2</td> </tr> <tr> <td>division</td> <td>operand1, operand2</td> </tr> <tr> <td>shift_left</td> <td>operand1, positions</td> </tr> <tr> <td>shift_right</td> <td>operand1, positions</td> </tr> <tr> <td>ones_complement</td> <td>operand1</td> </tr> <tr> <td>twos_complement</td> <td>operand1</td> </tr> <tr> <td>increment</td> <td>operand1</td> </tr> <tr> <td>decrement</td> <td>operand1</td> </tr> </tbody></table><hr><h2>Viva Preparation Guide</h2><h3>Key Concepts to Explain</h3><ol> <li><strong>What are micro-operations?</strong> <ul> <li>Atomic operations performed by CPU</li> <li>Execute in one clock cycle</li> <li>Building blocks of instructions</li> </ul> </li> <li><strong>Why binary arithmetic?</strong> <ul> <li>Computers use binary (0s and 1s)</li> <li>Easy to implement in hardware</li> <li>Reliable signal representation</li> </ul> </li> <li><strong>2's Complement Importance</strong> <ul> <li>Unified arithmetic circuit</li> <li>No separate subtraction hardware needed</li> <li>A - B = A + (2's complement of B)</li> </ul> </li> <li><strong>Shift Operations</strong> <ul> <li>Multiplication/division by powers of 2</li> <li>Very fast (single clock cycle)</li> <li>Used in floating-point arithmetic</li> </ul> </li> </ol><h3>Common Viva Questions</h3><ol> <li><strong>Q: How does a computer perform subtraction?</strong> <ul> <li>A: Using 2's complement method. The computer adds the minuend to the 2's complement of the subtrahend.</li> </ul> </li> <li><strong>Q: What is the difference between logical and arithmetic shift?</strong> <ul> <li>A: Logical shift fills with 0s. Arithmetic shift preserves the sign bit (MSB).</li> </ul> </li> <li><strong>Q: Why is 2's complement preferred over 1's complement?</strong> <ul> <li>A: 2's complement has only one representation of zero, and arithmetic circuits are simpler.</li> </ul> </li> <li><strong>Q: What is overflow in binary addition?</strong> <ul> <li>A: When the result exceeds the maximum representable value for the given bit width.</li> </ul> </li> <li><strong>Q: How is binary multiplication implemented in hardware?</strong> <ul> <li>A: Using shift registers and adders. The multiplicand is added to an accumulator when the multiplier bit is 1, then shifted.</li> </ul> </li> </ol><h3>Demonstration Tips</h3><ol> <li>Start with simple examples (4-bit numbers)</li> <li>Show the decimal equivalent for understanding</li> <li>Explain the algorithm step-by-step</li> <li>Point out the relationship between operations (e.g., shift = multiply/divide)</li> <li>Discuss hardware implementation briefly</li> </ol><hr><h2>Conclusion</h2><p>This web application provides a comprehensive, interactive demonstration of arithmetic micro-operations. Use it to:</p><ul> <li>Understand binary arithmetic fundamentals</li> <li>Visualize operation execution</li> <li>Prepare for academic presentations</li> <li>Practice problem-solving</li> </ul><p>Good luck with your viva presentation!</p>