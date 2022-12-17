"""
Controller for the RISC-V simulator. Gets assembly from user and passes binary 
to the model to be executed. Stores instruction and data memory as dictionaries.
"""

from abc import ABC, abstractmethod

import bitstring
# note that Convert works for whole files and Tools works for individual lines
from riscv_assembler.convert import AssemblyConverter
from riscv_assembler.utils import *

from model import Model


class Controller:
    """
    Gets Assembly and passes the binary instructions to instruction memory.
    """
    
    def __init__(self, model: Model, view):
        """
        Initializes controller with model and view and creates empty memory
        """
        model.set_controller(self)
        self.model = model
        self.view = view

        # reset model
        self.model.do_reset()

        # create empty memory
        self.instruction_memory = {}
        self.data_memory = {}
        

    def run(self, filename=None):
        """
        Gets assembly from user (either line-by-line instructions or from an
        .s file), compiles it to binary, writes to instruction memory, and
        runs the model.
        """

        # get PC from model (begins at 0)
        pc = self.model.get_pc

        # line-by-line mode
        if filename == None:
            # get PC from model
            pc = self.model.get_pc
            # get instruction line from user
            instruction = PromptCLI.get_instruction()
            instruction.lower()
            instruction = instruction.replace(',','')
            # compile assembly to binary (bitstring)
            tk = Toolkit()
            binary = self.compile_line_instruct(instruction)
            # update instruction memory
            self.set_instruct_mem(pc, binary)
            # do_clock tells model to run
            self.model.do_clock()


        # Assembly *file* mode
        else:
            # compile assembly
            cnv = AssemblyConverter(output_type="t", nibble=False)
            cnv.convert('/binary/instructions.txt')

            # for each line (instruction) in file add to instruction memory
            with open('/binary/instructions.txt', 'r') as f:
                for line in f:
                    # str to bitstring
                    instruction = bitstring.BitArray(bin=line)
                    # add to instruction memory at pc (dictionary of bit arrays)
                    self.instruction_memory[pc] = instruction
                    # finally, for next instruction, increment PC by 4
                    pc += 4

            # run through each instruction
            old_reg = None
            old_pc = None
            # (while PC not changing and register file not changing)
            while not(self.model.get_registers == old_reg) or \
            not (old_pc == self.model.get_pc):
                
                old_reg = self.model.get_registers
                old_pc = self.model.get_pc

                self.model.do_clock()
                reg = self.model.get_registers
                reg.fullreg = False


    def compile_line_instruct(self, instruct):
        """
        Compiles line of assembly to binary but first must determine the
        instruction type to use the correct function from the toolkit.

        Args:
            instruct (str): line of assembly

        Returns:
            bitstring: binary instruction
        """
        # R type instruct
        r_types = ['add','sub','sll','slt','sltu','xor','srl','sra','or','and']
        # I type instruct
        i_types_op3 = ['lb','lh','lw','lbu','lhu']
        i_types_op19 = ['addi','slli','sltu','sltiu','xori','srli','srai',
                        'ori','andi']
        # S type instruct
        s_types = ['sb','sh','sw']

        # compile to binary with toolkit
        if instruct.split()[0] in r_types:
            operation = instruct.split()[0]
            rd = instruct.split()[1]
            rs1 = instruct.split()[2]
            rs2 = instruct.split()[3]
            # toolkit requires special format
            return tk.R_type(operation, rs1, rs2, rd)

        elif instruct.split()[0] in i_types_op3:
            operation = instruct.split()[0]
            rd = instruct.split()[1]
            imm = instruct.split()[2].split('(')[0]
            rs1 = instruct.split()[2].split('(')[1].replace(')','')
            # toolkit requires special format, again
            return tk.I_type(operation, rs1, imm, rd)

        elif instruct.split()[0] in i_types_op19:
            operation = instruct.split()[0]
            rd = instruct.split()[1]
            rs1 = instruct.split()[2]
            imm = instruct.split()[3]
            # toolkit requires special format
            return tk.I_type(operation, rs1, imm, rd)

        elif instruct.split()[0] in s_types:
            operation = instruct.split()[0]
            rs2 = instruct.split()[1]
            imm = instruct.split()[2].split('(')[0]
            rs1 = instruct.split()[2].split('(')[1].replace(')','')
            # toolkit still requires a special format
            return tk.S_type(operation, rs1, rs2, imm)


    def set_instruct_mem(self, address, instruction):
        """
        Sets instruction at address

        Args:
            address (int): address to set
            instruction (bitstring): instruction to set
        """
        self.instruction_memory[address] = instruction
            

    def get_instruct_mem(self, address):
        """
        Returns instruction at address

        Args:
            address (int): address to get
        """
        if address in self.instruction_memory:
            return self.instruction_memory[address]
        
        # throws error if trying to access mem that doesn't exist
        else:
            print("no more instruction mem")
            print(self.model) #TODO this will eventually be in view
            return None


    def get_data_mem(self, address):
        """
        Returns data at address
        Args:
            address (int): address to get
        """
        if address in self.data_memory:
            return self.data_memory[address]

        # throws error if trying to access mem that doesn't exist
        else:
            raise Exception("Address does not exist in data memory")
        

    def set_data_mem(self, address, data):
        """
        Sets data at address

        Args:
            address (int): address to set
            data (bitstring): data to set
        """
        try:
            self.data_memory[address] = data
        except: 
            raise Exception("Data could not be set in data memory")


# abstract base class for prompts since they may be different for different
# views in the future
class Prompt(ABC):
    """
    Abstract base class for prompts
    """

    @abstractmethod
    
    def get_instruction(self):
        """
        Gets instruction from user
        """
        pass
    
    def get_file(self):
        """
        Gets file from user
        """
        pass


class PromptCLI(Prompt):
    """
    Gets file from user in CLI
    """
    
    def get_instruction():
        instruct = input('Enter instruction: ')
        # if branch or jump reject 
        while instruct[0] == 'b' or instruct[0] == 'j':
            print("Only I Types, R Types, and S Types supported in \
                 line-by-line mode")
            instruct = PromptCLI.retry_instruction()
        return

    def retry_instruction():
        instruct = input('Enter instruction: ')
        return

    def get_file():
        filename = input('Enter file name: ')
        return filename