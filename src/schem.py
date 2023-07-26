import mcschematic

from util import is_bit_set


AIR = 'minecraft:air'
TORCH = 'minecraft:redstone_wall_torch[facing=north,lit=false]'
FRAMES = 26
SCREEN_SIZE = 32

class DisplayRomBuilder:
    rom: mcschematic.MCSchematic

    def __init__(self):
        # Does not throw an exception if file does not exist, silently loads air schematic
        self.rom = mcschematic.MCSchematic('schems/template_rom.schem')

    def save(self, filename: str) -> None:
        self.rom.save('../schems', filename, mcschematic.Version.JE_1_18_2)

    def write_byte(self, byte: int, address: int) -> None:
        if address > 31:
            raise Exception(f'Byte address is {address} but only 0-31 byte addresses are supported')

        z = -7

        if address > 0xF:
            z = -1

        x = (address & 0b1111) * 2
        y_offset = address % 2

        for i in range(8):
            if is_bit_set(byte, i):
                y = (i * 2 - 14) + y_offset
                self.rom.setBlock((x, y, z), AIR)

    def inspect(self):
        size = 200
        torches = 0
        min_x = 1000
        max_x = -1000
        min_y = 1000
        max_y = -1000
        min_z = 1000
        max_z = -1000

        for x in range(-size, 0):
            for y in range(0, size):
                for z in range(0, size):
                    block_data = self.rom.getBlockDataAt((x, y, z))
                    if block_data == TORCH:
                        torches += 1
                        if x < min_x:
                            min_x = x
                        if x > max_x:
                            max_x = x
                        if y < min_y:
                            min_y = y
                        if y > max_y:
                            max_y = y
                        if z < min_z:
                            min_z = z
                        if z > max_z:
                            max_z = z
                        print(x, y, z, block_data)

        print('torches num:', torches)
        print('min_x, max_x:', min_x, max_x)
        print('min_y, max_y:', min_y, max_y)
        print('min_z, max_z:', min_z, max_z)

        # for x in range(31):
        #     for y in reversed(range(-15, 2)):
        #         z = -7
        #         block_data = self.rom.getBlockDataAt((x, y, z))
        #         print(x, y, z, block_data)


def generate_schem(filepath: str):
    # file_handle = open(filepath, 'r')
    # file = file_handle.read()
    # bytes_str = file.strip().replace('\n', ' ').split(' ')
    # bytes_int = list(map(lambda x: int(x, 16), bytes_str))
    builder = DisplayRomBuilder()
    builder.inspect()
    # for i in range(len(bytes_int)):
    #     builder.write_byte(bytes_int[i], i)
    #
    # builder.save('modified')


if __name__ == '__main__':
    generate_schem('schems/input.txt')
