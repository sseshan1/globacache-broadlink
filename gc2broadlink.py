import binascii
import struct
import math

def gc2lirc(gccmd):
    frequency = int(gccmd.split(",")[3])*1.0/1000000
    pulses = gccmd.split(",")[6:]
    return [int(round(int(code) / frequency)) for code in pulses]

def lirc2broadlink(pulses):
    array = bytearray()

    for pulse in pulses:
        pulse = math.floor(pulse * 269 / 8192)  # 32.84ms units

        if pulse < 256:
            array += bytearray(struct.pack('>B', pulse))  # big endian (1-byte)
        else:
            array += bytearray([0x00])  # indicate next number is 2-bytes
            array += bytearray(struct.pack('>H', pulse))  # big endian (2-bytes)

    packet = bytearray([0x26, 0x00])  # 0x26 = IR, 0x00 = no repeats
    packet += bytearray(struct.pack('<H', len(array)))  # little endian byte count
    packet += array
    packet += bytearray([0x0d, 0x05])  # IR terminator

    # Add 0s to make ultimate packet size a multiple of 16 for 128-bit AES encryption.
    remainder = (len(packet) + 4) % 16  # rm.send_data() adds 4-byte header (02 00 00 00)
    if remainder:
        packet += bytearray(16 - remainder)

    return packet

if __name__ == '__main__':
    import sys
    arguments = len(sys.argv) - 1
    if arguments  < 1:
        print("Usage "+sys.argv[0]+ " [filename_of_gc_codes] ")
        sys.exit(1)

    file = open(sys.argv[1], "r")
    for line in file:
        values=line.split('"')
        if len(values) > 2:
            commandname=values[1]
            command=values[3]
            pulses = gc2lirc(command)
            packet = lirc2broadlink(pulses)
            pcodes = [int(binascii.hexlify(packet[i:i+2]), 16) for i in range(0, len(packet), 2)]
            print(commandname.replace(' ', '_').replace('/','_').lower() +" "+ binascii.b2a_hex(packet).decode('utf-8'))
    sys.exit(0)
