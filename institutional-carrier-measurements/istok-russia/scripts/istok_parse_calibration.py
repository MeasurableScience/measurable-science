import cdflib
import numpy as np

FILE = "isee_induction_ist_2017032800_v01.cdf"

cdf = cdflib.CDF(FILE)

print("=" * 80)
print("GLOBAL ATTRIBUTES")
print("=" * 80)

g = cdf.globalattsget()

for k, v in g.items():
    print(f"{k}: {v}")


print("\n" + "=" * 80)
print("CDF VARIABLES")
print("=" * 80)

info = cdf.cdf_info()

try:
    variables = list(info.zVariables) + list(info.rVariables)
except Exception:
    variables = list(info["zVariables"]) + list(info["rVariables"])

for v in variables:
    print(v)


for var in [
    "db_dt",
    "epoch_db_dt",
    "frequency",
    "sensitivity",
    "phase_difference"
]:

    print("\n" + "=" * 80)
    print("VARIABLE:", var)
    print("=" * 80)

    try:
        attrs = cdf.varattsget(var)

        print("\nATTRIBUTES:")

        for k, v in attrs.items():
            print(f"  {k}: {v}")

    except Exception as e:
        print("Attribute error:", e)

    try:
        x = np.asarray(cdf.varget(var))

        print("\nDATA:")
        print("  shape:", x.shape)
        print("  dtype:", x.dtype)

        if np.issubdtype(x.dtype, np.number):

            finite = x[np.isfinite(x)]

            if finite.size:

                print("  min:", np.min(finite))
                print("  max:", np.max(finite))
                print("  mean:", np.mean(finite))
                print("  median:", np.median(finite))

        if var in [
            "frequency",
            "sensitivity",
            "phase_difference"
        ]:
            print("\nFULL ARRAY:")
            print(x)

    except Exception as e:
        print("Data error:", e)


print("\n" + "=" * 80)
print("CALIBRATION AROUND 6-9 Hz")
print("=" * 80)

f = np.asarray(
    cdf.varget("frequency"),
    dtype=float
)

s = np.asarray(
    cdf.varget("sensitivity"),
    dtype=float
)

p = np.asarray(
    cdf.varget("phase_difference"),
    dtype=float
)

for i, freq in enumerate(f):

    if 5.0 <= freq <= 10.0:

        print()
        print("Frequency:", freq, "Hz")
        print("Sensitivity:", s[i])
        print("Phase difference:", p[i])