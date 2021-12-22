from functools import reduce
from itertools import product
from collections import defaultdict

PRACTICE = False

with open("test2.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

# intersection of 1D closed intervals
def interval_intersection(min1, max1, min2, max2):
    assert min1 <= max1 and min2 <= max2
    if max1 < min2 or min1 > max2:
        return

    return max(min1, min2), min(max1, max2)


cube_str_format = """
- - - - - - - y={max_y}
| \\         | \\
|   \\       |   \\  y={min_y}
|     - - - - - - - z={max_z}
|     |     |     |
|     |     |     |
- - - | - - -     |
  \\   |       \\   |
    \\ |         \\ | z={min_z}
      - - - - - - -
     x={min_x:<5}      x={max_x}
"""[1:-1]

class Cuboid:
    def __init__(self, _x_bounds, _y_bounds, _z_bounds):
        assert _x_bounds and _y_bounds and _z_bounds
        self.x_bounds = _x_bounds
        self.y_bounds = _y_bounds
        self.z_bounds = _z_bounds

    def _key(self):
        return (self.x_bounds, self.y_bounds, self.z_bounds)

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        if not isinstance(other, Cuboid):
            return False
        return self._key() == other._key()

    def __str__(self):
        return cube_str_format.format(min_x=self.x_bounds[0], max_x=self.x_bounds[1],
            min_y=self.y_bounds[0], max_y=self.y_bounds[1], min_z=self.z_bounds[0], max_z=self.z_bounds[1])

    def intersection(self, other):
        x_bounds = interval_intersection(*self.x_bounds, *other.x_bounds)
        y_bounds = interval_intersection(*self.y_bounds, *other.y_bounds)
        z_bounds = interval_intersection(*self.z_bounds, *other.z_bounds)
        if x_bounds is None or y_bounds is None or z_bounds is None:
            return None
        return Cuboid(x_bounds, y_bounds, z_bounds)

    def contains(self, other):
        # thm: set is subset iff equal to intersection
        return other == self.intersection(other)

    def volume(self):
        edges = (b[1] - b[0] + 1 for b in (self.x_bounds, self.y_bounds, self.z_bounds))
        return reduce(lambda x, y: x * y, edges, 1)

    def fracture(self, sub_cuboid):
        res = [sub_cuboid]

        pos_x_bounds = (
            (sub_cuboid.x_bounds[1] + 1, self.x_bounds[1])
            if self.x_bounds[1] > sub_cuboid.x_bounds[1]
            else None
        )
        pos_y_bounds = (
            (sub_cuboid.y_bounds[1] + 1, self.y_bounds[1])
            if self.y_bounds[1] > sub_cuboid.y_bounds[1]
            else None
        )
        pos_z_bounds = (
            (sub_cuboid.z_bounds[1] + 1, self.z_bounds[1])
            if self.z_bounds[1] > sub_cuboid.z_bounds[1]
            else None
        )

        neg_x_bounds = (
            (self.x_bounds[0], sub_cuboid.x_bounds[0] - 1)
            if self.x_bounds[0] < sub_cuboid.x_bounds[0]
            else None
        )
        neg_y_bounds = (
            (self.y_bounds[0], sub_cuboid.y_bounds[0] - 1)
            if self.y_bounds[0] < sub_cuboid.y_bounds[0]
            else None
        )
        neg_z_bounds = (
            (self.z_bounds[0], sub_cuboid.z_bounds[0] - 1)
            if self.z_bounds[0] < sub_cuboid.z_bounds[0]
            else None
        )

        # faces
        if pos_x_bounds:
            res.append(Cuboid(pos_x_bounds, sub_cuboid.y_bounds, sub_cuboid.z_bounds))
        if pos_y_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, pos_y_bounds, sub_cuboid.z_bounds))
        if pos_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, sub_cuboid.y_bounds, pos_z_bounds))
        if neg_x_bounds:
            res.append(Cuboid(neg_x_bounds, sub_cuboid.y_bounds, sub_cuboid.z_bounds))
        if neg_y_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, neg_y_bounds, sub_cuboid.z_bounds))
        if neg_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, sub_cuboid.y_bounds, neg_z_bounds))

        # edges
        if pos_x_bounds and pos_y_bounds:
            res.append(Cuboid(pos_x_bounds, pos_y_bounds, sub_cuboid.z_bounds))
        if pos_x_bounds and neg_y_bounds:
            res.append(Cuboid(pos_x_bounds, neg_y_bounds, sub_cuboid.z_bounds))
        if neg_x_bounds and pos_y_bounds:
            res.append(Cuboid(neg_x_bounds, pos_y_bounds, sub_cuboid.z_bounds))
        if neg_x_bounds and neg_y_bounds:
            res.append(Cuboid(neg_x_bounds, neg_y_bounds, sub_cuboid.z_bounds))

        if pos_x_bounds and pos_z_bounds:
            res.append(Cuboid(pos_x_bounds, sub_cuboid.y_bounds, pos_z_bounds))
        if pos_x_bounds and neg_z_bounds:
            res.append(Cuboid(pos_x_bounds, sub_cuboid.y_bounds, neg_z_bounds))
        if neg_x_bounds and pos_z_bounds:
            res.append(Cuboid(neg_x_bounds, sub_cuboid.y_bounds, pos_z_bounds))
        if neg_x_bounds and neg_z_bounds:
            res.append(Cuboid(neg_x_bounds, sub_cuboid.y_bounds, neg_z_bounds))

        if pos_y_bounds and pos_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, pos_y_bounds, pos_z_bounds))
        if pos_y_bounds and neg_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, pos_y_bounds, neg_z_bounds))
        if neg_y_bounds and pos_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, neg_y_bounds, pos_z_bounds))
        if neg_y_bounds and neg_z_bounds:
            res.append(Cuboid(sub_cuboid.x_bounds, neg_y_bounds, neg_z_bounds))

        # corners
        if pos_x_bounds and pos_y_bounds and pos_z_bounds:
            res.append(Cuboid(pos_x_bounds, pos_y_bounds, pos_z_bounds))
        if pos_x_bounds and pos_y_bounds and neg_z_bounds:
            res.append(Cuboid(pos_x_bounds, pos_y_bounds, neg_z_bounds))
        if pos_x_bounds and neg_y_bounds and pos_z_bounds:
            res.append(Cuboid(pos_x_bounds, neg_y_bounds, pos_z_bounds))
        if pos_x_bounds and neg_y_bounds and neg_z_bounds:
            res.append(Cuboid(pos_x_bounds, neg_y_bounds, neg_z_bounds))
        if neg_x_bounds and pos_y_bounds and pos_z_bounds:
            res.append(Cuboid(neg_x_bounds, pos_y_bounds, pos_z_bounds))
        if neg_x_bounds and pos_y_bounds and neg_z_bounds:
            res.append(Cuboid(neg_x_bounds, pos_y_bounds, neg_z_bounds))
        if neg_x_bounds and neg_y_bounds and pos_z_bounds:
            res.append(Cuboid(neg_x_bounds, neg_y_bounds, pos_z_bounds))
        if neg_x_bounds and neg_y_bounds and neg_z_bounds:
            res.append(Cuboid(neg_x_bounds, neg_y_bounds, neg_z_bounds))

        for c in res:
            assert self.contains(c)
        return res


cuboids_on = set()

for line in content.split("\n"):
    state_str, cuboid = line.split(" ")
    state = state_str == "on"
    x_range, y_range, z_range = cuboid.split(",")

    min_x = int(x_range[2 : x_range.find("..")])
    max_x = int(x_range[x_range.find("..") + 2 :])

    min_y = int(y_range[2 : y_range.find("..")])
    max_y = int(y_range[y_range.find("..") + 2 :])

    min_z = int(z_range[2 : z_range.find("..")])
    max_z = int(z_range[z_range.find("..") + 2 :])

    cuboid = Cuboid((min_x, max_x), (min_y, max_y), (min_z, max_z))

    # a simplification: any subsets will be irrelevant to the result
    to_remove = set()
    for c in cuboids_on:
        if cuboid.contains(c):
            to_remove.add(c)
    cuboids_on.difference_update(to_remove)

    if state:
        to_add = {cuboid}
        problematic_cuboids = {
            other_cuboid
            for other_cuboid in cuboids_on
            if cuboid.intersection(other_cuboid)
        }
        while True:
            problematic_additions = {}
            for addition in to_add:
                for existing in problematic_cuboids:
                    isect = addition.intersection(existing)
                    if isect:
                        problematic_additions[addition] = isect
                        break
            if len(problematic_additions) == 0:
                break
            for addition, isect in problematic_additions.items():
                to_add.remove(addition)
                for replacement_addition in addition.fracture(isect):
                    for existing in problematic_cuboids:
                        if existing.contains(replacement_addition):
                            break
                    else:
                        to_add.add(replacement_addition)
        cuboids_on.update(to_add)
    else:
        adjusted_cuboids = {
            other_cuboid
            for other_cuboid in cuboids_on
            if cuboid.intersection(other_cuboid)
        }
        cuboids_on.difference_update(adjusted_cuboids)

        while True:
            overlapping_cuboids = {
                other_cuboid: cuboid.intersection(other_cuboid)
                for other_cuboid in adjusted_cuboids
                if cuboid.intersection(other_cuboid)
            }
            if len(overlapping_cuboids) == 0:
                break
            for overlapping_cuboid, isect in overlapping_cuboids.items():
                adjusted_cuboids.remove(overlapping_cuboid)
                for replacement in overlapping_cuboid.fracture(isect):
                    if not cuboid.contains(replacement):
                        adjusted_cuboids.add(replacement)
        cuboids_on.update(adjusted_cuboids)

res = 0
for c in cuboids_on:
    res += c.volume()
print(res)
