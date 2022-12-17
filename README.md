# RISC-V Python Simulation

By Joseph Gilbert, Kat Canavan, Arturo Joya

This repository contains the files used to create a command-line based simulation of a RISC-V CPU using Python. This is meant to be used as a tool for debugging assembly code, as its main functionality is outputting the register file of the CPU every time an instruction is run.

## Dependencies
This simulation was run and tested using Python 3.10 in Ubuntu 20.04 and we do not guarantee its functionality outside of this version of Python or OS. We also use the following libraries that allow our code to function properly.

- bitstring (downloadable by running `pip install bitstring`)

- riscv-assembler (downloadable by running `pip install riscv-assembler`)([documentation](https://github.com/kcelebi/riscv-assembler))

These are also references in `requirements.txt` in this repository.

## Using our Code
Start by opening a command-line terminal and go the where this repository lives on your computer.

Our program offers two ways of testing assembly. 

1. Test assembly code line by line

2. Test an assembly code file.

### Line By Line
To test assembly code line by line, simply run `python3 main.py`. You will be prompted to type in assembly code for example `addi t0, zero, 42` will store the immediate data `42` to register t0. If you choose to output verbose information (by initializing as ` `), you will be able to see the entire register.

```
Instruction : addi t0, zero, 42
PC : 0
+----Register File----+
|x00 | zero | 00000000|
|x01 | ra   | xxxxxxxx|
.Rest of the registers.
|x05 | t0   | 0000002A|
.Rest of the registers.
+---------------------+
```
Otherwise, you can also choose to only display the registers that have been changed so far. Assuming that `addi t0, zero, 42` was already run, typing in `addi t1, t0, 63` would result in the following output, which may be easier to follow.
```
Instruction : addi t1, t0, 63
PC : 4
+----Register File----+
|x05 | t0   | 0000002A|
|x06 | t1   | 00000069|
+---------------------+
```
### Assembly File
To test assembly code through a file, run `python3 main.py FILENAME.s`. This will run the simulation automatically and output the register file after executing each instruction. You can choose to output either a verbose register file or just the register files that have been messed with. The following is an example output had we had a file containing the assembly code from the Line by Line example in non-verbose display.
```
Instruction : addi t0, zero, 42
PC : 0
+----Register File----+
|x05 | t0   | 0000002A|
+---------------------+
Instruction : addi t1, t0, 63
PC : 4
+----Register File----+
|x05 | t0   | 0000002A|
|x06 | t1   | 00000069|
+---------------------+
```

## Our Software Design
We decided to implement this simulation using object oriented design. We followed the model-view-controller architecture to divide the program's functionality. The following is a quick breakdown of our program

(_insert diagram of mvc simulator_)

Please read through the comments on our code and their respective docstrings for more information on how the code gets the job done.