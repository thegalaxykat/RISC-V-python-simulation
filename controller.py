"""
Controller for the RISC-V simulator. Gets assembly from user and passes binary 
to the model to be executed. Stores instruction and data memory as dictionaries.
"""
import os
from abc import ABC, abstractmethod

from assembler import AssemblyProgram
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
        self.prompt = PromptCLI
        # reset model
        self.model.do_reset()

        # create empty memory
        self.instruction_memory = {}
        self.data_memory = {}

        # conversion toolkit object for later
        self._at_end_of_mem = False

    def run(self, filename=None):
        """
        Gets assembly from user (either line-by-line instructions or from an
        .s file), compiles it to binary, writes to instruction memory, and
        runs the model.
        """
        self.ap = AssemblyProgram()
        # get PC from model (begins at 0)

        # line-by-line mode
        if filename == None:
            while 1:
                # get instruction line from user
                instruction = self.prompt.get_instruction()
                instruction.lower()
                instruction = instruction.replace(',', '')
                if 'stop' in instruction or 'escape' in instruction:
                    print(self.model)
                    return
                # compile assembly to binary (bitstring)
                binary = self.compile_line_instruct(instruction)
                # update instruction memory
                self.instruction_memory[self.model.get_pc.uint] = binary
                # do_clock tells model to run
                self.model.do_instruction()

        # Assembly *file* mode
        else:
            # compile assembly
            self.ap
            with open(os.path.join(os.path.curdir, filename), "r") as f:
                for line in f:
                    self.ap.parse_line(line)

            self.instruction_memory = self.ap.return_mem()

            # run through each instruction
            old_reg = None
            old_pc = None
            # (while PC not changing and register file not changing)
            while not (self.model.get_registers == old_reg) or \
                    not (old_pc == self.model.get_pc) and not self._at_end_of_mem:

                old_reg = self.model.get_registers
                old_pc = self.model.get_pc

                self.model.do_instruction()
                reg = self.model.get_registers
                reg.fullreg = False
            print(self.model.get_registers)

    def reg_number(self, reg):
        """
        Gets the register number from the register name.

        Args:
            reg (str): register name

        Returns:
            int: register number
        """
        reg = reg.lower()
        num_str = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15",
                   "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30", "x31"]
        name_str = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4",
                    "a5", "a6", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
        if reg in num_str:
            return "x{:02d}".format(num_str.index(reg))
        if reg in name_str:
            return "x{:02d}".format(name_str.index(reg))
        return reg

    def compile_line_instruct(self, instruct):
        """
        Compiles line of assembly to binary

        Args:
            instruct (str): line of assembly

        Returns:
            bitstring: binary instruction
        """
        # comma formatting (Avi's code requires them)
        instruct = instruct.replace(' ', ', ')
        instruct = instruct.replace(',,', ',')
        instruct = instruct.replace(', ', ' ', 1)
        # PC is stored in model (as bitArray)
        pc = self.model.get_pc.uint
        # parse line and return binary instruction
        line = self.ap.parse_line(instruct)
        return self.ap.return_line(line, pc)

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
            self._at_end_of_mem = True
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
    Gets assembly from user in CLI
    """

    def get_instruction():
        instruct = input('Enter instruction: ')
        # if branch or jump reject
        while instruct[0] == 'b' or instruct[0] == 'j':
            print("Only I Types, R Types, and S Types supported in \
                 line-by-line mode")
            instruct = PromptCLI.retry_instruction()
        return instruct

    def retry_instruction():
        instruct = input('Enter instruction: ')
        return instruct

    def get_file():
        filename = input('Enter file name: ')
        return filename


class PromptEmulation(Prompt):
    """
    Gets assembly from test
    """

    def __init__(self):
        self.possible_instructions = []

    def get_instruction():
        instruct = input('Enter instruction: ')
        # if branch or jump reject
        while instruct[0] == 'b' or instruct[0] == 'j':
            print("Only I Types, R Types, and S Types supported in \
                 line-by-line mode")
            instruct = PromptCLI.retry_instruction()
        return instruct

    def get_file():
        filename = input('Enter file name: ')
        return filename
