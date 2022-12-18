# RISC-V Python Simulation

Joseph Gilbert, Kat Canavan, and Arturo Joya

This repository contains the files used to create a command-line based simulation of a RISC-V CPU using Python. Both a debugging and educational tool, this program takes assembly as input and returns the register files after each instruction. Note that store/load half and byte instructions are not supported.

For the conversion from assembly to binary we've slightly modified some course material, `assembler.py` from Avinash Nonholonomy's Olin Computer Architecture course material ([GitHub]([GitHub - avinash-nonholonomy/olin-cafe-f22: Repository for Olin's ENGR3410 - Fall 2022](https://github.com/avinash-nonholonomy/olin-cafe-f22))). Thanks Avinash!

## Dependencies

This simulation was run and tested using Python 3.10. Prior versions of Python are not compatible.

Only one library that needs to be installed is bitstring which can either be installed with `pip install bitstring` or

```bash
pip install -r requirements.txt
```

## Using our Code

This program requires the user to be at least somewhat familiar with command line interfaces. Create a clone of this repository to your local machine and navigate to that directory in a command-line terminal. 

There are two methods of inputting RISC-V assembly code:

1. Enter instructions line-by-line, live, through the terminal and immediately see the result of each given command. Since this is live, only I Type, R Type, and store word instructions are supported.

2. Process an entire assembly (.s) file. All instructions are processed and when the program is complete the relevant registers are displayed per step. This mode supports all RISC-V 32I instructions except those involving halfs and bytes. 

Each of these methods are described in more detail below.

### Line By Line

To test assembly code live, a line at a time, simply run `python3 main.py`. You will be prompted to type in assembly code (e.g `addi t0, zero, 42` to store the immediate  `42` to register t0).

```bash
Instruction : addi t0, zero, 42
PC : 0
+----Register File----+
|x05 | t0   | 0000002A|
+---------------------+
```

As you can see, the output only displays the registers that have been changed so far. Assuming that `addi t0, zero, 42` was already run, typing in `addi t1, t0, 63` would result in the following output. We implemented the output this way as we figured it would be way easier to debug a program without having to scroll through lots of meaningless register outputs (meaningless in the context of the user's specific program, that is).

```bash
Instruction : addi t1, t0, 63
PC : 4
+----Register File----+
|x05 | t0   | 0000002A|
|x06 | t1   | 00000069|
+---------------------+
```

### Assembly File

To test assembly code through a file, run `python3 main.py FILENAME.s` (where `FILENAME.s` is the filepath). This will run the simulation automatically and output the register file after executing each instruction. The following is an example output from a file containing the assembly code from the Line by Line example in non-verbose display.

```bash
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

![MCV Diagram](MVC.png)

Please read through the comments on our code and function docstrings for more information on precisely how the it works.


### Tests
Test cases with randomly generated instruction were used to test the system. The code behind these tests can be found in `test_single_line.py`, although it should be noted that the tests will be different each time.
