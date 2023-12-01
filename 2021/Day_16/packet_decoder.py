
def literal_value(packet, index, return_num = False):
    bits = ''
    # Take 5 bits at a time till the end where the current bits first bit is 0
    current_bits = packet[index : index + 5]
    while True:
        # Add the current bits
        bits = bits + current_bits[1:]
        # Goto new index
        index += 5
        # Store new bits
        current_bits = packet[index: index + 5]
        if current_bits[0] == '0':
            bits = bits + current_bits[1:]
            #print("Integer: {}, Binary: {}".format(int(bits, base = 2), bits))
            if return_num:
                return index + 5, int(bits, 2)
            return index + 5

def process_packet(packet, index):
    version = int(packet[index : index + 3], base = 2)
    type_id = int(packet[index + 3 : index + 6], base = 2)
    func_index = index + 6
    if type_id == 4:
        # print("Doing Literal Value version 4")
        return literal_value(packet, func_index), version
    else:
        # Get the length id
        length_id = packet[func_index]
        func_index += 1
        # Do things based on length ID
        if length_id == '0':
            # print("Doing Total Length Operator length id 0")
            length = int(packet[func_index : func_index + 15], base = 2)
            func_index += length + 15
            return func_index, version
        elif length_id == '1':
            # print("Doing Sub packets operator length id 1")
            num_subs = int(packet[func_index : func_index + 11], base = 2)
            # print(num_subs)
            func_index += 11
            for i in range(num_subs):
                _, version_To_add = process_packet(packet, func_index)
                version += version_To_add
                func_index += 11
            return func_index, version



def decode(file):
    """
    We receive a hexadecimal message. We then convert
    the message to binary, as our rules are in binary.

    The first three bits are the packet version
    The next three bits are the packet typeID
    Depending on the typeID

    * If the type ID gives a 4 (i.e. 100) then do a
    loop of taking 5 bits, each five bits starts with a 1
    except the last group of bits which starts with a 0.

    If the type ID is not 4, then its an operator packet which
    contains one or more packets. After the packet header, there is
    a length type ID that is 0 or 1.

    * If the length type ID is 0, Then the next 15 bits are a number
    that represents the total length in bits of the sub-packets
    contained by this packet

    * The length type ID is 1, Then the next 11 bits are a number that
    represents the number of sub-packets immediately contained by this
    packet.



    Parameters
    ----------
    file : [type]
        [description]
    """
    input = open(file, 'r').read().strip()
    # Convert hex string to integer then convert integer to binary
    binary_string = str(bin(int(input, base = 16)))[2:].zfill(len(input) * 4)
    string_index = 0
    while string_index <= (len(binary_string) - 12):
        string_index, version_sum = process_packet(binary_string, string_index)
    return version_sum
    
if __name__ == '__main__':
    # Tests for first part
    print("Version Sum: {}".format(decode('test_1.txt')))
    print("Version Sum: {}".format(decode('test_2.txt')))
    print("Version Sum: {}".format(decode('test_3.txt')))
    print("Version Sum: {}".format(decode('test_4.txt')))
    print("Version Sum: {}".format(decode('test_5.txt')))
    print("Version Sum: {}".format(decode('test_6.txt')))
    print("Version Sum: {}".format(decode('test_7.txt')))
