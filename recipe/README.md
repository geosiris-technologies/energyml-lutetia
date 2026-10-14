# Lutetia - the recipe of the model

Lutetia is the synthetic model of the Paris Basin around the Louvre. This folder
does not hold the package: it holds **what builds it** - the recipe, and the
versioned data the recipe reads. In the `energyml-lutetia` repository this
folder is `recipe/`, and the packages it builds are `package/` and
`package-with-errors/`.

```bash
energyml create --recipe recipe/recette.toml --plan              # the quote: every step, nothing written
energyml create --recipe recipe/recette.toml --out Lutetia.epc   # the package, with Lutetia.h5 next to it
```

The `energyml` CLI must be built with HDF5 (`--features hdf5`): the steps that
write arrays (the boundary, the boreholes, the surfaces) need it, and without it
the first of them stops and says so. `scripts/replay.py` of `energyml-lutetia`
plays both variants and writes the platform stamp.

## The rule

**To correct the model, edit `recette.toml` and replay.** Same inputs, same
package: the creation instant and the author are written in the recipe, every
uuid is derived from the content, so a diff between two packages says what
changed. Nothing is written by hand into the package, and a step is not
commented out to remove it: it carries `attente = "why"`, and the report shows
it on hold with its reason.

The format of the recipe is described in the CLI guide of `energyml`
(section *`create --recipe`*). The executor is `crates/energyml-build/src/recipe.rs`
of that repository. The keys of the recipe (`etape`, `titre`, `nom`, `operation`,
`attente`…) are French words read by the parser; the comments are in English.
A step may also carry `sert`, a free-text list of what it serves, recopied into
the workflow template; this recipe leaves it empty.

## What the recipe does

The steps are played in order into one package; the file lists them in sections
(reference frames, boundary and column, BSS boreholes, contacts and surfaces,
the grid, the geothermal doublet, WITSML and PRODML objects, faults, collections,
attachments and colours, and the deliberate-error group). A step on hold is
checked and reported but not played. Steps that take what a step on hold writes
must be on hold too - the recipe refuses otherwise. To lift a hold, remove the
`attente` line of the step and of the steps that depend on it.

What is still missing is said at the end of the recipe (for instance two
horizons that are contacts at a rank of the column, one horizon in depth, and
time series).

## The data

`donnees/bss/` - the boreholes and their intervals, prepared for this recipe;
its `README.md` says where each value comes from, what is to be reviewed, and
the licences (BSS: Licence Ouverte 2.0; GeolTs: CC BY 4.0). The public
Lutetia repository carries what the recipe reads: `forages.geojson`, the 23
boreholes as the BRGM API returned them (the API answers differently today, so a
replay needs this copy), and `passes-etages.csv`, the stage of each interval,
prepared by hand from the validated logs and the record sheets, which no API
returns. The harvested sheets and log images under `moisson/` are not republished.

`donnees/emprise.geojson` - the area of the model, **written for this recipe**:

- the four corners, in WGS 84 with six decimals (RFC 7946: a GeoJSON is in
  WGS 84), in the order SW, SE, NE, NW - the exterior ring runs
  counter-clockwise, as RFC 7946 §3.1.6 requires. Reprojected to Lambert-93 by
  `energyml-proj`, they give back the rectangle X 650 600-652 000,
  Y 6 861 100-6 862 700 within 5 cm (checked by triangulation);
- the third coordinate is **35 m NGF-IGN69**: the boundary is set at the mean
  ground level, and 35 m is the median of the 18 known ground elevations of the
  retained boreholes (from 26.14 to 37.7 m, median 35.06 m, mean 34.73 m).

`donnees/profils/` - the A-A' section and its drawing, **computed from the
package itself** by the section view (`energyml-section`): a two-segment
trace, three cross-sections, the boreholes projected in a corridor 200 m wide on
the left and 150 m on the right, and a blue diamond at the bottom of each drawn
BSS borehole. Replayed by:

```bash
# from the root of energyml-lutetia; the CLI needs the `png` feature, and the clean package is package/
energyml profile package/Lutetia.epc --track "650700,6861450;651250,6861750;651850,6861350" --left 200 --right 150 --cross-count 3 --cross-length 300 --cross-width 100 --draw long --size 1400x700 --labels full --marker "Forages BSS:shape=diamond,colour=#1565c0,at=bottom,type=WellboreTrajectory,title=BSS" --svg recipe/donnees/profils/coupe-lutetia.svg --png recipe/donnees/profils/coupe-lutetia.png --png-scale 1.5
```

The SVG carries in its metadata everything it was computed from; the `coupe`
step reads the trace back from it - the written polyline **is** the drawn line.
The font (Liberation Sans, SIL OFL) is the crate's own, embedded: no system font
enters the rendering.
