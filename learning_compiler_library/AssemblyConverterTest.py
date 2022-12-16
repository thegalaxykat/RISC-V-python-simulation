# documentation at https://www.riscvassembler.org/ac.html
from riscv_assembler.convert import AssemblyConverter

# instantiate converter with parameters
cnv = AssemblyConverter(output_type="t", nibble=False)

# convert assembly file to binary
cnv.convert('./learning_compiler_library/sample.s')