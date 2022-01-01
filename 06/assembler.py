import sys

COMMAND_TYPE_MAP = {
    'A_COMMAND':1,
    'C_COMMAND':2,
    'L_COMMAND':3,
}

symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 0x4000,
    'KBD': 0x6000
}

COMP_DIC = {
    "0":  "0101010",
    "1":  "0111111",
    "-1": "0111010",
    "D":  "0001100",
    "A":  "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1":"0011111",
    "A+1":"0110111",
    "D-1":"0001110",
    "A-1":"0110010",
    "D+A":"0000010",
    "D-A":"0010011",
    "A-D":"0000111",
    "D&A":"0000000",
    "D|A":"0010101",
    "M":  "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1":"1110111",
    "M-1":"1110010",
    "D+M":"1000010",
    "D-M":"1010011",
    "M-D":"1000111",
    "D&M":"1000000",
    "D|M":"1010101",
}

DEST_DIC = {
    ""  : "000",
    "M" : "001",
    "D" : "010",
    "MD": "011",
    "A" : "100",
    "AM": "101",
    "AD": "110",
    "AMD":"111",
}

JUMP_DIC = {
    ""    : "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111",
}

current_command_type = ''


def command_type(instruction):
    if instruction[0] == '@':
        return COMMAND_TYPE_MAP["A_COMMAND"]
    elif instruction[0] == '(':
        return COMMAND_TYPE_MAP["L_COMMAND"]
    else:
        return COMMAND_TYPE_MAP["C_COMMAND"]

def symbol(instruction, command_type):
    # A command
    # @xxx -> xxx
    if command_type == 1:
        return instruction[1:]
    # L command
    # (xxx) -> xxx
    if command_type == 3:
        return instruction[1:-1]

def add_entry(symbol, address):
    symbol_table[symbol] = address

def contains(symbol):
    return True if symbol_table.get(symbol) else False

def get_address(symbol):
    return symbol_table[symbol]

def parser():
    instructions = []
    while True:
        line = file.readline()
        # 命令が無いから終わり
        if not line:
            break
        # 命令の処理
        # 本のadvanceにあたる処理
        else:
            line = line.strip().replace(' ', '')
            comment_out_idx = line.find("//")
            if comment_out_idx >= 0:
                line = line[:comment_out_idx]
            if line == '':
                continue
            instructions.append(line)
    nextVariableAddress = 16
    # First Pass
    # only make a symbol table
    addressNumber = 0
    for instruction in instructions:
        commandtype = command_type(instruction)
        if (commandtype == 1 or commandtype == 2):
            addressNumber += 1
        if (commandtype == 3):
            instruction = symbol(instruction, commandtype)
            add_entry(instruction, addressNumber)
            addressNumber += 1

    # Second pass
    hoge = 0
    for instruction in instructions:
        commandtype = command_type(instruction)
        # A or L command
        if (commandtype == 1):
            a = symbol(instruction, commandtype)
            if (a.isdigit()):
                # @値
                print("{}".format(str(format(int(a), 'b')).zfill(16)))
            else:
                # @シンボル
                if (contains(a)):
                    # symbol found pattern
                    a = get_address(a)
                    print("{}".format(str(format(a, 'b')).zfill(16)))
                else:
                    # symbol not found pattern
                    add_entry(a, nextVariableAddress)
                    nextVariableAddress += 1
                    a = get_address(a)
                    print("{}".format(str(format(a, 'b')).zfill(16)))
                    hoge += 1

        # C command
        elif (commandtype == 2):
            if '=' in instruction:
                destination, comp_and_jump = instruction.split('=')
            else:
                comp_and_jump = instruction
                destination = ''
            if ';' in comp_and_jump:
                compare, jump = comp_and_jump.split(';')
            else:
                compare = comp_and_jump
                jump = ''
            tmp = "111" + COMP_DIC[compare] + DEST_DIC[destination] + JUMP_DIC[jump]
            print(tmp)
        else:
            pass

    print(hoge)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("ファイルを指定して❤")
        
    else:
        file_path = sys.argv[1]
    file = open(file_path, 'r')
    parser()