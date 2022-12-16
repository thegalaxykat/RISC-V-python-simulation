# documentation at https://www.riscvassembler.org/toolkit.html

from riscv_assembler.utils import *

# instantiate toolkit
tk = Toolkit()

# instruction to binary
instr = tk.R_type("add", "x1", "x2", "x3")

print(instr)

# note: need some logic to determine what type the command is before passing
# through specific function