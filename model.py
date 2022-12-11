from abc import ABC,abstractmethod

class Model(ABC):

    def __init__(self,register_file) -> None:
        self._register_file = register_file
        self._controller=None

    
    def set_controller(self,controller):
        """sets he controller of the memory"""
        self._controller = controller

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    @property
    def get_pc(self):
        pass

    @abstractmethod
    @property
    def get_registers(self):
        pass

    @abstractmethod
    def do_clock(self):
        pass

    @abstractmethod
    def do_rst(self):
        pass

class MVP_Model(Model):
    def __init__(self,register_file) -> None:
        super.__init__(self,register_file)
        self._pc = None

    def __repr__(self):
        return f"the current pc is {self._pc}\n"+self._register_file.__repr__()

    @property
    def get_pc(self):
        return self._pc

    @property
    def get_registers(self):
        return self._register_file

    def do_clock(self):
        pass
    
    def do_reset(self):
        #self._pc TODO make me
        self._pc = 0
        self._register_file.do_reset
        pass