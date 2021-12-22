import numpy as np

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

def bound(val):
    if val < -50:
        return -50
    elif val > 50:
        return 50
    else:
        return val

reactor = np.zeros((101, 101, 101), dtype=bool)
for line in content.split("\n"):
    state, cuboid = line.split(" ")
    x_range, y_range, z_range = cuboid.split(",")

    min_x = int(x_range[2:x_range.find("..")])
    max_x = int(x_range[x_range.find("..")+2:])
    if (min_x < -50 and max_x < -50) or (min_x > 50 and max_x > 50):
        continue

    min_y = int(y_range[2:y_range.find("..")])
    max_y = int(y_range[y_range.find("..")+2:])
    if (min_y < -50 and max_y < -50) or (min_y > 50 and max_y > 50):
        continue

    min_z = int(z_range[2:z_range.find("..")])
    max_z = int(z_range[z_range.find("..")+2:])
    if (min_z < -50 and max_z < -50) or (min_z > 50 and max_z > 50):
        continue

    min_x = bound(min_x) + 50
    max_x = bound(max_x) + 50
    min_y = bound(min_y) + 50
    max_y = bound(max_y) + 50
    min_z = bound(min_z) + 50
    max_z = bound(max_z) + 50

    reactor[min_x:max_x+1, min_y:max_y+1, min_z:max_z+1] = (state == "on")

print( np.count_nonzero(reactor) )
