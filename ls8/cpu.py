"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        here = []

        try:
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')
                    command_line = split_line[0]
                    if len(command_line) > 0:
                        command_line.strip()
                    if command_line[0] == '1' or command_line[0] == '0':
                        here = command_line.strip()
                        self.ram[address] = int(here, 2)
                        address += 1

        except FileNotFoundError:
            print('file does not exist')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:  # LDI
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:  # PRN
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                # decrement the stack pointer
                self.sp -= 1

                # get what is in the register
                reg_address = self.ram[self.pc + 1]
                value = self.reg[reg_address]

                # store it at that point in the stack
                self.ram[self.sp] = value
                self.pc += 2

            elif IR == POP:
                # Copy the value from the address pointed to by SP to the given register.
                value = self.ram[self.sp]
                target_reg_address = self.ram[self.pc + 1]
                self.reg[target_reg_address] = value
                # Increment SP
                self.sp += 1
                self.pc += 2

            elif IR == HLT:  # HLT
                break
            else:
                print(f"unknown command {IR}")
                break
