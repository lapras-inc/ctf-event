from pathlib import Path

ENCODED = bytes.fromhex(Path(__file__).with_name("program.hex").read_text())


def rol(value, shift):
    shift &= 7
    return ((value << shift) | (value >> ((8 - shift) & 7))) & 255


def decode():
    return bytes(rol(byte ^ ((i * 73 + 41) & 255), -(i % 7))
                 for i, byte in enumerate(ENCODED))


def verify(key):
    if len(key) != 32 or any(c not in "0123456789abcdef" for c in key):
        return False
    values = [int(c, 16) for c in key]
    if any(len(set(values[start:start + 16])) != 16 for start in (0, 16)):
        return False
    code, stack, pc, failed = decode(), [], 0, False
    while pc < len(code):
        op = code[pc]
        pc += 1
        if op in (0x31, 0x63, 0xE1):
            arg = code[pc]
            pc += 1
            if op == 0x31:
                stack.append(values[(arg * 13 + 7) & 31])
            elif op == 0x63:
                stack.append(arg)
            else:
                failed |= stack.pop() != arg
        else:
            right, left = stack.pop(), stack.pop()
            if op == 0xA7:
                value = left + right
            elif op == 0xD2:
                value = left ^ right
            elif op == 0x59:
                value = left * right
            elif op == 0xBC:
                value = rol(left, right)
            else:
                raise ValueError("Invalid instruction")
            stack.append(value & 255)
    return not failed and not stack

