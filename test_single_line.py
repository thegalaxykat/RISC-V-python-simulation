
from controller import Controller, Prompt
from model import MVP_Model
from register_file import RegisterFile
import random
from bitstring import BitArray

possible_instructions = ['lw','addi','slli','slti','sltiu','xori','srli',
'srai','ori','andi','auipc','sw','add','sub','sll','slt','sltu','xor','srl',
'sra','or','and','lui']
reg_index = ["x00","x01","x02","x03","x04","x05","x06","x07","x08","x09","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
reg_names = ["zero", "ra", "sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","a7", "s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6"]
reg_sim = [0]*32

args_data = {
            'lw':'rd imm(rs1)',
            'addi':'rd rs1 imm',
            'slli':'rd rs1 imm',
            'slti':'rd rs1 imm',
            'sltiu':'rd rs1 imm',
            'xori':'rd rs1 imm',
            'srli':'rd rs1 imm',
            'srai':'rd rs1 imm',
            'ori':'rd rs1 imm',
            'andi':'rd rs1 imm',
            'auipc':'rd imm',
            'sw':'rs2 imm(rs1)',
            'add':'rd rs1 rs2',
            'sub':'rd rs1 rs2',
            'sll':'rd rs1 rs2',
            'slt':'rd rs1 rs2',
            'sltu':'rd rs1 rs2',
            'xor':'rd rs1 rs2',
            'srl':'rd rs1 rs2',
            'sra':'rd rs1 rs2',
            'or':'rd rs1 rs2',
            'and':'rd rs1 rs2',
            'lui':'rd imm'
        }
class PromptEmulation(Prompt):
    def __init__(self) -> None:
        self.data = False
    #    model = model
    #    self.controller = controller
    #    pass

    def get_instruction(self):
        self.check_prev_data()
        self.good_to_send = False
        while not self.good_to_send:
            pre_sent = {}
            pre_sent['intr'] = random.choice(possible_instructions)
            pre_sent['rs1'] = self.get_modified_reg()
            pre_sent['rs2'] = self.get_modified_reg()
            pre_sent['rd']  = random.randint(0,31)
            pre_sent['imm'] = random.randint(0,2047)
            self.good_to_send = True
            self.data = self.check_instruction(pre_sent)

        return self.make_instruction()

    def get_file(self):
        filename = input('Enter file name: ')
        return filename

    def make_instruction(self):
        args = args_data[self.data['intr']]
        data = self.data.copy()
        if 'rd' in data.keys():
            data['rd'] = 'x'+str(data['rd'])
        if 'rs1' in data.keys():
            data['rs1'] = 'x'+str(data['rs1'])
        if 'rs2' in data.keys():
            data['rs2'] = 'x'+str(data['rs2'])
        for key, val in data.items():
            #if key in args:
            args = args.replace(key, str(val))
        return (data['intr']+" " + args)
        

    def check_prev_data(self):
        if self.data:
            if 'rd' in self.data.keys():
                rd = self.data['rd']
                future = self.data['future']
                if isinstance(future,BitArray):
                    future = future.uint
                if not model.get_registers.get_data(BitArray(uint=rd,length=5)).uint == future:
                    #raise ValueError("wrong register value")
                    None
            if 'next pc' in self.data.keys():
                if not model.get_pc.uint == self.data['next pc']:
                    #raise ValueError("wrong pc value")
                    None
            if 'data mem addr' in self.data.keys():
                if not controller.get_data_mem(BitArray(int=self.data['data mem addr'],length=32).uint) == model.get_registers.get_data(BitArray(uint=self.data['rs2'],length=5)):
                    #raise ValueError("wrong data mem value")
                    None

    def get_modified_reg(self):
        reg_data = None
        while reg_data is None:
            r = random.randint(0,31)
            reg_data = model.get_registers.get_data(BitArray(uint=r,length=32))
        return r


    def check_instruction(self,data):
        match(data['intr']):
            case 'lui':
                return self.check_lui(data)
            case 'lw':
                return self.check_lw(data)
            case 'addi'|'slli'|'slti'|'sltiu'|'xori'|'srli'|'srai'|'ori'|'andi'|'add'|'sub'|'sll'|'slt'|'sltu'|'xor'|'srl'|'sra'|'or'|'and':
                return self.check_ir(data)
            case 'auipc':
                return self.check_auipc(data)
            case 'sw':
                return self.check_sw(data)
            case _:
                None


    def check_lui(self,data):
        out = data
        out['future'] = out['imm']*4096
        out['next pc'] = model.get_pc.uint + 4 
        return out

    def check_lw(self,data):
        out = data
        if len(controller.data_memory.keys())<1:
            self.good_to_send = False
            return
        out['imm'] = random.choice(list(controller.data_memory.keys()))-model.get_registers.get_data(BitArray(uint=data['rs1'],length=5)).uint
        out['future'] = controller.get_data_mem(out['imm'])
        out['next pc'] = model.get_pc.uint + 4 
        return out

    def check_ir(self,data):
        out = data
        a = model.get_registers.get_data(BitArray(uint=data['rs1'],length=5))
        b = model.get_registers.get_data(BitArray(uint=data['rs2'],length=5))
        intr = data['intr']
        if 'i' in intr:
            b = BitArray(int=data['imm'],length =32)
            intr= intr.replace('i','')
        match intr:
            case 'add':
                out['future'] = BitArray(int=a.int+b.int,length=32)
            case 'sub':
                out['future'] = BitArray(int=a.int-b.int,length=32)
            case 'sll':
                out['future'] = a<<(b.uint)
            case 'slt':
                out['future'] = BitArray(int=a.int<b.int,length=32)
            case 'sltu':
                out['future'] = BitArray(int=a.uint<b.uint,length=32)
            case 'xor':
                out['future'] = a^b
            case 'srl':
                out['future'] = a>>(b.uint)
            case 'sra':
                out['future'] = BitArray(int=a.int//(2^b.uint),length=32)
            case 'or':
                out['future'] = a|b
            case 'and':
                out['future'] = a&b
        out['next pc'] = model.get_pc.uint + 4
        return out

    def check_auipc(self,data):
        out = data
        out['future'] = model.get_pc.uint +(BitArray(uint=out['imm'],length=32)<<12).uint
        out['next pc'] = model.get_pc.uint + 4 
        return out

    def check_sw(self,data):
        out = data
        a = BitArray(uint=out['rs1'],length=5)
        b = model.get_registers.get_data(a)
        out['imm'] = ((out['imm']+b).uint %4)-out['imm']
        out['data mem addr'] = out['imm']+model.get_registers.get_data(BitArray(uint=out['rs1'],length=5)).uint
        out['future'] = model.get_registers.get_data(BitArray(uint=out['rs2'],length=5))
        out['next pc'] = model.get_pc.uint + 4 
        del out['rd']
        return out






prompt = PromptEmulation()
model = MVP_Model(register_file=RegisterFile())
controller = Controller(model,view=None)
controller.prompt = prompt


def test_single_line():
    controller.run()


if __name__ == '__main__':
    test_single_line()

