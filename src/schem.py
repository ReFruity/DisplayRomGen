import mcschematic

AIR = 'minecraft:air'
TORCH = 'minecraft:redstone_wall_torch[facing=north,lit=false]'
FRAMES = 26
SCREEN_SIZE = 32
PIXEL_ADDRESSES = SCREEN_SIZE * SCREEN_SIZE * FRAMES

class DisplayRomBuilder:
    rom: mcschematic.MCSchematic

    def __init__(self):
        # Does not throw an exception if file does not exist, silently loads air schematic
        self.rom = mcschematic.MCSchematic('schems/template_rom.schem')

    def save(self, filename: str) -> None:
        self.rom.save('schems', filename, mcschematic.Version.JE_1_18_2)

    def write_pixel(self, frame: int, x: int, y: int, value: bool) -> None:
        if frame >= FRAMES:
            raise Exception(f'Frame is {frame} but only 0-{FRAMES - 1} frames are supported')

        if x >= SCREEN_SIZE or y >= SCREEN_SIZE:
            raise Exception(f'(x,y) is ({x},{y}) but only 0-{SCREEN_SIZE} coordinates are supported')

        # Z is frames axis
        first_frame_z = 2
        last_frame_z = 52
        rom_z = frame * 2 + first_frame_z
        rom_x = -x * 2 - 2
        rom_y = y * 4 + 1

        if value:
            self.rom.setBlock((rom_x, rom_y, rom_z), TORCH)
        else:
            self.rom.setBlock((rom_x, rom_y, rom_z), AIR)

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


def generate_schem(filepath: str):
    builder = DisplayRomBuilder()
    # builder.inspect()
    for frame in range(FRAMES):
        for x in range(SCREEN_SIZE):
            for y in range(SCREEN_SIZE):
                if x > frame or y > frame:
                    builder.write_pixel(frame=frame, x=x, y=y, value=False)

    builder.save('modified')


if __name__ == '__main__':
    generate_schem('schems/input.txt')
