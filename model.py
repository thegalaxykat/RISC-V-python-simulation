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

    @property
    @abstractmethod
    def get_pc(self):
        return None

    @property
    @abstractmethod
    def get_registers(self):
        return None

    @abstractmethod
    def do_clock(self):
        pass

    @abstractmethod
    def do_reset(self):
        pass

IMM_DICT = {
    BitArray('0b0000011',length=7).bin:[*range(-32,-20)], #   L                                 works
    BitArray('0b0010011',length=7).bin:[*range(-32,-20)], #   i                                 works
    BitArray('0b0100011',length=7).bin:[*range(-32,-25),*range(-12,-7)], #   s                   
    BitArray('0b0110011',length=7).bin:[], #none   r                                            
    BitArray('0b1100011',length=7).bin:[-32,-8,*range(-31,-25),*range(-12,-8),None], #   b            
    BitArray('0b1100111',length=7).bin:[*range(-32,-20)], #   jalr                                works
    BitArray('0b1101111',length=7).bin:[-32,*range(-20,-12),-21,*range(-31,-21),None], #   jal  
    #BitArray(0b0110111):[self.] #   lui
    #BitArray(0b0010111):[self.] #   aui
}

FUNCT3_BEQ  = BitArray('0b000',length=3)
FUNCT3_BNE  = BitArray('0b001',length=3)
FUNCT3_BLT  = BitArray('0b100',length=3)
FUNCT3_BGE  = BitArray('0b101',length=3)
FUNCT3_BLTU = BitArray('0b110',length=3)
FUNCT3_BGEU = BitArray('0b111',length=3)




class MVP_Model(Model):
    def __init__(self,register_file) -> None:
        self._register_file = register_file
        self._controller=None
        self._pc = None
        self.OP_DICT ={
            BitArray('0b0000011',length=7).bin:[self.memory_address,self.memory_read,self.memory_write_back], #   L
            BitArray('0b0010011',length=7).bin:[self.execute_i,self.alu_writeback], #   i
            BitArray('0b0100011',length=7).bin:[self.memory_address,self.memory_write], #   s
            BitArray('0b0110011',length=7).bin:[self.execute_r,self.alu_writeback], #   r
            BitArray('0b1100011',length=7).bin:[self.branch], #   b
            BitArray('0b1100111',length=7).bin:[self.jump_and_link_register,self.alu_writeback], #   jalr
            BitArray('0b1101111',length=7).bin:[self.jump_and_link,self.alu_writeback], #   jal
            #BitArray(0b0110111,length=32):[self.] #   lui
            #BitArray(0b0010111,length=32):[self.] #   aui
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
        self._pc = BitArray('0x00000000',length=32)
        #self._register_file.do_reset()
        pass

    def do_clock(self):
        #fetch
        instruction = self._controller.get_instruct_mem(self._pc.int)
        if instruction is None:
            return
        self._next_pc = BitArray(int = self._pc.uint + 4,length=32)

        #decode
        op = instruction[-7:]
        self.current_op = op
        self.current_instruction = instruction
        self.rd = self.current_instruction[-12:-7]
        self.rs1_addr = instruction[-20:-15]
        self.rs2_addr = instruction[-25:-20]
        #rest of states
        memory = instruction

        for func in self.OP_DICT[op.bin]:
            memory = func(memory)
        self._pc=self._next_pc
    
    def clock_string(self):
        pass

    def get_imm(self,instruction):
        order = IMM_DICT[self.current_op.bin]
        imm = [instruction[index] if index is not None else False for index in order]
        b = BitArray(imm).int
        return BitArray(int=b,length=32)

    def memory_address(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[-20:-15]
        rs1 = self._register_file.get_data(rs1_addr)
        addr = rs1+imm
        return addr # goes to memory write/read

    def memory_read(self,addr):
        out = self._controller.get_data_mem(addr.uint)
        return out

    def memory_write_back(self,data):
        rd = self.current_instruction[-12:-7]
        self._register_file.set_data(rd,data)
        return None

    def memory_write(self,addr):
        rs2_addr = self.current_instruction[-25:-20]
        rs2 = self._register_file.get_data(rs2_addr)
        self._controller.set_data_mem(addr.uint,rs2)
        return None

    def execute_i(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[-20:-15]
        rs1 = self._register_file.get_data(rs1_addr)
        code = instruction[-15:-11] # workaround for some weird issues
        if code.startswith('0b101') :
            code[3] = instruction[-31]
        else:
            code[3] = False
        return self._alu.calculate(code,rs1,imm)

    def execute_r(self,instruction):
        rs1_addr = instruction[-20:-15]
        rs1 = self._register_file.get_data(rs1_addr)
        rs2_addr = instruction[-25:-20]
        rs2 = self._register_file.get_data(rs2_addr)
        code = instruction[-15:-11]
        code[3] = instruction[-31]
        return self._alu.calculate(code,rs1,rs2)

    def branch(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[-20:-15]
        rs1 = self._register_file.get_data(rs1_addr)
        rs2_addr = instruction[-25:-20]
        rs2 = self._register_file.get_data(rs2_addr)
        branch = False
        bcode = instruction[-15:-12]
        match bcode.bin:
            case FUNCT3_BEQ.bin:
                branch = rs1 == rs2
            case FUNCT3_BNE.bin:
                branch = rs1 != rs2
            case FUNCT3_BGE.bin:
                branch = rs1.int>=rs2.int
            case FUNCT3_BGEU.bin:
                a = rs1.uint
                b = rs2.uint
                branch = a>=b
            case FUNCT3_BLT.bin:
                branch = rs1.int<rs2.int
            case FUNCT3_BLTU.bin:
                a = rs1.uint
                b = rs2.uint
                branch = a<b
        if branch:
            self._next_pc = BitArray(int = self._pc.int+imm.int,length=32)
        return None

    def jump_and_link_register(self,instruction):
        imm = self.get_imm(instruction)
        rs1_addr = instruction[-20:-15]
        rs1 = self._register_file.get_data(rs1_addr)
        self._next_pc = BitArray(imm.int+rs1,length=32)
        return BitArray(int = self._pc.uint + 4,length=32)

    def alu_writeback(self,data):
        rd = self.current_instruction[-12:-7]
        self._register_file.set_data(rd,data)
        return None


    def jump_and_link(self,instruction):
        imm = self.get_imm(instruction)
        self._next_pc = BitArray(int=imm.int+self._pc.int,length=32)
        #print(self._next_pc)
        return BitArray(int = self._pc.uint + 4,length=32)

    class ALU():

        def __init__(self) -> None:
            pass
            self.alu_code_dict = {
                '0000':self.add,
                '0001':self.sub,
                '0010':self.sll,
                '0100':self.slt,
                '0110':self.sltu,
                '1000':self._xor,
                '1010':self.srl,
                '1011':self.sra,
                '1100':self._or,
                '1110':self._and,
            }

        def calculate(self,code,a,b):
            return(self.alu_code_dict[code.bin](a,b))


        def add(self,a,b):
            try:
                a = a.int
            except AttributeError:
                None
            try:
                b = b.int
            except AttributeError:
                None
            return BitArray(int=a+b,length=32)

        def sub(self,a,b):
            try:
                a = a.int
            except AttributeError:
                None
            try:
                b = b.int
            except AttributeError:
                None
            return BitArray(int= a-b,length=32)

        def slt(self,a,b):
            try:
                a = a.int
            except AttributeError:
                None
            try:
                b = b.int
            except AttributeError:
                None
            return BitArray(int=a<b,length=32)
        
        def sltu(self,a,b):
            try:
                a = a.uint
            except AttributeError:
                None
            try:
                b = b.uint
            except AttributeError:
                None
            return BitArray(int=a<b,length=32)

        def _or(self,a,b):
            return a | b

        def _and(self,a,b):
            return a & b
        
        def _xor(self,a,b):
            return a ^ b
        
        def sll(self,a,b):
            try:
                a = a.uint
            except AttributeError:
                None
            try:
                b = b.uint
            except AttributeError:
                None
            return BitArray(int=a<<b,length=32)

        def srl(self,a,b):
            try:
                a = a.uint
            except AttributeError:
                None
            try:
                b = b.uint
            except AttributeError:
                None
            return BitArray(int=a>>(b),length=32)

        def sra(self,a,b):
            return BitArray(int=a.int//b.uint,length=32)
