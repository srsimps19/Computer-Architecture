"""CPU functionality."""

import sys

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD  = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

SP = 7

EQUAL = 0b001
LESS = 0b100
GREATER = 0b010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False
        self.branchTable = {
            ADD: self.op_add,
            AND: self.op_and,
            CALL: self.op_call,
            CMP: self.op_cmp,
            DEC: self.op_dec,
            DIV: self.op_div,
            HLT: self.op_hlt,
            INC: self.op_inc,
            INT: self.op_int,
            IRET: self.op_iret,
            JEQ: self.op_jeq,
            JGE: self.op_jge,
            JGT: self.op_jgt,
            JLE: self.op_jle,
            JLT: self.op_jlt,
            JMP: self.op_jmp,
            JNE: self.op_jne,
            LD: self.op_ld,
            LDI: self.op_ldi,
            MOD: self.op_mod,
            MUL: self.op_mul,
            NOP: self.op_nop,
            NOT: self.op_not,
            OR: self.op_or,
            POP: self.op_pop,
            PRA: self.op_pra,
            PRN: self.op_prn,
            PUSH: self.op_push,
            RET: self.op_ret,
            SHL: self.op_shl,
            SHR: self.op_shr,
            ST: self.op_st,
            SUB: self.op_sub,
            XOR: self.op_xor,
        }


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
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "CMP":
            self.flags = self.flags & 0x11111000
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = self.flags | LESS
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = self.flags | GREATER
            else:
                self.flags = self.flags | EQUAL
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "DIV":
            if self.reg[reg_b] > 0:
                self.reg[reg_a] /= self.reg[reg_b]
            else:
                print("Cannot divide by 0")
                self.op_hlt(self.reg[reg_a], self.reg[reg_b])
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "MOD":
            if self.reg[reg_b] > 0:
                self.reg[reg_a] %= self.reg[reg_b]
            else:
                print("Cannot divide by 0")
                self.op_hlt(self.reg[reg_a], self.reg[reg_b])
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "NOT":
            ~self.reg[reg_a]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def push_val(self, val):
        self.reg[SP] -= 1
        self.ram_write(val, self.reg[7])
        
    def pop_val(self):
        val = self.ram_read(self.reg[7])
        self.reg[SP] += 1
        return val

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

            instructionSize = ((ir >> 6)) + 1
            self.setOwnPC = ((ir >> 4) & 0b1) == 1

            if ir in self.branchTable:
                self.branchTable[ir](operand_a, operand_b)
            else:
                print(f"Invalid instruction")
            
            if not self.setOwnPC:
                self.pc += instructionSize

    def op_hlt(self, operand_a, operand_b):
        self.halted = True
    
    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
    
    def op_add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
    
    def op_sub(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)

    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        
    def op_div(self, operand_a, operand_b):
        self.alu("DIV", operand_a, operand_b)

    def op_and(self, operand_a, operand_b):
        self.alu("AND", operand_a, operand_b)

    def op_push(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])
        
    def op_pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()

    def op_cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)

    def op_jmp(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]

    def op_jeq(self, operand_a, operand_b):
        if self.flags & EQUAL:
            self.pc = self.reg[operand_a]
        else:
            self.setOwnPC = False

    def op_jne(self, operand_a, operand_b):
        if not self.flags & EQUAL:
            self.pc = self.reg[operand_a]
        else:
            self.setOwnPC = False