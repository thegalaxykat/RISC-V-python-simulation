import bitstring
from bitstring import BitArray

#bitstring.lsb0 = True
#BitArray = bitstring.BitArray

memh_str_f = """00300113 // PC=0x0 line=10: addi sp, zero, 3
01c11113 // PC=0x4 line=11: slli sp, sp, 28
3fc10113 // PC=0x8 line=12: addi sp, sp, 1020
00100513 // PC=0xc line=15: addi a0, zero, 1
00200593 // PC=0x10 line=16: addi a1, zero, 2
00300613 // PC=0x14 line=17: addi a2, zero, 3
00400693 // PC=0x18 line=18: addi a3, zero, 4
0bc000ef // PC=0x1c line=19: call SUM_4
00a00293 // PC=0x20 line=21: addi t0, zero, 10
0a551863 // PC=0x24 line=22: bne a0, t0, DONE # End the program if the result isn't 10.
00400513 // PC=0x28 line=25: addi a0, zero, 4
00300593 // PC=0x2c line=26: addi a1, zero, 3
00200613 // PC=0x30 line=27: addi a2, zero, 2
00100693 // PC=0x34 line=28: addi a3, zero, 1
0b0000ef // PC=0x38 line=29: call DIFF_OF_SUMS
00400293 // PC=0x3c line=30: addi t0, zero, 4
08551a63 // PC=0x40 line=31: bne a0, t0, DONE # End the program if the result isn't 4.
00000513 // PC=0x44 line=34: addi a0, zero, 0
01100593 // PC=0x48 line=35: addi a1, zero, 17
0ac000ef // PC=0x4c line=36: call MUL
08051263 // PC=0x50 line=37: bne a0, zero, DONE # End program on wrong result.
01100513 // PC=0x54 line=39: addi a0, zero, 17
00000593 // PC=0x58 line=40: addi a1, zero, 0
09c000ef // PC=0x5c line=41: call MUL
06051a63 // PC=0x60 line=42: bne a0, zero, DONE # End program on wrong result.
00100513 // PC=0x64 line=44: addi a0, zero, 1
01100593 // PC=0x68 line=45: addi a1, zero, 17
08c000ef // PC=0x6c line=46: call MUL
01100293 // PC=0x70 line=47: addi t0, zero, 17
06551063 // PC=0x74 line=48: bne a0, t0, DONE # End program on wrong result.
01100513 // PC=0x78 line=50: addi a0, zero, 17
00100593 // PC=0x7c line=51: addi a1, zero, 1
078000ef // PC=0x80 line=52: call MUL
01100293 // PC=0x84 line=53: addi t0, zero, 17
04551663 // PC=0x88 line=54: bne a0, t0, DONE # End program on wrong result.
06400593 // PC=0x8c line=57: addi a1, zero, 100  # Stop if we have more than 100 calls
00000db3 // PC=0x90 line=59: add s11, zero, zero # Reset stack counter
00200513 // PC=0x94 line=60: addi a0, zero, 2
0a4000ef // PC=0x98 line=61: call FIBONACCI
00100293 // PC=0x9c line=62: addi t0, zero, 1
02551a63 // PC=0xa0 line=63: bne a0, t0, DONE # End program on wrong result.
06400593 // PC=0xa4 line=66: addi a1, zero, 100  # Stop if we have more than 100 calls
00000db3 // PC=0xa8 line=68: add s11, zero, zero # Reset stack counter
00300513 // PC=0xac line=69: addi a0, zero, 3
08c000ef // PC=0xb0 line=70: call FIBONACCI
00200293 // PC=0xb4 line=71: addi t0, zero, 2
00551e63 // PC=0xb8 line=72: bne a0, t0, DONE # End program on wrong result.
06400593 // PC=0xbc line=75: addi a1, zero, 100  # Stop if we have more than 100 calls
00000db3 // PC=0xc0 line=77: add s11, zero, zero # Reset stack counter
00700513 // PC=0xc4 line=78: addi a0, zero, 7
074000ef // PC=0xc8 line=79: call FIBONACCI
00d00293 // PC=0xcc line=80: addi t0, zero, 13
00551263 // PC=0xd0 line=81: bne a0, t0, DONE # End program on wrong result.
00000063 // PC=0xd4 line=84: DONE: beq zero, zero, DONE
00b502b3 // PC=0xd8 line=89: add t0, a0, a1 # SUM_4: use temporaries, no need to preserve regs.
00d60333 // PC=0xdc line=90: add t1, a2, a3
00628533 // PC=0xe0 line=91: add a0, t0, t1
00008067 // PC=0xe4 line=92: ret
00b502b3 // PC=0xe8 line=96: add t0, a0, a1
00d60333 // PC=0xec line=97: add t1, a2, a3
40628533 // PC=0xf0 line=98: sub a0, t0, t1
00008067 // PC=0xf4 line=99: ret
02050863 // PC=0xf8 line=104: beq a0, zero, MUL_PRODUCT_IS_ZERO
02058663 // PC=0xfc line=105: beq a1, zero, MUL_PRODUCT_IS_ZERO
00100293 // PC=0x100 line=106: addi t0, zero, 1
02550663 // PC=0x104 line=107: beq a0, t0, MUL_A0_IS_ONE
02658863 // PC=0x108 line=108: beq a1, t1, MUL_A1_IS_ONE
00b002b3 // PC=0x10c line=109: add t0, zero, a1 # loop index start
00000333 // PC=0x110 line=110: add t1, zero, zero # product accumulator
00028663 // PC=0x114 line=112: beq t0, zero, MUL_FOR_END
00a30333 // PC=0x118 line=113: add t1, t1, a0
fff28293 // PC=0x11c line=114: addi t0, t0, -1 # t0--
00600533 // PC=0x120 line=116: add a0, x0, t1
00008067 // PC=0x124 line=117: ret
00000533 // PC=0x128 line=119: add a0, zero, zero # Early return if product is zero.
00008067 // PC=0x12c line=120: ret
00058533 // PC=0x130 line=122: add a0, a1, zero # Early return if product is a1.
00008067 // PC=0x134 line=123: ret
00008067 // PC=0x138 line=125: ret # Early return if product is a0.
04bdde63 // PC=0x13c line=132: bge s11, a1, FIB_STACK_OVERFLOW # Check if we've exceeded a1 calls, if so return -1.
001d8d93 // PC=0x140 line=133: addi s11, s11, 1  # Keep track of number of iterations in s11.
ff410113 // PC=0x144 line=135: addi sp, sp, -12  # Make space for variables that need to be preserved call to call.
00a12023 // PC=0x148 line=136: sw a0,  0(sp)     # Push a0 onto the stack.
00112223 // PC=0x14c line=137: sw ra,  4(sp)     # Push ra onto the stack.
00812423 // PC=0x150 line=138: sw s0,  8(sp)     # Use s0 to store the extra call result.
00100293 // PC=0x154 line=140: addi t0, zero, 1
02550c63 // PC=0x158 line=141: beq a0, t0, FIB_ONE
00200293 // PC=0x15c line=142: addi t0, zero, 2
02550863 // PC=0x160 line=143: beq  a0, t0, FIB_ONE
fff50513 // PC=0x164 line=144: addi a0, a0, -1
fd5ff0ef // PC=0x168 line=145: call FIBONACCI # fib(n-1)
00050433 // PC=0x16c line=146: add s0, a0, zero # save the result.
00012503 // PC=0x170 line=147: lw a0, 0(sp) # Recall original a0.
ffe50513 // PC=0x174 line=148: addi a0, a0, -2
fc5ff0ef // PC=0x178 line=149: call FIBONACCI # fib(n-2)
00a40533 // PC=0x17c line=150: add a0, s0, a0
00412083 // PC=0x180 line=153: lw ra,  4(sp)     # Pop ra from the stack.
00812403 // PC=0x184 line=154: lw s0,  8(sp)     # Pop s0 from the stack.
00c10113 // PC=0x188 line=155: addi sp, sp, 12   # Deallocate the stack variables.
00008067 // PC=0x18c line=156: ret
00100513 // PC=0x190 line=158: addi a0, zero, 1
fedff06f // PC=0x194 line=159: j FIB_STACK_POP_AND_RETURN
fff00513 // PC=0x198 line=161: addi a0, zero, -1
fe5ff06f // PC=0x19c line=162: j FIB_STACK_POP_AND_RETURN"""

memh_str_ls = """00300193 // PC=0x0 line=4: addi gp, zero, 3
01c19193 // PC=0x4 line=5: slli gp, gp, 28
20018113 // PC=0x8 line=6: addi sp, gp, 512
01100293 // PC=0xc line=7: addi t0, zero, 17
fe512e23 // PC=0x10 line=9: sw t0, -4(sp)
01128293 // PC=0x14 line=10: addi t0, t0, 17
fe512c23 // PC=0x18 line=11: sw t0, -8(sp)
01128293 // PC=0x1c line=12: addi t0, t0, 17
fe512a23 // PC=0x20 line=13: sw t0, -12(sp)
01128293 // PC=0x24 line=14: addi t0, t0, 17
fe512823 // PC=0x28 line=15: sw t0, -16(sp)
ff012283 // PC=0x2c line=17: lw t0, -16(sp)
0051a023 // PC=0x30 line=18: sw t0, 0(gp)
06502c23 // PC=0x34 line=19: sw t0, 120(zero)
ff412303 // PC=0x38 line=20: lw t1, -12(sp) // pc 56
0061a223 // PC=0x3c line=21: sw t1, 4(gp)
06602e23 // PC=0x40 line=22: sw t1, 124(zero)
ff812383 // PC=0x44 line=23: lw t2, -8(sp)
0071a423 // PC=0x48 line=24: sw t2, 8(gp)
08702023 // PC=0x4c line=25: sw t2, 128(zero)
ffc12e03 // PC=0x50 line=26: lw t3, -4(sp)
01c1a623 // PC=0x54 line=27: sw t3, 12(gp)
09c02223 // PC=0x58 line=28: sw t3, 132(zero)"""
memh_str_b="""00100093 // PC=0x0 line=6: addi x1, x0, 1
fff00113 // PC=0x4 line=7: addi x2, x0, -1
00000f93 // PC=0x8 line=8: addi x31, x0, 0
00000463 // PC=0xc line=9: beq x0, x0, BEQ_WORKS
001f8f93 // PC=0x10 line=10: addi x31, x31, 1 # Should never run!
00100513 // PC=0x14 line=11: BEQ_WORKS: addi x10, x0, 1
00209463 // PC=0x18 line=12: bne x1, x2, BNE_WORKS
001f8f93 // PC=0x1c line=13: addi x31, x31, 1 # Should never run!
00100593 // PC=0x20 line=14: BNE_WORKS: addi x11, x0, 1
00114463 // PC=0x24 line=15: blt x2, x1, BLT_WORKS
001f8f93 // PC=0x28 line=16: addi x31, x31, 1 # Should never run!
00100613 // PC=0x2c line=17: BLT_WORKS: addi x12, x0, 1
00005463 // PC=0x30 line=18: bge x0, x0, BGE_WORKS
001f8f93 // PC=0x34 line=19: addi x31, x31, 1 # Should never run!
00100693 // PC=0x38 line=20: BGE_WORKS: addi x13, x0, 1
0020e463 // PC=0x3c line=21: bltu x1, x2, BLTU_WORKS
001f8f93 // PC=0x40 line=22: addi x31, x31, 1 # Should never run!
00100713 // PC=0x44 line=23: BLTU_WORKS: addi x14, x0, 1
00117463 // PC=0x48 line=24: bgeu x2, x1, BGEU_WORKS
001f8f93 // PC=0x4c line=25: addi x31, x31, 1 # Should never run!
00100793 // PC=0x50 line=26: BGEU_WORKS: addi x15, x0, 1
00000063 // PC=0x54 line=27: INFINITE_LOOP: beq x0, x0, INFINITE_LOOP"""
memh_bit = [BitArray("0x"+line.split(" ")[0],length=31) for line in memh_str_f.split("\n")]
memh_dict = dict([(i*4,word) for i,word in enumerate(memh_bit)])
