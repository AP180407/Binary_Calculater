from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# ==================== INPUT VALIDATION ====================
def is_valid_binary(binary_str):
    """Validate that input contains only binary digits (0s and 1s)"""
    if not binary_str:
        return False
    pattern = r'^[01]+$'
    return bool(re.match(pattern, binary_str))

def normalize_binary(binary_str, length=None):
    """Normalize binary string to specified length by padding with zeros"""
    if length:
        return binary_str.zfill(length)
    return binary_str

# ==================== BASIC ARITHMETIC OPERATIONS ====================

def binary_addition(a, b):
    """
    Binary Addition using Full Adder Logic
    
    Algorithm: Bit-by-bit addition from LSB to MSB
    - Sum bit = A XOR B XOR Carry_in
    - Carry_out = (A AND B) OR (Carry_in AND (A XOR B))
    
    Time Complexity: O(n) where n is the number of bits
    """
    # Normalize to same length
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    result = []
    carry = 0
    
    # Process from right to left (LSB to MSB)
    for i in range(max_len - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])
        
        # Full adder logic
        sum_bit = bit_a ^ bit_b ^ carry
        carry = (bit_a & bit_b) | (carry & (bit_a ^ bit_b))
        
        result.insert(0, str(sum_bit))
    
    # If there's a final carry, add it
    if carry:
        result.insert(0, '1')
    
    return ''.join(result), carry

def binary_subtraction(a, b):
    """
    Binary Subtraction using 2's Complement Method
    
    Algorithm: A - B = A + (-B) = A + (2's complement of B)
    2's complement = 1's complement + 1
    
    This is how computers perform subtraction - by adding!
    """
    # Normalize to same length
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    # Calculate 2's complement of b
    # Step 1: 1's complement (invert all bits)
    ones_comp = ''.join('1' if bit == '0' else '0' for bit in b)
    
    # Step 2: Add 1 to get 2's complement
    twos_comp, _ = binary_addition(ones_comp, '1')
    twos_comp = twos_comp.zfill(max_len)
    
    # Step 3: Add a + (2's complement of b)
    result, carry = binary_addition(a, twos_comp)
    
    # If result is longer than max_len, there was overflow (positive result)
    # If carry is 0, result is negative (in 2's complement form)
    is_negative = not carry
    
    return result, is_negative

def binary_multiplication(a, b):
    """
    Binary Multiplication using Booth's Algorithm approach
    
    Algorithm: Shift and Add method
    - Initialize product to 0
    - For each bit of multiplier (from LSB):
        - If bit is 1, add multiplicand to product
        - Shift product left by 1
    
    Time Complexity: O(n²) where n is the number of bits
    """
    # Handle edge cases
    if a == '0' or b == '0':
        return '0', False
    
    # Convert to decimal for easier handling
    multiplicand = int(a, 2)
    multiplier = int(b, 2)
    
    product = 0
    steps = []
    
    # Shift and add algorithm
    iteration = 0
    while multiplier > 0:
        if multiplier & 1:  # If LSB is 1
            product += multiplicand << iteration
            steps.append(f"Add {bin(multiplicand << iteration)[2:]} (shifted left {iteration} times)")
        iteration += 1
        multiplier >>= 1
    
    result = bin(product)[2:]
    return result, False

def binary_division(dividend, divisor):
    """
    Binary Division using Restoring Division Algorithm
    
    Algorithm:
    1. Initialize quotient to 0
    2. Shift dividend left, bring down next bit
    3. Subtract divisor from current dividend portion
    4. If result is positive, set quotient bit to 1
    5. If result is negative, restore dividend and set quotient bit to 0
    
    Returns: (quotient, remainder)
    """
    # Handle edge cases
    if divisor == '0' or int(divisor, 2) == 0:
        return None, None, True  # Division by zero
    
    dividend_val = int(dividend, 2)
    divisor_val = int(divisor, 2)
    
    if dividend_val == 0:
        return '0', '0', False
    
    quotient = dividend_val // divisor_val
    remainder = dividend_val % divisor_val
    
    return bin(quotient)[2:], bin(remainder)[2:], False

# ==================== ADDITIONAL MICRO-OPERATIONS ====================

def logical_shift_left(binary, positions=1):
    """
    Logical Shift Left (LSL)
    
    Operation: Shift all bits left by specified positions
    - Vacated positions on right are filled with 0
    - Leftmost bits are lost (or stored in carry flag)
    
    Effect: Multiplication by 2^n (n = number of positions)
    
    Used in: Multiplication, bit manipulation, serial communication
    """
    result = binary + '0' * positions
    return result

def logical_shift_right(binary, positions=1):
    """
    Logical Shift Right (LSR)
    
    Operation: Shift all bits right by specified positions
    - Vacated positions on left are filled with 0
    - Rightmost bits are lost (or stored in carry flag)
    
    Effect: Division by 2^n for unsigned numbers (n = number of positions)
    
    Used in: Division, bit extraction, serial communication
    """
    if positions >= len(binary):
        return '0'
    result = '0' * positions + binary[:-positions]
    # Remove leading zeros but keep at least one
    result = result.lstrip('0') or '0'
    return result

def ones_complement(binary):
    """
    1's Complement
    
    Operation: Invert all bits (0 → 1, 1 → 0)
    
    Used for: Representing negative numbers (older method),
    bitwise NOT operation, network checksums
    
    Note: Range for n bits is -(2^n - 1) to +(2^n - 1)
    Has two representations of 0: +0 and -0
    """
    result = ''.join('1' if bit == '0' else '0' for bit in binary)
    return result

def twos_complement(binary):
    """
    2's Complement
    
    Operation: Invert all bits and add 1
    
    This is the standard method for representing negative numbers
    in modern computers because:
    - Only one representation of 0
    - Arithmetic operations work naturally
    - Range for n bits is -2^(n-1) to +(2^(n-1) - 1)
    
    Algorithm: 2's complement = 1's complement + 1
    """
    ones = ones_complement(binary)
    result, _ = binary_addition(ones, '1')
    return result

def increment(binary):
    """
    Increment Operation
    
    Operation: Add 1 to the binary number
    
    Micro-operation: Used in program counters, loop counters,
    stack pointers, and address calculations
    
    Hardware: Implemented using half-adders for LSB and
    full adders for remaining bits
    """
    result, _ = binary_addition(binary, '1')
    return result

def decrement(binary):
    """
    Decrement Operation
    
    Operation: Subtract 1 from the binary number
    
    Micro-operation: Used in loop counters, stack pointers,
    and countdown operations
    
    Hardware: Implemented using subtraction circuit or
    by adding 2's complement of 1
    """
    result, _ = binary_subtraction(binary, '1')
    # Clean up the result
    max_len = len(binary)
    if len(result) > max_len:
        # Take only the relevant bits
        result = result[-max_len:]
    return result

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests"""
    try:
        data = request.get_json()
        
        operation = data.get('operation')
        operand1 = data.get('operand1', '').strip()
        operand2 = data.get('operand2', '').strip()
        
        # Validate inputs
        if not is_valid_binary(operand1):
            return jsonify({
                'success': False,
                'error': 'Invalid binary input. Please enter only 0s and 1s.'
            })
        
        result = None
        explanation = ''
        
        if operation in ['addition', 'subtraction', 'multiplication', 'division']:
            if not operand2:
                return jsonify({
                    'success': False,
                    'error': 'Second operand is required for this operation.'
                })
            if not is_valid_binary(operand2):
                return jsonify({
                    'success': False,
                    'error': 'Invalid second operand. Please enter only 0s and 1s.'
                })
        
        # Perform operations
        if operation == 'addition':
            result, carry = binary_addition(operand1, operand2)
            explanation = f"Binary Addition: {operand1} + {operand2} = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} + {int(operand2, 2)} = {int(result, 2)}"
            if carry:
                explanation += f"\nNote: Carry out = {carry}"
            
        elif operation == 'subtraction':
            result, is_negative = binary_subtraction(operand1, operand2)
            explanation = f"Binary Subtraction: {operand1} - {operand2} = {result}\n"
            explanation += f"Method: 2's Complement ({operand1} + {twos_complement(operand2.zfill(max(len(operand1), len(operand2))))})\n"
            explanation += f"Decimal: {int(operand1, 2)} - {int(operand2, 2)} = {int(operand1, 2) - int(operand2, 2)}"
            
        elif operation == 'multiplication':
            result, _ = binary_multiplication(operand1, operand2)
            explanation = f"Binary Multiplication: {operand1} × {operand2} = {result}\n"
            explanation += f"Method: Shift and Add\n"
            explanation += f"Decimal: {int(operand1, 2)} × {int(operand2, 2)} = {int(result, 2)}"
            
        elif operation == 'division':
            quotient, remainder, error = binary_division(operand1, operand2)
            if error:
                return jsonify({
                    'success': False,
                    'error': 'Division by zero is not allowed.'
                })
            result = f"Quotient: {quotient}"
            if remainder != '0':
                result += f", Remainder: {remainder}"
            explanation = f"Binary Division: {operand1} ÷ {operand2}\n"
            explanation += f"Quotient: {quotient}, Remainder: {remainder}\n"
            explanation += f"Decimal: {int(operand1, 2)} ÷ {int(operand2, 2)} = {int(quotient, 2)} R {int(remainder, 2)}"
            
        elif operation == 'shift_left':
            positions = data.get('positions', 1)
            result = logical_shift_left(operand1, positions)
            explanation = f"Logical Shift Left by {positions} position(s): {operand1} → {result}\n"
            explanation += f"Effect: Multiplication by 2^{positions} = {2**positions}\n"
            explanation += f"Decimal: {int(operand1, 2)} × {2**positions} = {int(result, 2)}"
            
        elif operation == 'shift_right':
            positions = data.get('positions', 1)
            result = logical_shift_right(operand1, positions)
            explanation = f"Logical Shift Right by {positions} position(s): {operand1} → {result}\n"
            explanation += f"Effect: Division by 2^{positions} = {2**positions} (for unsigned)\n"
            explanation += f"Decimal: {int(operand1, 2)} ÷ {2**positions} = {int(operand1, 2) // (2**positions)}"
            
        elif operation == 'ones_complement':
            result = ones_complement(operand1)
            explanation = f"1's Complement: {operand1} → {result}\n"
            explanation += f"Method: Invert all bits (0→1, 1→0)\n"
            explanation += f"Decimal: {int(operand1, 2)} → {-int(operand1, 2) if operand1[0] == '0' else int(result, 2)}"
            
        elif operation == 'twos_complement':
            result = twos_complement(operand1)
            explanation = f"2's Complement: {operand1} → {result}\n"
            explanation += f"Method: 1's complement + 1\n"
            explanation += f"Decimal: {int(operand1, 2)} → {-int(operand1, 2)}"
            
        elif operation == 'increment':
            result = increment(operand1)
            explanation = f"Increment: {operand1} + 1 = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} + 1 = {int(result, 2)}"
            
        elif operation == 'decrement':
            result = decrement(operand1)
            explanation = f"Decrement: {operand1} - 1 = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} - 1 = {int(result, 2)}"
            
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid operation selected.'
            })
        
        return jsonify({
            'success': True,
            'result': result,
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/convert', methods=['POST'])
def convert():
    """Convert between binary and decimal"""
    try:
        data = request.get_json()
        binary = data.get('binary', '').strip()
        decimal = data.get('decimal')
        
        if binary:
            if not is_valid_binary(binary):
                return jsonify({
                    'success': False,
                    'error': 'Invalid binary input.'
                })
            dec_result = int(binary, 2)
            return jsonify({
                'success': True,
                'decimal': dec_result,
                'binary': binary
            })
        elif decimal is not None:
            try:
                dec_val = int(decimal)
                if dec_val < 0:
                    return jsonify({
                        'success': False,
                        'error': 'Please enter a positive number.'
                    })
                bin_result = bin(dec_val)[2:]
                return jsonify({
                    'success': True,
                    'decimal': dec_val,
                    'binary': bin_result
                })
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid decimal input.'
                })
        
        return jsonify({
            'success': False,
            'error': 'No input provided.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

if __name__ == '__main__':
    print("=" * 60)
    print("  Arithmetic Micro-Operations Calculator")
    print("  Web Application for Computer Organization & Architecture")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5001)