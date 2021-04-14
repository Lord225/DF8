<center><h1>DF8 Emulator Documentation</h1></center>

## CU Commands

| Index | Code | Description                     | Structure                                          |
| :---: | :--- | :------------------------------ | :------------------------------------------------- |
| 0     | int  | Interrupt                       | int code[4], options[8]                            |
| 1     | mov  | Move const to register          | mov register[4], value[8]                          |
| 2     | mvr  | Move register to register       | mvr register[4], source[4]                         |
| 3     | alu  | ALU Operation                   | alu operation[4], registerONE[4], registerTWO[4]   |
| 4     | wrt  | Write to memory                 | wrt source[4], memory_cell[8]                      |
| 5     | wrr  | Write to memory[register]       | wrr sourceMEM[4], source[4]                        |
| 6     | rd   | Read from memory                | rd register[4], memory_cell[8]                     |
| 7     | rdr  | Read from memory[register]      | rdr register[4], sourceMEM[4]                      |
| 8     | jmp  | Unconditional jump              | jmp line[8]                                        |
| 9     | jmr  | Unconditional jump[register]    | jmr source[4]                                      |
| 10    | jif  | Jump if flag                    | jif flag[4], line[8]                               |
| 11    | jrf  | Jump[register] if flag          | jrf flag[4], source[4]                             |
| 12    | jir  | Jump if requirement             | jir requirement[4], line[8]                        |
| 13    | jrr  | Jump[register15] if requirement | jrr requirement[4], registerONE[4], registerTWO[4] |
| 14    | cll  | Call                            | cll line[8]                                        |
| 15    | rtn  | Return                          | rtn                                                |

<br>

## ALU Operations

| Index | Operation |
| :---: | :-------- |
| 0     | AND       |
| 1     | OR        |
| 2     | XOR       |
| 3     | NOT       |
| 4     | RSH       |
| 5     | LSH       |
| 6     | ADD       |
| 7     | SUB       |
| 8     | INC       |
| 9     | DEC       |

<br>

## Interrupts

| Index | Description                      | Structure              |
| :---: | :------------------------------- | :--------------------- |
| 0     | Shut down                        | int 0x0, 0x00          |
| 1     | User input (value) -> reg[15]    | int 0x1, 0x00          |
| 2     | User input (keyboard) -> reg[15] | int 0x2, 0x00          |
| 3     |                                  |                        |
| 4     |                                  |                        |
| 5     |                                  |                        |
| 6     |                                  |                        |
| 7     |                                  |                        |
| 8     |                                  |                        |
| 9     |                                  |                        |
| 10    |                                  |                        |
| 11    |                                  |                        |
| 12    |                                  |                        |
| 13    |                                  |                        |
| 14    | Set debugging to True or False   | int 0xE, value[...]    |
| 15    | Output of register               | int 0xF, register[...] |

<br>

## Requirements

| Index | Description |
| :---: | :---------- |
| 0     | A > B       |
| 1     | A < B       |
| 2     | A >= B      |
| 3     | A <= B      |
| 4     | A == B      |
| 5     | A != B      |
| 6     | A == 0      |
| 7     | A != 0      |
| 8     | A == 1      |
| 9     | A != 1      |

<br>

## Flags
| Index | Description   |
| :---: | :------------ |
| 0     | Zero flag     |
| 1     | Overflow flag |

<br>

Author: <b><a href="https://github.com/diffiii/">diffi</a></b>
