COMMANDS = {
    'int': {
        'structure': '122',
        'index': 0
    },
    'mov': {
        'structure': '122',
        'index': 1
    },
    'mvr': {
        'structure': '12-',
        'index': 2
    },
    'alu': {
        'structure': '123',
        'index': 3
    },
    'wrt': {
        'structure': '122',
        'index': 4
    },
    'wrr': {
        'structure': '12-',
        'index': 5
    },
    'rd': {
        'structure': '122',
        'index': 6
    },
    'rdr': {
        'structure': '12-',
        'index': 7
    },
    'jmp': {
        'structure': '-11',
        'index': 8
    },
    'jmr': {
        'structure': '1--',
        'index': 9
    },
    'jif': {
        'structure': '122',
        'index': 10
    },
    'jrf': {
        'structure': '12-',
        'index': 11
    },
    'jir': {
        'structure': '122',
        'index': 12
    },
    'jrr': {
        'structure': '123',
        'index': 13
    },
    'cll': {
        'structure': '-11',
        'index': 14
    },
    'rtn': {
        'structure': '---',
        'index': 15
    }
}

def converter(command_line: str):
    cmdlines = command_line.replace(',', '').replace('\n', '').split(' ')
    command, args, result = cmdlines[0], [], ''

    for i, element in enumerate(cmdlines):
        if i != 0:
            args.append(bin(int(element, 16))[2:])

    result += bin(COMMANDS[command]['index'])[2:].zfill(4)
    structure = COMMANDS[command]['structure']


    for i in range(3):
        if structure[i] == '-':
            result += '0000'
        else:
            try:
                if structure[i] == structure[i + 1]:
                    result += args[0].zfill(8)
                    args.remove(args[0])
                    break
            except Exception:
                pass
            result += args[0].zfill(4)
            args.remove(args[0])

    return result

def convert():
    with open('Program') as pfile:
        with open('ROM', 'w') as rom:
            program = pfile.readlines()
            for line in program:
                if line.startswith(';') or line == '\n':
                    program.remove(line)
            towrite = ['0000000000000000\n'] * 256
            towrite[255] = '1000000000000000'
            for i, line in enumerate(program):
                towrite[i] = f'{converter(line)}\n'
            rom.writelines(towrite)

if __name__ == '__main__':
    convert()
