import time
import numpy as np
from typing import Literal, Optional
from DF8Converter import convert


def ROM(filename: Optional[str]='ROM'):
    ROM = []
    with open(filename) as file:
        contents = file.read().replace(' ', '').replace('\n', '')
    for i in range(256):
        ROM.append(contents[i*16:i*16+16])
    return ROM


class DF8:
    def __init__(self, memory: np.ndarray):
        self.__registers = np.zeros(16, np.ubyte)
        self.__memory = memory
        self.__flags = {'zero': False, 'overflow': False}
        self.__stack = []
        self.__pc = 0xFF  # 0xFF in memory is initializing command line (jump(...) recommended)
        self.__on = False
        self.__debug = True

    def init(self):
        self.__on = True

    @property
    def PC(self):
        return self.__pc

    @property
    def ON(self):
        return self.__on

    def __repr__(self):
        return ', '.join(f'\33[94m{str(register)}\33[0m' for register in self.__registers)

    #########################
    ###     Executing     ###
    #########################

    def __call__(self, command_line: str):
        self.__pc = np.ubyte(self.__pc + 1)

        if int(command_line[0:4], 2) == 0:
            if self.__debug: print(f'\33[91mint\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__int(int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 1:
            if self.__debug: print(f'\33[91mmov\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__mov(int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 2:
            if self.__debug: print(f'\33[91mmvr\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}')
            self.__mvr(int(command_line[4:8], 2), int(command_line[8:12], 2))
        elif int(command_line[0:4], 2) == 3:
            if self.__debug: print(f'\33[91malu\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}, {hex(int(command_line[12:16], 2))}')
            self.__alu(int(command_line[4:8], 2), int(command_line[8:12], 2), int(command_line[12:16], 2))
        elif int(command_line[0:4], 2) == 4:
            if self.__debug: print(f'\33[91mwrt\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__wrt(int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 5:
            if self.__debug: print(f'\33[91mwrr\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}')
            self.__wrr(int(command_line[4:8], 2), int(command_line[8:12], 2))
        elif int(command_line[0:4], 2) == 6:
            if self.__debug: print(f'\33[91mrd\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__rd (int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 7:
            if self.__debug: print(f'\33[91mrdr\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}')
            self.__rdr(int(command_line[4:8], 2), int(command_line[8:12], 2))
        elif int(command_line[0:4], 2) == 8:
            if self.__debug: print(f'\33[91mjmp\33[0m {hex(int(command_line[8:16], 2))}')
            self.__jmp(int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 9:
            if self.__debug: print(f'\33[91mjmr\33[0m {hex(int(command_line[4:8], 2))}')
            self.__jmr(int(command_line[4:8], 2))
        elif int(command_line[0:4], 2) == 10:
            if self.__debug: print(f'\33[91mjif\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__jif(int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 11:
            if self.__debug: print(f'\33[91mjrf\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}')
            self.__jrf(int(command_line[4:8], 2), int(command_line[8:12], 2))
        elif int(command_line[0:4], 2) == 12:
            if self.__debug: print(f'\33[91mjir\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:16], 2))}')
            self.__jir(int(command_line[4:8], 2), int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 13:
            if self.__debug: print(f'\33[91mjrr\33[0m {hex(int(command_line[4:8], 2))}, {hex(int(command_line[8:12], 2))}, {hex(int(command_line[12:16], 2))}')
            self.__jrr(int(command_line[4:8], 2), int(command_line[8:12], 2), int(command_line[12:16], 2))
        elif int(command_line[0:4], 2) == 14:
            if self.__debug: print(f'\33[91mcll\33[0m {hex(int(command_line[8:16], 2))}')
            self.__cll(int(command_line[8:16], 2))
        elif int(command_line[0:4], 2) == 15:
            if self.__debug: print('\33[91mrtn\33[0m')
            self.__rtn()

    #########################
    ###     Interrupt     ###
    #########################

    def __int(self, code: Literal[0,...,15], options: Literal[0,...,255]):
        if code == 0:
            self.__on = False
        elif code == 1:
            _input = int(input('\033[95mUser input (val) > \033[92m'))
            self.__mov(0xF, np.ubyte(_input))
            self.__wrt(0xF, 0xFF)
        elif code == 2:
            _input = input('\033[95mUser input (kbd) > \033[92m')
            if _input == 'ESC': _input = 27
            elif _input == 'TAB': _input = 9
            elif _input == 'BSP': _input = 8
            elif _input == 'ENT': _input = 13
            elif _input == 'DEL': _input = 127
            else: _input = ord(_input)
            self.__mov(0xF, np.ubyte(_input))
            self.__wrt(0xF, 0xFF)
        elif code == 14:
            self.__debug = bool(options) 
        elif code == 15:
            print('\033[92mOutput >\033[95m', self.__registers[options % 16])

    #########################
    ###     Registers     ###
    #########################

    def __mov(self, register: Literal[0,...,15], value: np.ubyte):
        self.__registers[register] = value

    def __mvr(self, register: Literal[0,...,15], source: Literal[0,...,15]):
        self.__registers[register] = self.__registers[source]

    #########################
    ###        RAM        ###
    #########################

    def __wrt(self, source: Literal[0,...,15], memory_cell: Literal[0,...,255]):
        self.__memory[memory_cell] = self.__registers[source]

    def __wrr(self, sourceMEM: Literal[0,...,15], source: Literal[0,...,15]):
        self.__memory[self.__registers[sourceMEM]] = self.__registers[source]

    def __rd(self, register: Literal[0,...,15], memory_cell: Literal[0,...,255]):
        self.__registers[register] = self.__memory[memory_cell]

    def __rdr(self, register: Literal[0,...,15], sourceMEM: Literal[0,...,15]):
        self.__registers[register] = self.__memory[self.__registers[sourceMEM]]

    #########################
    ###        ALU        ###
    #########################

    def __alu(self, operation: Literal[0,...,15], registerONE: Literal[0,...,15], registerTWO: Literal[0,...,15]):

        def _and(registerA: Literal[0,...,15], registerB: Literal[0,...,15]):
            result = self.__registers[registerA] & self.__registers[registerB]
            if result % 255 == 0: self.__flags['zero'] = True
            return result

        def _or(registerA: Literal[0,...,15], registerB: Literal[0,...,15]):
            result = self.__registers[registerA] | self.__registers[registerB]
            if result % 255 == 0: self.__flags['zero'] = True
            return result

        def _xor(registerA: Literal[0,...,15], registerB: Literal[0,...,15]):
            result = self.__registers[registerA] ^ self.__registers[registerB]
            if result % 255 == 0: self.__flags['zero'] = True
            return result

        def _not(registerTO: Literal[0,...,15], registerFROM: Literal[0,...,15]):
            result = ~self.__registers[registerFROM]
            if result % 255 == 0: self.__flags['zero'] = True
            return result

        def _rsh(registerTO: Literal[0,...,15], registerFROM: Literal[0,...,15]):
            result = self.__registers[registerFROM] >> 1
            if result % 255 == 0: self.__flags['zero'] = True
            return result

        def _lsh(registerTO: Literal[0,...,15], registerFROM: Literal[0,...,15]):
            result = int(self.__registers[registerFROM]) << 1
            if result % 255 == 0: self.__flags['zero'] = True
            if result > 255: self.__flags['overflow'] = True
            return result

        def _add(registerA: Literal[0,...,15], registerB: Literal[0,...,15]):
            result = int(self.__registers[registerA]) + int(self.__registers[registerB])
            if result % 255 == 0: self.__flags['zero'] = True
            if result > 255: self.__flags['overflow'] = True
            return result

        def _sub(registerA: Literal[0,...,15], registerB: Literal[0,...,15]):
            result = int(self.__registers[registerA]) + int(~self.__registers[registerB]) + 1
            if result % 255 == 0: self.__flags['zero'] = True
            if result > 255: self.__flags['overflow'] = True
            return result

        def _inc(registerTO: Literal[0,...,15], registerFROM: Literal[0,...,15]):
            result = int(self.__registers[registerFROM]) + 1
            if result % 255 == 0: self.__flags['zero'] = True
            if result > 255: self.__flags['overflow'] = True
            return result

        def _dec(registerTO: Literal[0,...,15], registerFROM: Literal[0,...,15]):
            result = int(self.__registers[registerFROM]) + 255
            if result % 255 == 0: self.__flags['zero'] = True
            if result > 255: self.__flags['overflow'] = True
            return result

        if operation == 0:   self.__registers[registerONE] = _and(registerONE, registerTWO)
        elif operation == 1: self.__registers[registerONE] = _or (registerONE, registerTWO)
        elif operation == 2: self.__registers[registerONE] = _xor(registerONE, registerTWO)
        elif operation == 3: self.__registers[registerONE] = _not(registerONE, registerTWO)
        elif operation == 4: self.__registers[registerONE] = _rsh(registerONE, registerTWO)
        elif operation == 5: self.__registers[registerONE] = _lsh(registerONE, registerTWO)
        elif operation == 6: self.__registers[registerONE] = _add(registerONE, registerTWO)
        elif operation == 7: self.__registers[registerONE] = _sub(registerONE, registerTWO)
        elif operation == 8: self.__registers[registerONE] = _inc(registerONE, registerTWO)
        elif operation == 9: self.__registers[registerONE] = _dec(registerONE, registerTWO)

    #########################
    ###        ROM        ###
    #########################

    def __jmp(self, line: np.ubyte):
        self.__pc = line

    def __jmr(self, source: Literal[0,...,15]):
        self.__pc = self.__registers[source]

    def __jif(self, flag: Literal[0, 1], line: np.ubyte):
        if list(self.__flags.values())[flag]:
            self.__pc = line

    def __jrf(self, flag: Literal[0, 1], source: Literal[0,...,15]):
        if list(self.__flags.values())[flag]:
            self.__pc = self.__registers[source]

    def __jir(self, requirement: Literal[0,...,15], line: np.ubyte):                                                                      # ?????????
        if {
            0: self.__registers[0] > self.__registers[1],
            1: self.__registers[0] < self.__registers[1],
            2: self.__registers[0] >= self.__registers[1],
            3: self.__registers[0] <= self.__registers[1],
            4: self.__registers[0] == self.__registers[1],
            5: self.__registers[0] != self.__registers[1],
            6: self.__registers[0] == 0,
            7: self.__registers[0] != 0,
            8: self.__registers[0] == 1,
            9: self.__registers[0] != 1
        }[requirement]:
            self.__pc = line

    def __jrr(self, requirement: Literal[0,...,15], registerONE: Literal[0,...,15], registerTWO: Literal[0,...,15]):
        if {
            0: self.__registers[registerONE] > self.__registers[registerTWO],
            1: self.__registers[registerONE] < self.__registers[registerTWO],
            2: self.__registers[registerONE] >= self.__registers[registerTWO],
            3: self.__registers[registerONE] <= self.__registers[registerTWO],
            4: self.__registers[registerONE] == self.__registers[registerTWO],
            5: self.__registers[registerONE] != self.__registers[registerTWO],
            6: self.__registers[registerONE] == 0,
            7: self.__registers[registerONE] != 0,
            8: self.__registers[registerONE] == 1,
            9: self.__registers[registerONE] != 1
        }[requirement]:
            self.__pc = self.__registers[15]

    def __cll(self, line: np.ubyte):
        if len(self.__stack) < 16:
            self.__stack.append(self.__pc)
            self.__pc = line
        else:
            raise OverflowError('Stack overflow')

    def __rtn(self):
        self.__pc = self.__stack.pop()


def run():
    ROM_ = ROM('ROM')
    MEM_ = np.zeros(256, np.ubyte)
    DF8_ = DF8(MEM_)

    FREQ = 10

    DF8_.init()  # Starting the CPU

    while DF8_.ON:  # Executing program allocated in ROM from 0xFF
        DF8_(ROM_[DF8_.PC])
        time.sleep(1 / FREQ)

    print(DF8_)  # Printing the CPU's registers

if __name__ == '__main__':
    convert()
    run()
