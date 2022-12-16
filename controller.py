"""
Controller for the RISC-V simulator. Gets assembly from user and passes binary 
to the model to be executed. Stores instruction and data memory as dictionaries.
"""

import abc

import bitstring
from riscv_assembler.convert import AssemblyConverter as convertFile
#from riscv_assembler.tools import AssemblyTools as convertLine

from model import Model
from test_strings import memh_dict

# note that Convert works for whole files and Tools works for individual lines

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

        # line-by-line mode
        if filename == None:
            self.instruction_memory=memh_dict
            
            old_reg = None
            old_pc = None
            
            while not(self.model.get_registers == old_reg) or not (old_pc == self.model.get_pc):
                old_reg = self.model.get_registers
                old_pc = self.model.get_pc
                print(self.model.get_pc)
                self.model.do_clock()
                reg = self.model.get_registers
                reg.fullreg = False
                print(reg)
            print(self.model)


            # get PC from model

            # get instruction line from user

            # compile assembly to binary

            # send back to model at that PC

            # do_clock tells model to run
            pass


        # Assembly file mode
        else:
            # get assembly from file

            # compile assembly

            # create data and instruction memory

            # write instructions to instruction memory

            # run through each instruction
            
            # for instruction in instructions: self.model.do_clock()
            pass

        

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
            print(self.model)
            return None
            #raise Exception("Address does not exist in instruction memory")


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
# views
class Prompt(abc.ABC):
    """
    Abstract base class for prompts
    """

    @abc.abstractmethod
    def get_file(self):
        """
        Gets file from user
        """
        pass