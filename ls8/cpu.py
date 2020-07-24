"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
ADD = 0b10100000
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b1010100
JEQ = 0b1010101
JNE = 0b1010110

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #list
        self.pc = 0  #program counter
        self.running = False
        self.ram = [0]* 256
        self.reg = [0] * 8 #stack pointer at 8
        #initial value of where the stack pointer 
        self.reg[SP] = 0xf4
        self.fl = 0


        #read the ram
    def ram_read(self,index):
        return self.ram[index]

        #write function
    def ram_write(self, index, value):
        self.ram[index] = value    

    def load(self):
        """Load a program into memory."""

        address = 0
        
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                else:
                    value = int(line, 2)
                    self.ram[address] = value
                    address += 1
       



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            self.reg[reg_a] == self.reg[reg_b]
            self.fl = 1    
       
            
        


        else:
            raise Exception("Unsupported ALU operation")

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
        ###########################
        #When we have too many variables > 8
        #We need to use the stack to store this extra information
        #Stack: Push, Pop, storage
        #We will use RAM,memory
        ###########################
        

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            #self.trace()
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3 
                

            elif instruction == HLT:
                running = False

                self.pc += 1
                
            elif instruction == PRN:
                reg_num = operand_a
                print(self.reg[reg_num])
            
                self.pc += 2

            elif instruction == MUL:
            
                self.alu("MUL", operand_a, operand_b) 
                self.pc +=3

            elif instruction == PUSH:
                #self.trace()
                #print('Push')
                value = self.reg[operand_a]
                #dec the stack pointer by 1
                self.reg[SP] -= 1
                reg_k = self.ram[self.pc + 1]
                reg_value = self.reg[reg_k]
                #put the value at the stack pointer address
                latest_stack_address = self.reg[SP]
                self.ram[latest_stack_address] = reg_value
                self.ram_write(value,self.reg[SP])
                
                self.pc += 2

            elif instruction == POP:

                # #get the stack pointer
                value = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                # #get register number to put value in
                self.reg[operand_a] = value
                # # increment pc counter
                self.pc += 2
            elif instruction == CALL:
                #print('CALL')
                #dec the stack pointer
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                self.pc = self.reg[operand_a]
            elif instruction == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1
            elif instruction == CMP:
                #compare operand a and b
                first_address = self.ram_read(self.pc + 1)
                second_address = self.ram_read(self.pc + 2)
                self.alu("CMP", first_address, second_address)
                #inc pc by 3 - cmp take 2 args = 3bytes
                self.pc += 3

            elif instruction == JMP:
                #Jump to the address stored in the given register.
                reg_address = self.ram_read(self.pc + 1)
                self.pc = self.reg[reg_address]
            elif instruction == JEQ:
                #If `equal` flag is set (true), 
                # jump to the address stored in the given register.
                reg_address = self.ram_read(self.pc + 1)
                if self.fl == 1:
                    self.pc = self.reg[reg_address]
                else:
                    self.pc += 2    
            elif instruction == JNE:
                # If `E` flag is clear (false, 0), 
                # jump to the address stored in the given register.   
                reg_address = self.ram_read(self.pc + 1)
                if self.fl == 0:
                    self.pc = self.reg[reg_address]
                else:
                    self.pc += 2    

            else:
                print(f' Unknown, {instruction}')   
                running = False    
