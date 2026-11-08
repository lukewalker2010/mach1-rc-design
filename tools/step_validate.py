"""Import-check the committed STEP files (AGENTS.md §4 quality gate).

Verifies that every authoritative solid loads, is a single connected solid,
contains no zero-volume debris and occupies the intended Z extent. Uses the
OpenCascade (OCP) bindings that ship with CadQuery; if OCP is not installed
the check is skipped (exit 0) so the standard-library analysis CI is not
coupled to the CAD environment.

Run:  python3 tools/step_validate.py [--json]
Exit: 0 all checks pass or OCP unavailable (SKIP);
      1 a solid failed; 2 missing file / unexpected error.
"""
import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOL = 0.75  # mm, bounding-box tolerance

# filename, expected solid count, expected zmin, expected zmax
EXPECTED = [
    ("ab_transition.step", 1, 0.0, 100.0),
    ("ab_spray_ring.step", 1, 0.0, 15.0),
    ("ab_flameholder.step", 1, 0.0, 35.0),
    ("ab_liner.step", 1, 0.0, 200.0),
    ("ab_iris_nozzle.step", 1, 0.0, 35.0),
    ("ab_assembly.step", 1, 0.0, 385.0),
]


@dataclass(frozen=True)
class Result:
    file: str
    passed: bool
    detail: str


def _ocp():
    try:
        from OCP.Bnd import Bnd_Box
        from OCP.BRepBndLib import BRepBndLib
        from OCP.BRepGProp import BRepGProp
        from OCP.GProp import GProp_GProps
        from OCP.IFSelect import IFSelect_RetDone
        from OCP.STEPControl import STEPControl_Reader
        from OCP.TopAbs import TopAbs_SOLID
        from OCP.TopExp import TopExp_Explorer
    except Exception:
        return None
    return {
        "Bnd_Box": Bnd_Box,
        "BRepBndLib": BRepBndLib,
        "BRepGProp": BRepGProp,
        "GProp_GProps": GProp_GProps,
        "IFSelect_RetDone": IFSelect_RetDone,
        "STEPControl_Reader": STEPControl_Reader,
        "TopAbs_SOLID": TopAbs_SOLID,
        "TopExp_Explorer": TopExp_Explorer,
    }


def inspect(path, ocp):
    reader = ocp["STEPControl_Reader"]()
    status = reader.ReadFile(str(path))
    if status != ocp["IFSelect_RetDone"]:
        raise RuntimeError(f"read failed (status {status})")
    reader.TransferRoots()
    shape = reader.OneShape()

    explorer = ocp["TopExp_Explorer"](shape, ocp["TopAbs_SOLID"])
    solids = 0
    zero_volume = 0
    while explorer.More():
        props = ocp["GProp_GProps"]()
        ocp["BRepGProp"].VolumeProperties_s(explorer.Current(), props)
        if props.Mass() <= 1e-6:
            zero_volume += 1
        solids += 1
        explorer.Next()

    box = ocp["Bnd_Box"]()
    ocp["BRepBndLib"].Add_s(shape, box)
    zmin = box.CornerMin().Z()
    zmax = box.CornerMax().Z()
    return {"solids": solids, "zero_volume": zero_volume, "zmin": zmin, "zmax": zmax}


def validate(names=None):
    ocp = _ocp()
    if ocp is None:
        return None
    results = []
    for filename, expected_solids, zmin, zmax in EXPECTED:
        if names and filename not in names:
            continue
        path = ROOT / filename
        if not path.exists():
            results.append(Result(filename, False, "missing file"))
            continue
        try:
            info = inspect(path, ocp)
        except Exception as exc:  # pragma: no cover - defensive
            results.append(Result(filename, False, f"import error: {exc}"))
            continue
        problems = []
        if info["solids"] != expected_solids:
            problems.append(f"solids {info['solids']} != {expected_solids}")
        if info["zero_volume"]:
            problems.append(f"{info['zero_volume']} zero-volume solid(s)")
        if abs(info["zmin"] - zmin) > TOL or abs(info["zmax"] - zmax) > TOL:
            problems.append(
                "z extent {:.1f}..{:.1f} != {:.1f}..{:.1f}".format(
                    info["zmin"], info["zmax"], zmin, zmax
                )
            )
        detail = (
            f"solids={info['solids']} zero={info['zero_volume']} "
            f"z={info['zmin']:.1f}..{info['zmax']:.1f}"
        )
        if problems:
            detail += " | " + "; ".join(problems)
        results.append(Result(filename, not problems, detail))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    results = validate()
    if results is None:
        print("SKIP: OpenCascade (OCP) not available; STEP import check not run.")
        return 0

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        for r in results:
            print(f"{'PASS' if r.passed else 'FAIL'} {r.file:22s} {r.detail}")
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
