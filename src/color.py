from struct import pack

def write_color(file_name, pixel_color):
    x = int(pixel_color[0])
    y = int(pixel_color[1])
    z = int(pixel_color[2])

    with open(file_name, 'ab') as file:
        file.write(pack('=BBB', x, y, z))
        file.close()