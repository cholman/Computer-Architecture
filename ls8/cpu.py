"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.return_pc = 0
        self.running = False
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.ADD = 0b10100000
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.JMP = 0b01010100

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        for instruction in program:
            self.ram[address] = instruction
            # print(f"i am an instruction: {self.ram[address]}")
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc\
        elif op == "MUL":
            #accept instruction
            #write to reg_a
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            pass
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        # accept address
        # return it's value
        return self.ram[address]

    def ram_write(self, value, address):
        # take a value
        # write to address
        # no return
        self.ram[address] = value


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
        branch_table = {
            self.LDI : self.ldi,
            self.PRN : self.prn,
            self.MUL : self.mult,
            self.ADD : self.add,
            self.HLT : self.hlt,
            self.PUSH : self.push,
            self.POP : self.pop,
            self.CALL : self.call,
            self.RET : self.ret,
            self.CMP : self.cmp,
            self.JEQ : self.jeq,
            self.JNE : self.jne,
            self.JMP : self.jmp
        }
        self.reg[self.sp] = 0xF4
        
        self.running = True
        while self.running:
            # ir is the value in ram at the index of pc
            ir = self.ram[self.pc]
            # check if the value is in our hash table
            if ir in branch_table:
            
                branch_table[ir]()
            elif ir not in branch_table:
                print(f"Unknown instruction {ir} at address {self.pc}")
                sys.exit(1)
        # while self.running:
        #     ir = self.ram[self.pc]

        #     if ir == self.LDI:
        #         self.ldi()

        #     elif ir == self.PRN:
        #         self.prn()

        #     elif ir == self.HLT:
        #         running = self.hlt()
        #     elif ir == self.MUL:
        #         running = self.mult()
        #     else:
        #         print(f"unknown instruction {ir} at address {self.pc}")
        #         sys.exit(1)


    def ldi(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value
        self.pc += 3

    def prn(self):
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        print(value)
        # print(self.ram)
        # print(self.reg)
        print("address", address)
        self.pc += 2

    def hlt(self):
        self.pc += 1
        self.running = False

    def mult(self):
        # a = self.ram[self.pc + 1]
        # b = self.ram[self.pc + 2]
        self.alu("MUL", 0, 1)
        print(f'RAM: {self.ram}')
        print(f'Reg: {self.reg}')
        self.pc += 3

    def add(self):
        self.alu("ADD", 0, 0)
        print(f'RAM: {self.ram}')
        print(f'Reg: {self.reg}')
        self.pc += 3

    def mod(self):
        self.alu("MOD", 0, 1)
    
    def call(self):
        # self.return_pc = self.pc + 2
        return_pc = self.pc + 2
        # print("reg address in CALL:", return_pc)
        # print("value in reg: ", self.reg[return_pc])


        self.reg[self.sp] -= 1
        top_of_stack = self.reg[self.sp]
        self.ram[top_of_stack] = return_pc

        subroutine_pc = self.reg[1]
        self.pc = subroutine_pc

    def ret(self):
        top_of_stack = self.reg[self.sp]
        return_pc = self.ram[top_of_stack]
        self.pc = return_pc

    def push(self):
        #self.reg[7] = 104 
        self.reg[self.sp] -= 1

        address = self.ram[self.pc + 1]
        value = self.reg[address]

        top_loc = self.reg[self.sp]
        self.ram[top_loc] = value
        print("PC", self.pc)

        self.pc += 2

    def pop(self):
        #take value from ram
        top_stack_val = self.reg[self.sp]
        # lets get the register address
        reg_addr = self.ram[self.pc + 1]
        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[reg_addr] = self.ram[top_stack_val]
        self.reg[self.sp] += 1
        self.pc += 2

    def cmp(self):
        pass

    def jeq(self):
        pass

    def jne(self):
        pass

    def jmp(self):
        pass
        
        