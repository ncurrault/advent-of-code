from itertools import product
from tqdm import tqdm
from functools import cache

PRACTICE = True

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

def overlaps(a, b):
    # TODO rethink entire xform logic to yield 24 options based on how we orient
    # +x axis (6 options)
    # +y axiis (4 options, it can't align with the chosen x)
    axis_rays = ["+x", "+y", "+z", "-x", "-y", "-z"]
    for plus_x in axis_rays:
        # minus_x = {"-":"+", "+": "-"}[plus_x_[0]] + plus_x_[1]
        plus_y_options = [ax for ax in axis_rays if ax[1] != plus_x[1]]
        assert len(plus_y_options) == 4
        for plus_y in plus_y_options:
            # minus_y = {"-":"+", "+": "-"}[plus_y[0]] + plus_y[1]
            a_pts = sorted(a)
            encoded_xform = (plus_x, plus_y), (0, 0, 0)
            b_pts = sorted(xform(encoded_xform, pt) for pt in b)
            delta_x, delta_y, delta_z = tuple(b_pts[0][i] - a_pts[0][i] for i in range(3))
            for a_pt, b_pt in zip(a_pts, b_pts):
                if a_pt[0] + delta_x != b_pt[0]:
                    break
                elif a_pt[1] + delta_y != b_pt[1]:
                    break
                elif a_pt[2] + delta_z != b_pt[2]:
                    break
            else:
                return (plus_x, plus_y), (delta_x, delta_y, delta_z)

def xform(overlap_result, pt):
    rotation, (delta_x, delta_y, delta_z) = overlap_result

    x, y, z = pt
    # plus_z = cross_product(plus_x, plus_y)

    match rotation:
        case ("+x", "+y"):
            x, y, z = x, y, z
        case ("+x", "+z"):
            x, y, z = x, z, -y
        case ("+x", "-y"):
            x, y, z = x, -y, -z
        case ("+x", "-z"):
            x, y, z = x, -z, y
        case ("+y", "+x"):
            x, y, z = y, x, -z
        case ("+y", "+z"):
            x, y, z = y, z, x
        case ("+y", "-x"):
            x, y, z = y, -x, z
        case ("+y", "-z"):
            x, y, z = y, -z, -x
        case ("+z", "+x"):
            x, y, z = z, x, y
        case ("+z", "+y"):
            x, y, z = z, y, -x
        case ("+z", "-x"):
            x, y, z = z, -x, -y
        case ("+z", "-y"):
            x, y, z = z, -y, x
        case ("-x", "+y"):
            x, y, z = -x, y, -z
        case ("-x", "+z"):
            x, y, z = -x, z, y
        case ("-x", "-y"):
            x, y, z = -x, -y, z
        case ("-x", "-z"):
            x, y, z = -x, -z, -y
        case ("-y", "+x"):
            x, y, z = -y, x, z
        case ("-y", "+z"):
            x, y, z = -y, z, -x
        case ("-y", "-x"):
            x, y, z = -y, -x, -z
        case ("-y", "-z"):
            x, y, z = -y, -z, x
        case ("-z", "+x"):
            x, y, z = -z, x, -y
        case ("-z", "+y"):
            x, y, z = -z, y, x
        case ("-z", "-x"):
            x, y, z = -z, -x, y
        case ("-z", "-y"):
            x, y, z = -z, -y, -x

    return x - delta_x, y - delta_y, z - delta_z

def get_overlap_groups(beacons):
    overlap_groups = set()
    xs = sorted(x for x, y, z in beacons)
    ys = sorted(y for x, y, z in beacons)
    zs = sorted(z for x, y, z in beacons)
    for dirs in product((True, False), repeat=3):
        x_dir, y_dir, z_dir = dirs
        for extent_x in xs[::-1 if x_dir else 1]:
            for extent_y in ys[::-1 if y_dir else 1]:
                potential_overlap_group = set()
                remaining_beacons = set(beacons)
                for extent_z in zs[::-1 if z_dir else 1]:
                    for x, y, z in remaining_beacons:
                        x_valid = x >= extent_x if x_dir else x <= extent_x
                        y_valid = y >= extent_y if y_dir else y <= extent_y
                        z_valid = z >= extent_z if z_dir else z <= extent_z
                        if x_valid and y_valid and z_valid:
                            potential_overlap_group.add((x, y, z))
                    remaining_beacons.difference_update(potential_overlap_group)
                    if len(potential_overlap_group) == 12:
                        # overlap_groups.add((tuple(sorted(potential_overlap_group)), dirs))
                        overlap_groups.add(tuple(sorted(potential_overlap_group)))
                    elif len(potential_overlap_group) > 12:
                        break
    return overlap_groups

result = set()
overlap_groups_by_scanner = []
beacons_by_scanner = []

# TODO efficiency gain by normalizing overlap sets (min point is always 0,0) and checking
# membership of each rotation in the set in O(1) time

for i, scanner_str in enumerate(content.split("\n\n")):
    beacons = []
    for beacon_pos_str in scanner_str.split("\n")[1:]:
        beacon = eval(f"({beacon_pos_str})")
        beacons.append(beacon)

    if i == 0:
        result.update(beacons)
    beacons_by_scanner.append(beacons)
    overlap_groups_by_scanner.append(get_overlap_groups(beacons))

overlap_groups = overlap_groups_by_scanner[0]
isolated_scanners = set(range(1, len(overlap_groups_by_scanner)))

while len(isolated_scanners) > 0:
    print("computing overlaps... {} scanners remain".format(len(isolated_scanners)))
    for base_overlap in tqdm(overlap_groups):
        for new_scanner in isolated_scanners:
            for new_overlap in overlap_groups_by_scanner[new_scanner]:
                res = overlaps(base_overlap, new_overlap)
                if res:
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        print(isolated_scanners)
        raise Exception("no overlap found")

    print(f"found overlap with scanner {new_scanner}, merging...")
    isolated_scanners.remove(new_scanner)
    for beacon in beacons_by_scanner[new_scanner]:
        result.add(xform(res, beacon))
    for new_overlap in overlap_groups_by_scanner[new_scanner]:
        mapped_overlap = set()
        for pt in new_overlap:
            mapped_overlap.add(xform(res, pt))
        overlap_groups.add(tuple(sorted(mapped_overlap)))
    print(f"successfully merged in data from scanner {new_scanner}")

print(len(result))
