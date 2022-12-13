"""
RISC-V Register File Implementation
"""
class Register:
    """
    Register class that stores its address, name, and data.
    
    Attributes:
        address: An integer representing the regirster's address.
        data: A 32-bit integer holding the data stored in the register.
    """

    def __init__(self, address, data=None):
        """
        Create the register
        """
        self._address = address
        self._data = data
    
    @property
    def address(self):
        """
        Return the register's address.
        """
        return self._address

    @property
    def data(self):
        """
        Return the register's data.
        """
        return self._data

    def write_data(self, new_data):
        """
        Write data to the register.

        Args:
            new_data: A 32 bit integer that 
        """
        self._data = new_data

    def __repr__(self):
        """
        Return a string representing the data in the register.
        """
        data_string = str(self._data)
        return data_string
    
    def __eq__(self,__o):
        if isinstance(__o,Register):
            return self._data == __o._data & self._address == __o._address
        return False

