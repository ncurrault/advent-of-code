from itertools import product, combinations
from tqdm import tqdm

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

def xform(pt, rotation=("+x", "+y"), translation=(0,0,0)):
    x, y, z = pt

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

    (delta_x, delta_y, delta_z) = translation
    return x + delta_x, y + delta_y, z + delta_z

def xform_group(pts, rotation=("+x", "+y"), translation=(0,0,0)):
    return (xform(pt, rotation=rotation, translation=translation) for pt in pts)

def neg(vector):
    return tuple(-d for d in vector)
def add(vec1, vec2):
    return tuple(a+b for a,b in zip(vec1, vec2))

def normalize(point_group):
    points = sorted(point_group)
    norm_translation = neg(points[0])
    return tuple(
        xform(pt, translation=norm_translation)
        for pt in points
    ), points[0]


def get_overlap_groups(beacons):
    overlap_groups = {}
    xs = sorted(x for x, y, z in beacons)
    ys = sorted(y for x, y, z in beacons)
    zs = sorted(z for x, y, z in beacons)
    for dirs in product((True, False), repeat=3):
        x_dir, y_dir, z_dir = dirs
        for extent_x in xs[:: -1 if x_dir else 1]:
            for extent_y in ys[:: -1 if y_dir else 1]:
                potential_overlap_group = set()
                remaining_beacons = set(beacons)
                for extent_z in zs[:: -1 if z_dir else 1]:
                    for x, y, z in remaining_beacons:
                        x_valid = x >= extent_x if x_dir else x <= extent_x
                        y_valid = y >= extent_y if y_dir else y <= extent_y
                        z_valid = z >= extent_z if z_dir else z <= extent_z
                        if x_valid and y_valid and z_valid:
                            potential_overlap_group.add((x, y, z))
                    remaining_beacons.difference_update(potential_overlap_group)
                    if len(potential_overlap_group) == 12:
                        norm_group, reverse_translation = normalize(potential_overlap_group)
                        overlap_groups[norm_group] = reverse_translation
                    elif len(potential_overlap_group) > 12:
                        break
    return overlap_groups

def yield_rotations():
    axis_rays = ["+x", "+y", "+z", "-x", "-y", "-z"]
    for plus_x in axis_rays:
        # minus_x = {"-":"+", "+": "-"}[plus_x_[0]] + plus_x_[1]
        plus_y_options = [ax for ax in axis_rays if ax[1] != plus_x[1]]
        assert len(plus_y_options) == 4
        for plus_y in plus_y_options:
            yield (plus_x, plus_y)

def get_overlap(target_groups, source_group):
    for rot in yield_rotations():
        source_norm, translate_to_source = normalize(xform(pt, rotation=rot) for pt in source_group)
        if source_norm not in target_groups.keys():
            continue
        translate_to_target = target_groups[source_norm]
        def xform_to_target(pt):
            pt = xform(pt, rotation=rot)
            pt = xform(pt, translation=neg(translate_to_source))
            pt = xform(pt, translation=translate_to_target)
            return pt
        return xform_to_target

overlap_groups_by_scanner = []
beacons_by_scanner = []

print("Loading potential overlap regions from scanners...")
for i, scanner_str in enumerate(tqdm(content.split("\n\n"))):
    beacons = []
    for beacon_pos_str in scanner_str.split("\n")[1:]:
        beacon = eval(f"({beacon_pos_str})")
        beacons.append(beacon)

    beacons_by_scanner.append(beacons)
    overlap_groups_by_scanner.append(get_overlap_groups(beacons))

scanners_remaining = set(range(1, len(beacons_by_scanner)))
base_frame_overlap_groups = overlap_groups_by_scanner[0]
scanner_locs = {(0, 0, 0)}

while len(scanners_remaining) > 0:
    print("computing overlaps... {} scanners remain".format(len(scanners_remaining)))
    to_remove = None
    for scanner_to_connect in scanners_remaining:
        for scanner_group in overlap_groups_by_scanner[scanner_to_connect].keys():
            # TODO may need to translate scanner_group to its native coords somewhere
            # TODO or maybe not?
            scanner_group_original = tuple(xform_group(scanner_group, translation=overlap_groups_by_scanner[scanner_to_connect][scanner_group]))
            xform_to_base = get_overlap(base_frame_overlap_groups, scanner_group_original)
            if xform_to_base is None:
                continue
            print(f"found overlap with scanner {scanner_to_connect}, merging...")
            to_remove = scanner_to_connect
            scanner_locs.add(xform_to_base((0,0,0)))
            for scanner_overlap_group, rev_translate in overlap_groups_by_scanner[scanner_to_connect].items():
                group_translated = xform_group(scanner_overlap_group, translation=rev_translate)
                mapped_group = map(xform_to_base, group_translated)
                mapped_group_norm, mapped_group_rev_trans = normalize(mapped_group)
                base_frame_overlap_groups[mapped_group_norm] = mapped_group_rev_trans
            print(f"successfully merged in data from scanner {scanner_to_connect}\n")

            break
        if to_remove is not None:
            break
    assert to_remove is not None
    scanners_remaining.remove(to_remove)

print("computing max Manhattan distance...")
max_manhattan = 0
for pt1, pt2 in combinations(scanner_locs, 2):
    curr_manhattan = 0
    for d in range(3):
        curr_manhattan += abs(pt1[d] - pt2[d])
    if curr_manhattan > max_manhattan:
        max_manhattan = curr_manhattan
print(max_manhattan)
