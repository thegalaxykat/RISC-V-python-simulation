from abc import ABC,abstractmethod

import bitstring

bitstring.lsb0 = True
BitArray = bitstring.BitArray

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

IMM_DICT = {
    BitArray(0b0000011):[*range(20,32)], #   L
    BitArray(0b0010011):[*range(20,32)], #   i
    #BitArray(0b0010111):[self.] #   aui
    BitArray(0b0100011):[*range(7,12),*range(25,32)], #   s
    BitArray(0b0110011):[None], #none   r
    #BitArray(0b0110111):[self.] #   lui
    BitArray(0b1100011):[None,*range(8,12),*range(25,31),7,31], #   b
    BitArray(0b1100111):[*range(20,32)], #   jalr
    BitArray(0b1101111):[None,*range(25,31),24,*range(12,24),31], #   jal
}

FUNCT3_BEQ  = BitArray(0b000)
FUNCT3_BNE  = BitArray(0b001)
FUNCT3_BLT  = BitArray(0b100)
FUNCT3_BGE  = BitArray(0b101)
FUNCT3_BLTU = BitArray(0b110)
FUNCT3_BGEU = BitArray(0b111)


class MVP_Model(Model):
    def __init__(self,register_file) -> None:
        super.__init__(self,register_file)
        self._pc = None
        self.OP_DICT ={
            BitArray(0b0000011):[self.memory_address,self.memory_read,self.memory_write_back], #   L
            BitArray(0b0010011):[self.execute_i,self.alu_writeback], #   i
            #BitArray(0b0010111):[self.] #   aui
            BitArray(0b0100011):[self.memory_address,self.memory_write], #   s
            BitArray(0b0110011):[self.execute_r,self.alu_writeback], #   r
            #BitArray(0b0110111):[self.] #   lui
            BitArray(0b1100011):[self.branch], #   b
            BitArray(0b1100111):[self.jump_and_link_register,self.alu_writeback], #   jalr
            BitArray(0b1101111):[self.jump_and_link,self.alu_writeback], #   jal
        }
        self._alu = self.ALU()

    def __repr__(self):
        return f"the current pc is {self._pc}\n"+self._register_file.__repr__()

    @property
    def get_pc(self):
        return self._pc

    @property
    def get_registers(self):
        return self._register_file
    
    def do_reset(self):
        self._pc = BitArray(0x00000000)
        #self._register_file.do_reset()
        pass

    def do_clock(self):
        #fetch
        instruction = self._controller.get_instruct_mem(int(self._pc))
        self._next_pc = self._pc + BitArray(int=4)

        #decode
        op = instruction[6:0]
        self.current_op = op
        self.current_instruction = instruction
        #rest of states
        memory = instruction
        for func in self.OP_DICT[op]:
            memory = func(memory)
        pass

    def get_imm(self,instruction):
        op = instruction[6:0]
        order = IMM_DICT[op]
        imm = [instruction[index] for index in order]
        return imm

    def memory_address(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[19:15]
        rs1 = self._register_file.data(rs1_addr)
        addr = rs1+imm
        return addr # goes to memory write/read

    def memory_read(self,addr):
        out = self._controller.get_data_mem(addr)
        return out

    def memory_write_back(self,data):
        rd = self.current_instruction[7:11]
        self._register_file.write_data(rd,data)
        return None

    def memory_write(self,addr):
        rs2_addr = self.current_instruction[24:20]
        rs2 = self._register_file.data(rs2_addr)
        self._controller.set_data_mem(addr,rs2)
        return None

    def execute_i(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[19:15]
        rs1 = self._register_file.data(rs1_addr)
        code = instruction[12:14]+instruction[30]
        return self._alu(code,rs1,imm)

    def execute_r(self,instruction):
        rs1_addr = instruction[19:15]
        rs1 = self._register_file.data(rs1_addr)
        rs2_addr = instruction[24:20]
        rs2 = self._register_file.data(rs2_addr)
        code = instruction[12:15]+instruction[30]
        return self._alu(code,rs1,rs2)

    def branch(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[19:15]
        rs1 = self._register_file.data(rs1_addr)
        rs2_addr = instruction[24:20]
        rs2 = self._register_file.data(rs2_addr)
        branch = False
        match(instruction[12:14]):
            case[FUNCT3_BEQ]:
                branch = rs1 is rs2
            case[FUNCT3_BGE]:
                branch = rs1.int>=rs2.int
            case[FUNCT3_BGEU]:
                branch = rs1.uint>=rs2.unit
            case[FUNCT3_BLT]:
                branch = rs1.int<rs2.int
            case[FUNCT3_BLTU]:
                branch = rs1.uint<rs2.uint
        if branch:
            self._next_pc = self._pc+imm
        return None

    def jump_and_link_register(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[19:15]
        rs1 = self._register_file.data(rs1_addr)
        self._next_pc = BitArray(imm.int+rs1,length=32)
        return self._pc + 4

    def alu_writeback(self,data):
        rd = self.current_instruction[7:11]
        self._register_file.write_data(rd,data)
        return None


    def jump_and_link(self,instruction):
        imm = self.get_imm(instruction)
        self._next_pc = BitArray(imm.int+self._pc,length=32)
        return 

    class ALU():

        def __init__(self) -> None:
            pass
            self.alu_code_dict = {
                BitArray('0b0000'):self.add,
                BitArray('0b0001'):self.sub,
                BitArray('0b0010'):self.sll,
                BitArray('0b0100'):self.slt,
                BitArray('0b0110'):self.sltu,
                BitArray('0b1000'):self._xor,
                BitArray('0b1010'):self.srl,
                BitArray('0b1011'):self.sra,
                BitArray('0b1100'):self._or,
                BitArray('0b1110'):self._and,
            }

        def calculate(self,code,a,b):
            return(self.alu_code_dict[code](a,b))


        def add(self,a,b):
            return BitArray(int=int(a)+int(b),length=32)

        def sub(self,a,b):
            return BitArray(int=int(a)-int(b),length=32)

        def slt(self,a,b):
            return BitArray(int=int(a)<int(b),length=32)
        
        def sltu(self,a,b):
            return BitArray(int=a.uint<b.uint,length=32)

        def _or(self,a,b):
            return a | b

        def _and(self,a,b):
            return a & b
        
        def _xor(self,a,b):
            return a ^ b
        
        def sll(self,a,b):
            return a.__lshift__(b.uint)

        def srl(self,a,b):
            return a.__rshift__(b.uint)

        def sra(self,a,b):
            return BitArray(int=a.int//b.uint,length=32)

        


BitArray()