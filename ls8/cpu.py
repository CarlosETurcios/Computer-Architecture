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
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        
        

        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0
       

        self.running = True

     
        


       
    
    def ram_read(self, address):

        return self.ram[address]
        

    def ram_write(self, address, data):

        self.ram[address] = data
        
        
       
        
        
            

    def load(self):
        """Load a program into memory."""
        program = []

        try: 
            if len(sys.argv) < 2:
                print(f'Error: missing filename argument')
                sys.exit(1)

            # add a counter that adds memory at that index 
            address = 0
                
            with open(sys.argv[1]) as f:
                for line in f:
                    
                    split_line = line.split("#")[0]
                    stripped_split_line = split_line.strip()
                
                    if stripped_split_line != '':
                        
                        command = int(stripped_split_line, 2)
                        program.append(command)
                    
                for command in program:
                     self.ram[address] = command
                     address +=1
   
        except FileNotFoundError:
               print(f'Your file {sys.argv[1]} could not be found in {sys.argv[0]}')
        
                                       

            

                          


       

# For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif  op == MUL:
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
        while self.running:

             ir = self.ram_read(self.pc)
             operand_a = self.ram_read(self.pc + 1)
             operand_b = self.ram_read(self.pc + 2)
             self.execute_command(ir, operand_a, operand_b)

             
               
    def execute_command(self, command, operand_a, operand_b):
        #0b10100010
        #Meanings of the bits in the first byte of each instruction: `AABCDDDD`

        #* `AA` Number of operands for this opcode, 0-2
        #* `B` 1 if this is an ALU operation
        #* `C` 1 if this instruction sets the PC
        #* `DDDD` Instruction identifier

        alu_command = command >> 5 & 0b1



        if command ==  HLT:
                self.running = False
                self.pc += 1

        if  command == PRN:
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])
                self.pc += 2

        if command == LDI:

                self.reg[operand_a] = operand_b
                self.pc += 3

       
                # must incremnt 
        if alu_command:
               
                 self.alu(command, operand_a, operand_b) 
                 self.pc += 3
                

    
        
