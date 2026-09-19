import numpy as np
import pymagglobal

model = pymagglobal.Model("gufm1")

print("GUFM1 loaded")
print("t_min =", model.t_min)
print("t_max =", model.t_max)
print("l_max =", model.l_max)

# Test point:
# latitude 17 N
# longitude 30 W
# year 1700
#
# pymagglobal grid:
# row 0 = colatitude = 90 - latitude
# row 1 = longitude
# row 2 = radius km
# row 3 = year

grid = np.array([
    [90.0 - 17.0],
    [-30.0],
    [6371.2],
    [1700.0]
])

north, east, down = pymagglobal.field(
    grid,
    model,
    field_type="nez",
    inp_gd=False,
    out_gd=False
)

D = np.degrees(np.arctan2(east, north))

print()
print("TEST: 17 N, 30 W, year 1700")
print("North =", north[0], "nT")
print("East  =", east[0], "nT")
print("Down  =", down[0], "nT")
print("D     =", D[0], "degrees")