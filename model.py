from abc import ABC,abstractmethod

import bitstring
from bitstring import BitArray

#bitstring.lsb0 = True
#BitArray = bitstring.BitArray

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

# this for the imm types is a list
# the order of the list is msb0 
# None is a always 0 and an empy list is no imm at all
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

#this is the funct3 codes functions for the branch match case
FUNCT3_BEQ  = BitArray('0b000',length=3)
FUNCT3_BNE  = BitArray('0b001',length=3)
FUNCT3_BLT  = BitArray('0b100',length=3)
FUNCT3_BGE  = BitArray('0b101',length=3)
FUNCT3_BLTU = BitArray('0b110',length=3)
FUNCT3_BGEU = BitArray('0b111',length=3)




class MVP_Model(Model):
    def __init__(self,register_file) -> None:
        """inits the model with a register file"""
        self._register_file = register_file
        self._controller=None
        self._pc = None # the ps is set to none b/c it needs to be reset first like the real model
        self.OP_DICT ={ # this shows the track for every path through the fsm (this only stores after the decode state)
            BitArray('0b0000011',length=7).bin:'l type',#['MemAdr',self.memory_read,self.memory_write_back], #   L
            BitArray('0b0010011',length=7).bin:'i type',#[self.execute_i,self.alu_writeback], #   i
            BitArray('0b0100011',length=7).bin:'s type',#['MemAdr',self.memory_write], #   s
            BitArray('0b0110011',length=7).bin:'r type',#[self.execute_r,self.alu_writeback], #   r
            BitArray('0b1100011',length=7).bin:'b type',#[self.branch], #   b
            BitArray('0b1100111',length=7).bin:'jr type',#[self.jump_and_link_register,self.alu_writeback], #   jalr
            BitArray('0b1101111',length=7).bin:'jal type',#[self.jump_and_link,self.alu_writeback], #   jal
            #BitArray(0b0110111,length=32).bin:[self.] #   lui  unused
            #BitArray(0b0010111,length=32).bin:[self.] #   aui  unused
        }
        self._alu = self.ALU(self) # init alu class
        self._fsm_state = None
        self._PC_write = None
        self._result_slt = None
        self._alu_control = None
        

    def __repr__(self):
        return self._register_file.__repr__()

    @property
    def get_pc(self):
        return self._pc 

    @property
    def get_registers(self):
        return self._register_file
    
    def do_reset(self):
        self._fsm_state = 'Fetch'
        self._pc = BitArray('0x00000000',length=32) # resets the pc counter to 0
        self._data_mem_adr= BitArray('0x00000000',length=32)
        self._pc = BitArray('0x00000000',length=32)
        
        self._pc_old = BitArray('0x00000000',length=32)
        self._current_instruction = BitArray('0x00000000',length=32)
        
        
        self.rs1_data = BitArray('0x00000000',length=32)
        self.rs2_data = BitArray('0x00000000',length=32)
        self._alu_result_old = BitArray('0x00000000',length=32)
        pass

    def do_instruction(self):
        if(self._fsm_state == 'Fetch'):
            self.do_clock()
        while self._fsm_state != 'Fetch':
            if self.do_clock()<1:
                return
        pass

    def do_clock(self):
        """ run a clock cycle of the processor 
        inputs : none
        outputs : none"""
        print(self._fsm_state)
        if self._pc.int >= 0x0e4:
            None
        match(self._fsm_state):
            case 'Fetch':
                #fetch
                self._IR_write = True
                self._alu_a_slt = 'pc'
                self._alu_b_slt = 'four'
                self._alu_control = 'add'
                self.next_fsm_state = 'Decode'
                self._result_slt = 'alu_result'
                self._write_to_register=False
                self._addr_slt = False
                self._PC_write = True
                self._write_mem = False
            case 'Decode':
                #decode
                if self._current_instruction is None:# this is for the end of the loop where is there is no instruction
                    return 0
                self._IR_write = False
                self._PC_write = False
                op = self._current_instruction[-7:] # all the data is weirdly reserve indexed b/c of issues with the Bitarray lib
                self.current_op = op
                self._op_type = self.OP_DICT[op.bin]
                match(self._op_type):
                    case 'l type' | 's type':
                        self.next_fsm_state = 'MemAdr'
                    case 'i type':
                        self.next_fsm_state = 'Execute I'
                    case 'r type':
                        self.next_fsm_state = 'Execute R'
                    case 'b type':
                        self.next_fsm_state = 'Branch'
                        self._alu_a_slt = 'old pc'
                        self._alu_b_slt = 'imm'
                    case 'jr type':
                        self.next_fsm_state = 'Jump and link register'
                        self._alu_a_slt = 'rs1'
                        self._alu_b_slt = 'imm'
                        self._alu_control = 'add' #TODO FIX THE ISSUE WHERE WE DONT GET RSI QUICK INEOUGH FOR TJIS CYCLE AND WE GET IT NEXT CYCLE
                    case 'jal type':
                        self.next_fsm_state = 'Jump and link'
                        self._alu_a_slt = 'old pc'
                        self._alu_b_slt = 'imm'
                        self._alu_control = 'add'
                    case []:
                        None


        #rest of states
            case 'MemAdr':
                self._memory_address()
                if self._op_type == 'l type':
                    self.next_fsm_state = 'MemRead'
                else:
                    self.next_fsm_state = 'MemWrite'
            case 'MemRead':
                self.memory_read()
                self.next_fsm_state = 'MemWriteBack'
            case 'MemWriteBack':
                self.memory_write_back()
                self.next_fsm_state = 'Fetch'
            case 'MemWrite':
                self.memory_write()
                self.next_fsm_state = 'Fetch'
            case 'Execute I':
                self.execute_i()
                self.next_fsm_state = 'alu writeback'
            case 'Execute R':
                self.execute_r()
                self.next_fsm_state = 'alu writeback'
            case 'Jump and link register':
                self.jump_and_link_register()
                self.next_fsm_state = 'alu writeback'
            case 'Jump and link':
                self.jump_and_link()
                self.next_fsm_state = 'alu writeback'
            case 'alu writeback':
                self._PC_write = False
                self.alu_writeback()
                self.next_fsm_state = 'Fetch'
            case 'Branch':
                self.branch()
                self.next_fsm_state = 'Fetch'
            
        
        if self._write_mem:
            self._controller.set_data_mem((self._addr).uint,self.rs2_data)
        #the reason we need 2 steps here is b/c python is serial and real logic is parallel
        if self._pc.int > 0x0e4:
            None
        #registers data collection
        _result = self._result
        _pc = self._pc
        _data_addr = self._addr 
        instruction = self._controller.get_instruct_mem((self._addr).uint)

        self.rs1_addr = self._current_instruction[-20:-15]
        self.rs2_addr = self._current_instruction[-25:-20]
        rs1 = self._register_file.get_data(self.rs1_addr)
        rs2 = self._register_file.get_data(self.rs2_addr)
        alu_result = self._alu_result 


        #register data storage
        self._data_mem_adr= _data_addr

        if self._write_to_register:
            self._register_file.set_data(self.rd,_result)
        if self._PC_write:
            self._pc = _result
        
        if self._IR_write:
            self._pc_old = _pc
            self._current_instruction = instruction
        
        
        self.rs1_data = rs1
        self.rs2_data = rs2
        self._alu_result_old = alu_result
        self._fsm_state = self.next_fsm_state
        return 1 # flag for good
    #work around for only calling data me when its needed so as not to raise an error
    @property
    def _memory_result(self):
        return self._controller.get_data_mem(self._data_mem_adr.uint)

    @property
    def rd(self):
        return self._current_instruction[-12:-7]
    
    ######################## alu ########################
    @property
    def _alu_result(self):
        if self._alu_a == None or self._alu_b == None:
            None
        return self._alu.calculate(self._alu_control,self._alu_a,self._alu_b)

    ####################### muxes #######################
    @property
    def _result(self):
        match(self._result_slt):
            case 'alu_result_old':
                return self._alu_result_old
            case 'alu_result':
                return self._alu_result
            case 'memory_result':
                return self._memory_result
        return None
    
    @property
    def _alu_a(self):
        match(self._alu_a_slt):
            case 'pc':
                return self._pc
            case 'old pc':
                return self._pc_old
            case 'rs1':
                return self.rs1_data
        return None

    @property
    def _alu_b(self):
        match(self._alu_b_slt):
            case 'imm'|'immediate':
                return self._imm
            case 'four'|'4'|4:
                return BitArray(int=4, length=32)
            case 'rs2':
                return self.rs2_data
        return None
    
    @property
    def _addr(self):
        if self._addr_slt:
            return self._result
        return self._pc
    

    def clock_string(self):
        pass


    def wire_states(self):
        """returns the states of the names wires in dict"""
        out = {
            "PC":self._pc
        }

    @property
    def _imm(self): # return the imm of the current instruction
        order = IMM_DICT[self.current_op.bin] # get order of bits  and iter though bits
        imm = [self._current_instruction[index] if index is not None else False for index in order]
        b = BitArray(imm).int # make it signed
        return BitArray(int=b,length=32) # and extend it to 32 bits

    def _get_imm(self,instruction): # return the imm of the current instruction
        order = IMM_DICT[self.current_op.bin] # get order of bits  and iter though bits
        imm = [instruction[index] if index is not None else False for index in order]
        b = BitArray(imm).int # make it signed
        return BitArray(int=b,length=32) # and extend it to 32 bits

    @property
    def instuction(self):
        return self._current_instruction 

    def _memory_address(self):
        self._alu_control = 'add'
        self._alu_a_slt = 'rs1'
        self._alu_b_slt = 'imm'
        pass


    def memory_read(self):# just grab the data nothing more
        self._result_slt = 'alu_result_old'
        self._addr_slt = True
        return None

    def memory_write_back(self): # take data and write it back to the register
        self._result_slt = 'memory_result'
        self._write_to_register = True
        return None

    def memory_write(self):# write data to data memory
        self._result_slt = 'alu_result_old'
        self._addr_slt = True
        self._write_mem = True
        return None

    def execute_i(self):
        self._alu_a_slt = 'rs1'
        self._alu_b_slt = 'imm'
        code = self._current_instruction[-15:-11] # workaround for some weird issues
        if code.startswith('0b101') : # if its the only i type that has cares about the bit in fucnt7
            code[3] = self._current_instruction[-31] #use the bit then
        else:
            code[3] = False # ignore the bit
        self._alu_control = code.bin
        pass

    def execute_r(self):
        self._alu_a_slt = 'rs1'
        self._alu_b_slt = 'rs2'
        code = self._current_instruction[-15:-11]
        code[3] = self._current_instruction[-31] # always use the bit
        self._alu_control = code.bin
        pass

    def branch(self):
        rs1 = self.rs1_data
        rs2 = self.rs2_data
        branch = False
        bcode = self._current_instruction[-15:-12] 
        match bcode.bin: #sort by branch code (sadly not using alu)
            case FUNCT3_BEQ.bin:
                branch = rs1 == rs2 # this is if the branch will return
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
        if branch: # and do the branch
            self._PC_write = True
            self._result_slt = "alu_result_old"
        return None

    def jump_and_link_register(self):
        self._PC_write = True
        self._result_slt = "alu_result"
        self._alu_a_slt = "old pc"
        self._alu_b_slt = "4"
        self._alu_control = 'add'
        return None

    def alu_writeback(self): # write the data from the alu
        self._result_slt = "alu_result_old"
        self._write_to_register=True
        return None


    def jump_and_link(self):
        self._PC_write = True
        self._result_slt = "alu_result_old"
        self._alu_a_slt = "old pc"
        self._alu_b_slt = "4"
        self._alu_control = 'add'
        pass

    class ALU():

        def __init__(self,inputs) -> None:
            self.alu_code_dict = { #make list of control codes and what func they should do
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
                'add':self.add,
                'sub':self.sub,
                'sll':self.sll,
                'slt':self.slt,
                'sltu':self.sltu,
                'xor':self._xor,
                'srl':self.srl,
                'sra':self.sra,
                'or':self._or,
                'and':self._and,
            }

        def calculate(self,code,a,b): # and run the code from that list
            return(self.alu_code_dict[code](a,b))

        #below are the functions the codes run
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
