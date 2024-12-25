import struct
import json
import sys

# Constants for instruction opcodes
OPCODES = {
    "LOAD_CONST": 181,
    "READ_MEM": 120,
    "WRITE_MEM": 92,
    "UNARY_SGN": 119,
}

# Asssembler: Converts assembly instructions to binary
class Assembler:
    def __init__(self):
        self.log = []

    def assemble_instruction(self, mnemonic, operand):
        if mnemonic == "LOAD_CONST":
            opcode = OPCODES[mnemonic]
            binary = struct.pack('<BQ', opcode, operand & 0x1FFFFFFF)  # Mask to 29 bits
        elif mnemonic in ["READ_MEM", "WRITE_MEM", "UNARY_SGN"]:
            opcode = OPCODES[mnemonic]
            binary = struct.pack('<BH', opcode, operand)
        else:
            raise ValueError(f"Unknown instruction: {mnemonic}")
        self.log.append({"mnemonic": mnemonic, "operand": operand, "binary": list(binary)})
        return binary

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        binary_code = b''
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Invalid instruction format: {line}")

            mnemonic, operand = parts[0], int(parts[1])
            binary_code += self.assemble_instruction(mnemonic, operand)

        with open(output_file, 'wb') as f:
            f.write(binary_code)

        with open(log_file, 'w') as f:
            json.dump(self.log, f, indent=4)

# Interpreter: Executes binary instructions
class Interpreter:
    def __init__(self):
        self.memory = [0] * 1024
        self.stack = []

    def load_const(self, value):
        self.stack.append(value)

    def read_mem(self, address):
        self.stack.append(self.memory[address])

    def write_mem(self, address):
        value = self.stack.pop()
        self.memory[address] = value

    def unary_sgn(self, address):
        value = self.stack.pop()
        self.memory[address] = 1 if value > 0 else -1 if value < 0 else 0

    def execute(self, binary_file, result_file, memory_range):
        with open(binary_file, 'rb') as f:
            code = f.read()

        pc = 0
        while pc < len(code):
            opcode = code[pc]
            pc += 1

            if opcode == OPCODES["LOAD_CONST"]:
                operand = struct.unpack('<Q', code[pc:pc+8])[0] & 0x1FFFFFFF  # Decode 29 bits
                self.load_const(operand)
                pc += 8
            elif opcode == OPCODES["READ_MEM"]:
                operand, = struct.unpack('<H', code[pc:pc+2])
                self.read_mem(operand)
                pc += 2
            elif opcode == OPCODES["WRITE_MEM"]:
                operand, = struct.unpack('<H', code[pc:pc+2])
                self.write_mem(operand)
                pc += 2
            elif opcode == OPCODES["UNARY_SGN"]:
                operand, = struct.unpack('<H', code[pc:pc+2])
                self.unary_sgn(operand)
                pc += 2
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

        start, end = memory_range
        with open(result_file, 'w') as f:
            json.dump(self.memory[start:end], f, indent=4)

# Main execution
if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "assemble":
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        log_file = sys.argv[4]
        assembler = Assembler()
        assembler.assemble(input_file, output_file, log_file)
    elif mode == "interpret":
        binary_file = sys.argv[2]
        result_file = sys.argv[3]
        memory_start = int(sys.argv[4])
        memory_end = int(sys.argv[5])
        interpreter = Interpreter()
        interpreter.execute(binary_file, result_file, (memory_start, memory_end))
    else:
        print("Unknown mode. Use 'assemble' or 'interpret'.")
