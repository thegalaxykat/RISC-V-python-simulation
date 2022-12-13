"""
RISC-V Single Cycle CPU
"""
from abc import ABC, abstractmethod


class CPUView(ABC):
    """
    The CPU abstracted class representing the display of a CPU running
    an instruction.
    """

    def __init__(self, cpu):
        """
        Initializes the CPU view, which takes an instance of the CPU
        as a parameter and stores int as a private instance attribute.
        """
        self._cpu = cpu

    @property
    def cpu(self):
        """
        Returns the cpu register file stored in the cpu instance.
        """
        return self._cpu

    @abstractmethod
    def draw(self):
        """
        A draw method that is an abstract method.
        """


class TextView(CPUView):
    """
    The CPU text-based view. Takes place of the abstracted view class.
    """

    def draw(self):
        """
        Prints the CPUs state. Specifically it will print out the non
        xxxxxxxx registers. If verbose, will print out the entire
        register file.
        """
        print(self.cpu)
        print(f"Please enter a new instruction")