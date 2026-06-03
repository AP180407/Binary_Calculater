from flask import Flask, render_template, request, jsonify
import re
import json
import os
from datetime import datetime

app = Flask(__name__)

HISTORY_FILE = 'calculation_history.json'

# ==================== INPUT VALIDATION ====================

def is_valid_binary(binary_str):
    """Validate that input contains only binary digits and optional single decimal point"""
    if not binary_str:
        return False
    # Allow binary integers (e.g., "1010") and binary floats (e.g., "1010.11")
    pattern = r'^[01]+(\.[01]+)?$'
    return bool(re.match(pattern, binary_str))

def is_valid_binary_integer(binary_str):
    """Validate that input is a binary integer (no decimal point)"""
    if not binary_str:
        return False
    pattern = r'^[01]+$'
    return bool(re.match(pattern, binary_str))

def normalize_binary(binary_str, length=None):
    """Normalize binary string to specified length by padding with zeros"""
    if length:
        return binary_str.zfill(length)
    return binary_str

# ==================== FLOATING-POINT CONVERSION ====================

def binary_fraction_to_decimal(binary_str):
    """Convert a binary string (integer or floating-point) to decimal"""
    if '.' in binary_str:
        integer_part, fraction_part = binary_str.split('.')
        int_val = int(integer_part, 2) if integer_part else 0
        frac_val = 0
        for i, bit in enumerate(fraction_part):
            frac_val += int(bit) * (2 ** -(i + 1))
        return int_val + frac_val
    else:
        return int(binary_str, 2)

def decimal_to_binary_fraction(decimal_val):
    """Convert a decimal number to binary string (supports floating-point)"""
    if decimal_val == 0:
        return '0'
    
    is_negative = decimal_val < 0
    decimal_val = abs(decimal_val)
    
    integer_part = int(decimal_val)
    fraction_part = decimal_val - integer_part
    
    # Convert integer part
    if integer_part == 0:
        int_binary = '0'
    else:
        int_binary = bin(integer_part)[2:]
    
    # Convert fraction part
    if fraction_part == 0:
        return ('-' if is_negative else '') + int_binary
    
    frac_binary = ''
    max_bits = 20  # Limit precision
    seen = set()
    
    while fraction_part > 0 and len(frac_binary) < max_bits:
        fraction_part *= 2
        if fraction_part >= 1:
            frac_binary += '1'
            fraction_part -= 1
        else:
            frac_binary += '0'
        
        # Detect repeating patterns
        key = round(fraction_part, 10)
        if key in seen:
            break
        seen.add(key)
    
    result = int_binary + '.' + frac_binary if frac_binary else int_binary
    return ('-' if is_negative else '') + result

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
    steps = []
    
    # Process from right to left (LSB to MSB)
    for i in range(max_len - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])
        
        # Full adder logic
        sum_bit = bit_a ^ bit_b ^ carry
        carry_out = (bit_a & bit_b) | (carry & (bit_a ^ bit_b))
        
        steps.append({
            'position': max_len - 1 - i,
            'bit_a': bit_a,
            'bit_b': bit_b,
            'carry_in': carry,
            'sum': sum_bit,
            'carry_out': carry_out
        })
        
        carry = carry_out
        result.insert(0, str(sum_bit))
    
    # If there's a final carry, add it
    if carry:
        result.insert(0, '1')
    
    return ''.join(result), carry, steps

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
    
    steps = []
    
    # Calculate 2's complement of b
    # Step 1: 1's complement (invert all bits)
    ones_comp = ''.join('1' if bit == '0' else '0' for bit in b)
    steps.append({
        'phase': "1's Complement",
        'description': f"Invert all bits of {b}",
        'result': ones_comp
    })
    
    # Step 2: Add 1 to get 2's complement
    twos_comp, _, add_steps = binary_addition(ones_comp, '1')
    twos_comp = twos_comp.zfill(max_len)
    steps.append({
        'phase': "2's Complement",
        'description': f"Add 1 to 1's complement: {ones_comp} + 1",
        'result': twos_comp
    })
    
    # Step 3: Add a + (2's complement of b)
    result, carry, final_add_steps = binary_addition(a, twos_comp)
    steps.append({
        'phase': "Final Addition",
        'description': f"Add {a} + {twos_comp}",
        'result': result,
        'add_steps': final_add_steps
    })
    
    # If result is longer than max_len, there was overflow (positive result)
    # If carry is 0, result is negative (in 2's complement form)
    is_negative = not carry
    
    return result, is_negative, steps

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
        return '0', False, []
    
    # Convert to decimal for easier handling
    multiplicand = int(a, 2)
    multiplier = int(b, 2)
    
    product = 0
    steps = []
    
    # Shift and add algorithm
    iteration = 0
    while multiplier > 0:
        if multiplier & 1:  # If LSB is 1
            shifted = multiplicand << iteration
            product += shifted
            steps.append({
                'iteration': iteration + 1,
                'multiplier_bit': 1,
                'action': 'Add',
                'shifted_value': bin(shifted)[2:],
                'shift_amount': iteration,
                'partial_product': bin(product)[2:]
            })
        else:
            steps.append({
                'iteration': iteration + 1,
                'multiplier_bit': 0,
                'action': 'Skip',
                'shifted_value': '0',
                'shift_amount': iteration,
                'partial_product': bin(product)[2:]
            })
        iteration += 1
        multiplier >>= 1
    
    result = bin(product)[2:]
    return result, False, steps

def binary_division(dividend, divisor):
    """
    Binary Division using Restoring Division Algorithm
    
    Algorithm:
    1. Initialize quotient to 0
    2. Shift dividend left, bring down next bit
    3. Subtract divisor from current dividend portion
    4. If result is positive, set quotient bit to 1
    5. If result is negative, restore dividend and set quotient bit to 0
    
    Returns: (quotient, remainder, error, steps)
    """
    # Handle edge cases
    if divisor == '0' or int(divisor, 2) == 0:
        return None, None, True, []
    
    dividend_val = int(dividend, 2)
    divisor_val = int(divisor, 2)
    
    if dividend_val == 0:
        return '0', '0', False, []
    
    steps = []
    current_remainder = 0
    quotient_bits = []
    
    for i in range(len(dividend)):
        bit = int(dividend[i])
        current_remainder = (current_remainder << 1) | bit
        
        subtract_val = current_remainder - divisor_val
        
        if subtract_val >= 0:
            quotient_bits.append('1')
            current_remainder = subtract_val
            steps.append({
                'step': i + 1,
                'bit_brought_down': bit,
                'current_value': bin(current_remainder + divisor_val)[2:] if subtract_val >= 0 else bin(current_remainder)[2:],
                'after_subtract': bin(subtract_val)[2:] if subtract_val >= 0 else 'negative',
                'quotient_bit': '1',
                'action': 'Positive - set quotient bit to 1'
            })
        else:
            quotient_bits.append('0')
            steps.append({
                'step': i + 1,
                'bit_brought_down': bit,
                'current_value': bin(current_remainder)[2:],
                'after_subtract': 'negative',
                'quotient_bit': '0',
                'action': 'Negative - restore, set quotient bit to 0'
            })
    
    quotient = ''.join(quotient_bits).lstrip('0') or '0'
    remainder = bin(current_remainder)[2:]
    
    return quotient, remainder, False, steps

# ==================== ADDITIONAL MICRO-OPERATIONS ====================

def logical_shift_left(binary, positions=1):
    """
    Logical Shift Left (LSL)
    
    Operation: Shift all bits left by specified positions
    - Vacated positions on right are filled with 0
    - Leftmost bits are lost (or stored in carry flag)
    
    Effect: Multiplication by 2^n (n = number of positions)
    """
    steps = []
    current = binary
    for i in range(positions):
        shifted = current + '0'
        steps.append({
            'shift': i + 1,
            'before': current,
            'after': shifted,
            'bit_shifted_out': '0',
            'effect': f'Multiply by 2'
        })
        current = shifted
    return current, steps

def logical_shift_right(binary, positions=1):
    """
    Logical Shift Right (LSR)
    
    Operation: Shift all bits right by specified positions
    - Vacated positions on left are filled with 0
    - Rightmost bits are lost
    
    Effect: Division by 2^n for unsigned numbers
    """
    steps = []
    current = binary
    for i in range(positions):
        if len(current) <= 1:
            shifted = '0'
        else:
            shifted = '0' + current[:-1]
        bit_out = current[-1] if len(current) > 0 else '0'
        steps.append({
            'shift': i + 1,
            'before': current,
            'after': shifted,
            'bit_shifted_out': bit_out,
            'effect': f'Divide by 2'
        })
        current = shifted
        current = current.lstrip('0') or '0'
    return current, steps

def ones_complement(binary):
    """
    1's Complement - Invert all bits
    """
    steps = []
    result = ''
    for i, bit in enumerate(binary):
        inverted = '1' if bit == '0' else '0'
        result += inverted
        steps.append({
            'position': i,
            'original': bit,
            'inverted': inverted
        })
    return result, steps

def twos_complement(binary):
    """
    2's Complement - Invert all bits and add 1
    """
    ones, ones_steps = ones_complement(binary)
    result, carry, add_steps = binary_addition(ones, '1')
    steps = {
        'ones_complement': {
            'result': ones,
            'bit_steps': ones_steps
        },
        'add_one': {
            'operation': f"{ones} + 1",
            'result': result,
            'carry': carry,
            'add_steps': add_steps
        }
    }
    return result, steps

def increment(binary):
    """Increment: Add 1 to binary number"""
    result, carry, steps = binary_addition(binary, '1')
    return result, steps

def decrement(binary):
    """Decrement: Subtract 1 from binary number"""
    result, is_negative, steps = binary_subtraction(binary, '1')
    max_len = len(binary)
    if len(result) > max_len:
        result = result[-max_len:]
    return result, steps

# ==================== CALCULATION HISTORY ====================

def load_history():
    """Load calculation history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history):
    """Save calculation history to JSON file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_to_history(operation, operand1, operand2, result, explanation):
    """Add a calculation to history"""
    history = load_history()
    entry = {
        'id': len(history) + 1,
        'timestamp': datetime.now().isoformat(),
        'operation': operation,
        'operand1': operand1,
        'operand2': operand2,
        'result': result,
        'explanation': explanation
    }
    history.insert(0, entry)  # Newest first
    # Keep only last 100 entries
    if len(history) > 100:
        history = history[:100]
    save_history(history)
    return entry

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
                'error': 'Invalid binary input. Please enter only 0s and 1s (with optional decimal point for floats).'
            })
        
        result = None
        explanation = ''
        steps = []
        decimal_operand1 = binary_fraction_to_decimal(operand1)
        decimal_operand2 = binary_fraction_to_decimal(operand2) if operand2 and is_valid_binary(operand2) else None
        
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
        
        is_float_operation = '.' in operand1 or (operand2 and '.' in operand2)
        
        # Handle floating-point operations
        if is_float_operation and operation in ['addition', 'subtraction', 'multiplication', 'division']:
            dec1 = binary_fraction_to_decimal(operand1)
            dec2 = binary_fraction_to_decimal(operand2)
            
            if operation == 'addition':
                dec_result = dec1 + dec2
            elif operation == 'subtraction':
                dec_result = dec1 - dec2
            elif operation == 'multiplication':
                dec_result = dec1 * dec2
            elif operation == 'division':
                if dec2 == 0:
                    return jsonify({
                        'success': False,
                        'error': 'Division by zero is not allowed.'
                    })
                dec_result = dec1 / dec2
            
            result = decimal_to_binary_fraction(dec_result)
            explanation = f"Binary {operation.title()}: {operand1} {['+', '-', '×', '÷'][['addition', 'subtraction', 'multiplication', 'division'].index(operation)]} {operand2} = {result}\n"
            explanation += f"Decimal: {dec1} {['+', '-', '×', '÷'][['addition', 'subtraction', 'multiplication', 'division'].index(operation)]} {dec2} = {dec_result}"
            steps = [{'type': 'floating_point', 'decimal_op': f"{dec1} {['+', '-', '×', '÷'][['addition', 'subtraction', 'multiplication', 'division'].index(operation)]} {dec2} = {dec_result}"}]
        
        # Integer operations
        elif operation == 'addition':
            result, carry, steps = binary_addition(operand1, operand2)
            explanation = f"Binary Addition: {operand1} + {operand2} = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} + {int(operand2, 2)} = {int(result, 2)}"
            if carry:
                explanation += f"\nNote: Carry out = {carry}"
        
        elif operation == 'subtraction':
            result, is_negative, steps = binary_subtraction(operand1, operand2)
            explanation = f"Binary Subtraction: {operand1} - {operand2} = {result}\n"
            explanation += f"Method: 2's Complement ({operand1} + {twos_complement(operand2.zfill(max(len(operand1), len(operand2))))[0]})\n"
            explanation += f"Decimal: {int(operand1, 2)} - {int(operand2, 2)} = {int(operand1, 2) - int(operand2, 2)}"
        
        elif operation == 'multiplication':
            result, _, steps = binary_multiplication(operand1, operand2)
            explanation = f"Binary Multiplication: {operand1} × {operand2} = {result}\n"
            explanation += f"Method: Shift and Add\n"
            explanation += f"Decimal: {int(operand1, 2)} × {int(operand2, 2)} = {int(result, 2)}"
        
        elif operation == 'division':
            quotient, remainder, error, steps = binary_division(operand1, operand2)
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
            result, steps = logical_shift_left(operand1, positions)
            explanation = f"Logical Shift Left by {positions} position(s): {operand1} → {result}\n"
            explanation += f"Effect: Multiplication by 2^{positions} = {2**positions}\n"
            explanation += f"Decimal: {int(operand1, 2)} × {2**positions} = {int(result, 2)}"
        
        elif operation == 'shift_right':
            positions = data.get('positions', 1)
            result, steps = logical_shift_right(operand1, positions)
            explanation = f"Logical Shift Right by {positions} position(s): {operand1} → {result}\n"
            explanation += f"Effect: Division by 2^{positions} = {2**positions} (for unsigned)\n"
            explanation += f"Decimal: {int(operand1, 2)} ÷ {2**positions} = {int(operand1, 2) // (2**positions)}"
        
        elif operation == 'ones_complement':
            result, steps = ones_complement(operand1)
            explanation = f"1's Complement: {operand1} → {result}\n"
            explanation += f"Method: Invert all bits (0→1, 1→0)\n"
            explanation += f"Decimal: {int(operand1, 2)} → {-int(operand1, 2) if operand1[0] == '0' else int(result, 2)}"
        
        elif operation == 'twos_complement':
            result, steps = twos_complement(operand1)
            explanation = f"2's Complement: {operand1} → {result}\n"
            explanation += f"Method: 1's complement + 1\n"
            explanation += f"Decimal: {int(operand1, 2)} → {-int(operand1, 2)}"
        
        elif operation == 'increment':
            result, steps = increment(operand1)
            explanation = f"Increment: {operand1} + 1 = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} + 1 = {int(result, 2)}"
        
        elif operation == 'decrement':
            result, steps = decrement(operand1)
            explanation = f"Decrement: {operand1} - 1 = {result}\n"
            explanation += f"Decimal: {int(operand1, 2)} - 1 = {int(result, 2)}"
        
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid operation selected.'
            })
        
        # Save to history
        history_entry = add_to_history(
            operation, operand1, operand2, 
            result if isinstance(result, str) else str(result),
            explanation
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'explanation': explanation,
            'steps': steps,
            'decimal_operand1': decimal_operand1,
            'decimal_operand2': decimal_operand2,
            'history_entry': history_entry
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
            dec_result = binary_fraction_to_decimal(binary)
            return jsonify({
                'success': True,
                'decimal': dec_result,
                'binary': binary
            })
        elif decimal is not None:
            try:
                dec_val = float(decimal)
                if dec_val < 0:
                    return jsonify({
                        'success': False,
                        'error': 'Please enter a positive number.'
                    })
                bin_result = decimal_to_binary_fraction(dec_val)
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

# ==================== HISTORY API ====================

@app.route('/history', methods=['GET'])
def get_history():
    """Get all calculation history"""
    history = load_history()
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/history/clear', methods=['POST'])
def clear_history():
    """Clear all calculation history"""
    save_history([])
    return jsonify({
        'success': True,
        'message': 'History cleared successfully.'
    })

@app.route('/history/<int:entry_id>', methods=['DELETE'])
def delete_history_entry(entry_id):
    """Delete a specific history entry"""
    history = load_history()
    history = [entry for entry in history if entry.get('id') != entry_id]
    save_history(history)
    return jsonify({
        'success': True,
        'message': f'Entry {entry_id} deleted.'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  Arithmetic Micro-Operations Calculator")
    print("  Web Application for Computer Organization & Architecture")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5001)