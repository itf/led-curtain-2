import array
width = 15
height = 5

id_grid = [[292, 418, 328, 256, 625],
           [529, 601, 592, 493, 319],
           [445, 388, 697, 655, 682],
           [709, 337, 718, 472, 346],
           [None, 301, 745, 277, None]]
id_map = {}
for x in range(width):
    for y in range(height):
        grid_value = id_grid[y][x / 3]
        if grid_value != None:
            id_map[x, y] = grid_value - 256 + (x % 3) * 3

def array_to_bytes(byte_array):
    return array.array('B', byte_array).tostring()

packet_header_array = [0x04, 0x01, 0xdc, 0x4a, 0x01, 0x00, 0x01, 0x01,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0xff, 0xff, 0xff, 0xff, 0x00]
packet_header = array_to_bytes(packet_header_array)


def canvasToData(canvas):
        array = [0x00] * 512
        for x in range(width):
            for y in range(height):
                if (x, y) in id_map:
                    colors = [int(min(max(0, color), 1) * 255) for color in canvas[y, x]]
                    index = id_map[x, y]
                    array[index:index+3] = colors
        return packet_header + array_to_bytes(array)
                    

 
