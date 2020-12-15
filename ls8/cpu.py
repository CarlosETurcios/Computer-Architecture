"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
ltf = 0b00000100
gtf = 0b00000010
etf = 0b00000001

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

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == SUB: 
            self.reg[reg_a] -= self.reg[reg_b]

        elif  op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == CMP:
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = ltf
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = gtf
            else:
                self.fl = etf
        else:
            raise Exception("Unsupported ALU operation")

        self.reg[reg_a] = self.reg[reg_a] & 0xFF
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
             # Ir == (Instruction Register) = value at memory address in PC (Program Counter)
             ir = self.ram_read(self.pc)
             print("instruction",ir)
             operand_a = self.ram_read(self.pc + 1)
             print("op_a:",operand_a)
             operand_b = self.ram_read(self.pc + 2)
             print("op_b:", operand_b)
             self.execute_command(ir, operand_a, operand_b)
            #  print("command", self.execute_command(ir,operand_a,operand_b))
             

             
               
    def execute_command(self, command, operand_a, operand_b):
        #0b10100010
        #Meanings of the bits in the first byte of each instruction: `AABCDDDD`

        #* `AA` Number of operands for this opcode, 0-2
        #* `B` 1 if this is an ALU operation
        #* `C` 1 if this instruction sets the PC
        #* `DDDD` Instruction identifier
        #   AABCDDDD
        #   01010000
        #   01010000

        alu_command = (command >> 5 & 0b001) == 1
        # print("hello", command,  0b001)
        num_operands = (command >> 6 & 0b11 ) + 1
        sets_pc_directly = (command >> 4 & 0b0001) == 1

        

      
      


        if  not sets_pc_directly:

            if command == LDI:

                    self.reg[operand_a] = operand_b

            elif  command == PRN:
                    
                    print("this is the result:", self.reg[operand_a])
                # must incremnt 

            elif command ==  HLT:
                      self.running = False    

            elif alu_command:
                        
                self.alu(command, operand_a, operand_b) 
            
            
            elif command == PUSH:
                # decrement the SP 
                ## start, the SP point to address 
            
            
                self.reg[7]  -= 1

                # copy the value fromm given register into address pointed to by SP
            
                register_address = self.ram[self.pc + 1]
                value = self.reg[register_address]
                # copy into SP address 
                #  copy this value in to our memory
                self.ram[self.reg[7]] = value
               
            elif command == POP:
                # Copy the value from the address pointed to by 'SP' to the given register
                ## get the SP
                
                ## copy the value from memory to that SP Adress
                value = self.ram_read(self.reg[7])

                # get the target register address
                register_address = self.ram_read(self.pc + 1)
                # put the value in the register 
                self.reg[register_address] = value

                # Increment the SP (move it back up )
                self.reg[7] += 1
                

            # elif command == CALL:
            #     # push the return address into the stack 
            #     ## find the address/index of the command AFTER call
            #     return_address = self.pc + 2 

            #     # push address into the stack 
            #     ## decrement the SP
            #     self.reg[7] -= 1

            #     self.ram[self.reg[7]] = return_address

            #     register_number = self.ram[self.pc + 1]

            #     address_to_jump_to = self.reg[register_number]

            #     self.pc = self.reg[address_to_jump_to]

            # elif command == RET:
            #     # pop from the top of stack
            #     # get the value first
            #     return_address = self.ram[self.reg[7]]
            #     # move the stack pointer back up 
            #     self.reg[7] += 1
            #     # jump back, and set the pc to this value 
            #     self.pc = return_address

            
            
           

          
                  

          
               
            
           

        
            self.pc += num_operands
        elif sets_pc_directly:

            if command == JEQ:
            # fl = 00000001
            #etf = 00000001#
            #  flag is set to <  
            # ltf = 00000100 
            # etf = 00000001
                print("this is fl", self.fl)
                if self.fl == etf:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += num_operands 

            elif command == JNE:
                if  self.fl != etf:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += num_operands

            elif command == JMP:
                self.pc = self.reg[operand_a]
            


        else:
            print(f"Invalid instruction {self.ir} at address {self.pc}")
            sys.exit(1)
                
           
  



 


    
        
