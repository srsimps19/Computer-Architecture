"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg= [0] * 8
        self.pc = 0
        self.halted = False

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as programFile:
            for line in programFile:
                splitLine = line.split("#")
                numLine = splitLine[0].strip()
                if numLine == '':
                    continue
                decVal = int(numLine, 2)
                self.ram[address] = decVal
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                self.halted = True
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                self.pc += 3
            else:
                print("I did not understand that command.")
