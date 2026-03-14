"""
WUT Language Interpreter - FIXED version
"""
import sys

def run_wut(source, debug=False):
    stack = []
    pc = 0
    loop_stack = []
    output = []
    
    while pc < len(source):
        ch = source[pc]
        
        if ch == '(':
            pc += 1
            num_str = ""
            while pc < len(source) and source[pc].isdigit():
                num_str += source[pc]
                pc += 1
            stack.append(int(num_str) if num_str else 0)
            if debug: print(f"  PUSH {stack[-1]} -> {stack}", flush=True)
            continue
            
        elif ch == '~':
            stack.append(65)
            if debug: print(f"  PUSH_A 65 -> {stack}", flush=True)
                
        elif ch == '!':
            if not stack:
                print("Error: stack empty (INC)", file=sys.stderr, flush=True)
                return ''.join(output)
            stack[-1] += 1
            if debug: print(f"  INC -> {stack}", flush=True)
                
        elif ch == '@':
            if not stack:
                print("Error: stack empty (DEC)", file=sys.stderr, flush=True)
                return ''.join(output)
            stack[-1] -= 1
            if debug: print(f"  DEC -> {stack}", flush=True)
                
        elif ch == '#':
            if not stack:
                print("Error: stack empty (NEG)", file=sys.stderr, flush=True)
                return ''.join(output)
            stack[-1] = -stack[-1]
            if debug: print(f"  NEG -> {stack}", flush=True)
                
        elif ch == '$':
            if len(stack) < 2:
                print("Error: stack underflow (SWAP)", file=sys.stderr, flush=True)
                return ''.join(output)
            stack[-1], stack[-2] = stack[-2], stack[-1]
            if debug: print(f"  SWAP -> {stack}", flush=True)
                
        elif ch == '%':
            if len(stack) < 2:
                print("Error: stack underflow (ADD)", file=sys.stderr, flush=True)
                return ''.join(output)
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
            if debug: print(f"  ADD -> {stack}", flush=True)
                
        elif ch == '^':
            if not stack:
                print("Error: stack empty (PRINT)", file=sys.stderr, flush=True)
                return ''.join(output)
            val = stack[-1]
            c = chr(val & 0xFF)
            output.append(c)
            if debug: print(f"  PRINT {val}='{c}'", flush=True)
            else: print(c, end='', flush=True)
                
        elif ch == '&':
            if not stack:
                print("Error: stack underflow (LOOP_START)", file=sys.stderr, flush=True)
                return ''.join(output)
            if stack[-1] != 0:
                loop_stack.append(pc)
                if debug: print(f"  LOOP_START (entering)", flush=True)
            else:
                depth = 1
                pc += 1
                while pc < len(source) and depth > 0:
                    if source[pc] == '&': depth += 1
                    elif source[pc] == '*': depth -= 1
                    pc += 1
                if debug: print(f"  LOOP_START (skipped)", flush=True)
                continue
                
        elif ch == '*':
            if not loop_stack:
                print("Error: unmatched *", file=sys.stderr, flush=True)
                return ''.join(output)
            if not stack:
                print("Error: stack underflow (LOOP_END)", file=sys.stderr, flush=True)
                return ''.join(output)
            if stack[-1] != 0:
                pc = loop_stack[-1]
                if debug: print(f"  LOOP_END (repeating)", flush=True)
            else:
                loop_stack.pop()
                if debug: print(f"  LOOP_END (exiting)", flush=True)
                
        elif ch == '`':
            if not stack:
                print("Error: stack empty (DROP)", file=sys.stderr, flush=True)
                return ''.join(output)
            stack.pop()
            if debug: print(f"  DROP -> {stack}", flush=True)

        elif ch == ')':
            while pc < len(source) and source[pc] != '\n':
                pc += 1
            if debug: print("  COMMENT SKIPPED", flush=True)
            continue

        pc += 1
    
    if not debug: print(flush=True)
    return ''.join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <source file> [--debug]", flush=True)
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        source = f.read()
    
    debug = '--debug' in sys.argv
    run_wut(source, debug=debug)
