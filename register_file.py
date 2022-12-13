"""
RISC-V register file implementation.
"""
from registers import Register

# def _register_names():
#     reg_index = ["x00","x01","x02","x03","x04","x05","x06","x07","x08","x09","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
#     reg_names = ["zero", "ra", "sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6"]

class RegisterFile:
    """
    Register file implementation containing 32 instances of registers
    following RISC-V guidelines.

    Attributes:
    a1: A 5-bit integer representing a signal choosing address 1.
    a2: A 5-bit integer representing a signal choosing address 2.
    a3: A 5-bit integer representing a signal choosing address 3.
    rs1: A 32-bit integer representing the data in register at a1.
    rs2: A 32-bit integer representing the data in register at a2.
    wd: A 32-bit integer representing data to be written to the register
        at a3.
    we: A boolean that allows the data at the wd port to be written to
        the register at a3. 
    _regfile: A list of register instances.
    """

    def __init__(self):
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.rs1 = None
        self.rs2 = None
        self.wd = None
        self.we = False
        self.regfile = []
        self.modified_regs = []
        self.fullreg = False
        self.generate_registers()

    def generate_registers(self):
        """
        Instantiate all 32 registers found in the register file.
        """
        for i in range(32):
            if ( i == 0 ):
                self.regfile.append(Register(i, 0))
            else:
                self.regfile.append(Register(i))
    
    def read_registers(self, a1, a2):
        """
        Read the registers on a1 and a2.
        """
        for j in self.regfile:
            if (j == a1):
                self.rs1 = self.regfile[j].data()
            if (j == a2):
                self.rs2 = self.regfile[j].data()
        return (self.rs1, self.rs2)

    def write_to_register(self, a3, wd):
        """
        Write data in `wd` to the register on a3.
        """
        for k in self.regfile:
            if(k == a3):
                self.regfile[k].write_data(wd)
                if (len(self.modified_regs) == 0): 
                    self.modified_regs.append(k)
                else:
                    for m in len(self.modified_regs):
                        if(k == self.modified_regs[m]):
                            break
                    self.modified_regs.append(k)

    def switch_display():
        """
        Method to switch between full register-file print out and
        the non empty 
        """
    def get_data(self,addr):
        return self.regfile[int(addr)].data

    def set_data(self,addr,data):
        return self.regfile[int(addr)].write_data(data)
    
    def __repr__(self):
        """
        Return a string representing the data in the register
        """
        reg_index = ["x00","x01","x02","x03","x04","x05","x06","x07","x08","x09","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
        reg_names = ["zero", "ra", "sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6"]

        title = "+----Register File----+"
        end_line = "+---------------------+"
        lines = [title]

        if (self.fullreg == True):
            for l in range(32):
                data = self.regfile[l].data()
                if (data is None):
                    data = "xxxxxxxx"
                if (len(reg_names[l]) == 4):
                    reg_line = f"|{reg_index[l]} | {reg_names[l]} | {data}|"
                    lines.append(reg_line)
                if (len(reg_names[l]) == 3):
                    reg_line = f"|{reg_index[l]} | {reg_names[l]}  | {data}|"
                    lines.append(reg_line)
                if (len(reg_names[l]) == 2):
                    reg_line = f"|{reg_index[l]} | {reg_names[l]}   | {data}|"
                    lines.append(reg_line)
            lines.append(end_line)
            return "\n".join(lines)
        else:
            sorted_list = self.modified_regs.sort()
            for n in sorted_list:
                reg_line = f"|{reg_index[n]} | {reg_names[n]} | {self.regfile[n].data()}|"
                lines.append(reg_line)
            lines.append(end_line)
            return "\n".join(lines)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o,RegisterFile):
            return self.regfile == __o.regfile
        return False