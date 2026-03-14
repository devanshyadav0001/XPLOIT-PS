# 🛠️ Bad Compiler Challenge — Final Documentation

## 1. Executive Summary
This project involved the reverse engineering of a broken stack-based compiler (`broken_compiler.exe`) to understand its underlying bytecode language (`.wut`), identify critical bugs, and implement a corrected interpreter to successfully execute programs.

## 2. Reverse Engineering Process (Step-by-Step)

### Phase 1: Initial Discovery & Static Analysis
We began by analyzing the `broken_compiler.exe` binary. Our primary goal was to understand how it processes `.wut` files.
- **Compiler Identification**: Using header analysis, we identified the binary as being compiled with MinGW GCC 6.3.0.
- **String Extraction**: We identified key error messages like "stack underflow" and "stack empty," which confirmed the language is stack-based.

### Phase 2: Disassembly & Instruction Mapping
Using the `capstone` engine, we disassembled the binary to find the core execution loop.
- **The Dispatcher**: We located the main bytecode processor which reads characters one by one.
- **Jump Table Analysis**: At address `0x004040f4`, we discovered a **Jump Table**. This is the heart of the compiler. It maps each ASCII character (starting from `!`) to the memory address of its specific logic handler.
- **Handler Deduction**: We analyzed each handler address. For example, the handler at `0x4023c0` parsed digits for the `(` instruction, while `0x402480` performed addition for core `%`.

### Phase 3: Operator Semantics Identification
By tracing the stack pointer manipulation in each handler, we reconstructed the instruction set:
| Char | Operation | Technical Logic |
| :--- | :--- | :--- |
| `(N` | **PUSH** | Parses integer `N` into the stack. |
| `~`  | **PUSH_A** | Pushes constant `65`. |
| `%`  | **ADD** | Pops two, pushes `sum`. |
| `#`  | **NEGATE** | Multiplies top by `-1`. |
| `!`  | **INC** | Increments top value. |
| `@`  | **DEC** | Decrements top value. |
| `$`  | **SWAP** | Reorders top two elements. |
| `^`  | **PEEK-PRINT**| Output top as ASCII (No Pop). |
| `` ` `` | **DROP** | Pops and discards. |
| `&`  | **LOOP START**| Jumps to `*` if top is 0. |
| `*`  | **LOOP END** | Jumps back to `&` if top is not 0. |
| `)`  | **COMMENT** | Consumes all chars until `\n`. |

### Phase 4: Bug Hunting
By comparing the binary logic to the expected behavior of `program.wut`, we found three critical errors in the original `broken_compiler.exe`:
1. **Faulty SWAP**: The `$!` handler incorrectly pushed twice instead of swapping.
2. **Destructive Output**: The `^` handler incorrectly decremented the stack pointer after printing.
3. **Loop Tracking**: The original compiler failed to handle nested loop depths correctly.

## 3. Deliverables

All deliverables are located within this folder for the Pull Request:
- **fixed_compiler.py**: The corrected WUT interpreter (Python based).
- **showcase.wut**: A program demonstrating "Tupolev - FIXED!" with loops.
- **program.wut**: The original challenge program, modified to prefix the team name.

## 4. Verification Commands

Run these commands from within the `bad_compiler` directory:

### ✅ Check Showcase Program
```bash
python fixed_compiler.py showcase.wut
```
*Expected Output: Prints "Tupolev - FIXED!" and a star pattern.*

### ✅ Check Modified Challenge Program
```bash
python fixed_compiler.py program.wut
```
*Expected Output: Prints "Tupolev - This is right! Congratulations!"*
