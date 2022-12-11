"""
Controller for the RISC-V simulator. Gets assembly from user and passes binary 
to the model to be executed. Stores instruction and data memory as dictionaries.
"""
from model import Model
import abc
from riscv_assembler.convert import AssemblyConverter as convertFile
from riscv_assembler.tools import AssemblyTools as convertLine
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
        
        # REVIEW should we initialize the memory with addresses
        # and 0s or leave it empty? Also: Are how are we storing the binary?
        # in a str?

    def run(self, filename=None):
        """
        Gets assembly from user (either line-by-line instructions or from an
        .s file), compiles it to binary, writes to instruction memory, and
        runs the model.
        """

        # line-by-line mode
        if filename == None:
            
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
        """
        # throws error if trying to access mem that doesn't exist


    def get_data_mem(self, address):
        """
        Returns data at address
        """
        # throws error if trying to access mem that doesn't exist

    def set_data_mem(self, address, data):
        """
        Sets data at address
        """


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