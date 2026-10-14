#!/usr/bin/env python3
"""Replay the Lutetia recipe into package/ and package-with-errors/, and stamp the platform.

    python scripts/replay.py                       # both variants, with `energyml` from PATH
    python scripts/replay.py --energyml PATH       # another CLI binary
    python scripts/replay.py --plan                # the quote of each variant, nothing written
    python scripts/replay.py --redraw              # draw the stored section again first (CLI with hdf5,png)

What it does, in this order:

1. checks that the BSS inputs are there (recipe/donnees/bss/, kept in the
   repository: see docs/build.md);
2. plays `recipe/recette.toml` with the `energyml` CLI into a staging folder
   (`replay/`, ignored by git): the clean model (`--without erreur`) and the
   variant with deliberate errors (the whole recipe);
3. only if both succeeded, moves the four files into `package/` and
   `package-with-errors/` and writes `written-on`.

Nothing is renamed by hand: the EPC names its HDF5 file after the recipe's
`donnees` key, so a different file name is obtained by playing the recipe again
with another `--out`, or with `energyml rename`, never by renaming files.

`written-on` records where the files were written, because the platform's maths
library decides whether a replay elsewhere can be compared byte for byte or only
up to float noise. Two lines, spelled as node's `process.platform` and
`process.arch`:

    linux
    arch: x64

The CLI should be the version in `recipe/energyml-version`, built with HDF5.

Needs Python 3.8+ and the standard library only. Exit 0 on success, non-zero
with a message on any failure; nothing under package*/ is touched on failure.
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPE = ROOT / "recipe" / "recette.toml"
STAGING = ROOT / "replay"

# (folder, extra CLI arguments). The two variants share their file names: the
# recipe writes `Lutetia.h5` and the EPC refers to it by that name.
VARIANTS = [
    ("package", ["--without", "erreur"]),
    ("package-with-errors", []),
]
EPC = "Lutetia.epc"
H5 = "Lutetia.h5"

# Inputs the recipe reads that the repository does not hold (docs/build.md).
FETCHED = [
    "recipe/donnees/bss/forages.geojson",
    "recipe/donnees/bss/passes-etages.csv",
]


# --redraw. The stored drawing names, by full uri, the objects it was computed
# from, so it goes stale whenever a recipe edit moves uuids. The CLI could draw
# again from the SVG's own metadata (`profile --from-svg`), but that looks up
# the very uris that moved, so it cannot help here: the profile options are
# hard-coded instead. THEY MUST MATCH THE STORED DRAWING (the SVG metadata holds
# the track, widths, crosses, size and markers it was computed with) and the
# command in recipe/README.md; change them together.
STORED = ROOT / "recipe" / "donnees" / "profils" / "coupe-lutetia.svg"
PROFILE_ARGS = [
    "--track", "650700,6861450;651250,6861750;651850,6861350",
    "--left", "200", "--right", "150",
    "--cross-count", "3", "--cross-length", "300", "--cross-width", "100",
    "--draw", "long", "--size", "1400x700", "--labels", "full",
    "--marker", "Forages BSS:shape=diamond,colour=#1565c0,at=bottom,type=WellboreTrajectory,title=BSS",
]
PNG_SCALE = "1.5"
AWAITED = "redrawn from the package played without it"
MEMBER_LINE = '{ creneau = "members", etape = "coupe" },'


def node_platform() -> str:
    """This platform, spelled as node's `process.platform`."""
    # Python and node agree on win32, linux and darwin; an old Python wrote
    # linux2 and freebsd13, which node never spells.
    if sys.platform in ("win32", "darwin"):
        return sys.platform
    return sys.platform.rstrip("0123456789")


def node_arch() -> str:
    """This architecture, spelled as node's `process.arch`."""
    machine = platform.machine().lower()
    return {"amd64": "x64", "x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}.get(machine, machine)


def fail(message: str):
    sys.exit(f"replay: {message}")


def run(command: list) -> None:
    print("+", " ".join(str(part) for part in command), flush=True)
    try:
        done = subprocess.run(command, cwd=ROOT)
    except FileNotFoundError:
        fail(f"cannot run {command[0]!r}: install the energyml CLI (version in recipe/energyml-version, built with --features hdf5) or pass --energyml PATH")
    if done.returncode != 0:
        fail(f"{' '.join(str(part) for part in command[:3])} ... exited with status {done.returncode}")


def without_coupe(text: str) -> str:
    """The recipe text with the `coupe` step marked as awaited and left out of the project."""
    lines = text.splitlines(keepends=True)
    out = []
    marked = 0
    dropped = 0
    after_name = False
    for line in lines:
        stripped = line.strip()
        if stripped == MEMBER_LINE:
            dropped += 1
            continue
        out.append(line)
        if after_name and stripped == 'operation = "section-view"':
            out.append(f'attente = "{AWAITED}"\n')
            marked += 1
        after_name = stripped == 'nom = "coupe"'
    if marked != 1 or dropped != 1:
        fail(
            f"--redraw: expected one `coupe` step with operation = \"section-view\" and one member line "
            f"`{MEMBER_LINE}` in {RECIPE.name}, found {marked} and {dropped}: the recipe changed shape, update without_coupe()"
        )
    return "".join(out)


def redraw(energyml: str) -> None:
    """Draw the stored section again from the package played without it (defect n.102).

    1. a temporary copy of the recipe, next to the real one so that its relative
       paths resolve, with the `coupe` step awaited and out of the project;
    2. that copy played (`--without erreur`) into the staging folder;
    3. `energyml profile` on that package, into the staging folder, then moved
       over recipe/donnees/profils/coupe-lutetia.{svg,png}.
    The normal replay follows, and finds a drawing that names objects it holds.
    """
    if STAGING.exists():
        shutil.rmtree(STAGING)
    drawn = STAGING / "redraw"
    drawn.mkdir(parents=True)
    copy = RECIPE.with_name(".redraw-" + RECIPE.name)
    try:
        try:
            copy.write_text(without_coupe(RECIPE.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        except OSError as why:
            fail(f"--redraw: cannot make the temporary copy {copy}: {why}")
        epc = drawn / EPC
        run([energyml, "create", "--recipe", str(copy), "--without", "erreur", "--out", str(epc)])
        if not epc.is_file():
            fail(f"--redraw: the package played without the section was not written ({epc})")
        svg, png = drawn / "coupe-lutetia.svg", drawn / "coupe-lutetia.png"
        command = [energyml, "profile", str(epc), *PROFILE_ARGS, "--svg", str(svg), "--png", str(png), "--png-scale", PNG_SCALE]
        print("+", " ".join(str(part) for part in command), flush=True)
        done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        sys.stdout.write(done.stdout)
        sys.stderr.write(done.stderr)
        if done.returncode != 0:
            if "png" in (done.stdout + done.stderr).lower():
                fail("--redraw: the CLI refused the PNG: it must be built with --features hdf5,png")
            fail(f"--redraw: `energyml profile` exited with status {done.returncode}")
        for name, made in (("svg", svg), ("png", png)):
            if not made.is_file():
                fail(f"--redraw: no .{name} was written (is the CLI built with --features png?)")
            shutil.move(str(made), str(STORED.with_suffix("." + name)))
    finally:
        # Always: a stray recipe next to the real one would be taken for part of it.
        try:
            copy.unlink()
        except FileNotFoundError:
            pass
        shutil.rmtree(STAGING, ignore_errors=True)
    print(f"replay: redrew {STORED.with_suffix('.svg').relative_to(ROOT)} and .png", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--energyml", default="energyml", help="the CLI to play the recipe with (default: energyml from PATH)")
    parser.add_argument("--plan", action="store_true", help="print the quote of each variant; write nothing")
    parser.add_argument(
        "--redraw",
        action="store_true",
        help="first draw the stored section (recipe/donnees/profils/coupe-lutetia.svg and .png) again from the package "
        "played without it, then replay; needs a CLI built with hdf5 and png",
    )
    args = parser.parse_args()
    if args.redraw and args.plan:
        fail("--redraw writes the stored drawing: it cannot be combined with --plan")

    if not RECIPE.is_file():
        fail(f"{RECIPE} not found: run this script from a checkout of energyml-lutetia")
    missing = [name for name in FETCHED if not (ROOT / name).is_file()]
    if missing and not args.plan:
        fail(
            "missing inputs: "
            + ", ".join(missing)
            + " - they are kept in the repository (docs/build.md, section 'The BSS inputs are in this repository')"
        )

    version_file = ROOT / "recipe" / "energyml-version"
    if version_file.is_file():
        wanted = version_file.read_text(encoding="utf-8").splitlines()[0].strip()
        print(f"replay: recipe/energyml-version asks for energyml {wanted}", flush=True)
        try:
            ours = subprocess.run([args.energyml, "--version"], capture_output=True, text=True, cwd=ROOT)
            if wanted not in ours.stdout:
                print(f"replay: warning: `{args.energyml} --version` says {ours.stdout.strip()!r}, not {wanted}", file=sys.stderr)
        except FileNotFoundError:
            pass  # reported by run() below with the full message

    if args.plan:
        for folder, extra in VARIANTS:
            print(f"== {folder}", flush=True)
            run([args.energyml, "create", "--recipe", str(RECIPE), "--plan", *extra])
        return 0

    if args.redraw:
        redraw(args.energyml)

    if STAGING.exists():
        shutil.rmtree(STAGING)
    for folder, extra in VARIANTS:
        (STAGING / folder).mkdir(parents=True)
        run([args.energyml, "create", "--recipe", str(RECIPE), *extra, "--out", str(STAGING / folder / EPC)])
        for name in (EPC, H5):
            if not (STAGING / folder / name).is_file():
                fail(f"the replay of {folder} did not write {name} (is the CLI built with --features hdf5?)")

    # Both variants played: only now is anything replaced.
    for folder, _ in VARIANTS:
        (ROOT / folder).mkdir(exist_ok=True)
        for name in (EPC, H5):
            shutil.move(str(STAGING / folder / name), str(ROOT / folder / name))
    shutil.rmtree(STAGING, ignore_errors=True)

    (ROOT / "written-on").write_text(f"{node_platform()}\narch: {node_arch()}\n", encoding="utf-8", newline="\n")
    print(f"replay: wrote package/, package-with-errors/ and written-on ({node_platform()}, {node_arch()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
