# Lutetia

A **synthetic** model of the Paris Basin around the Louvre, built to exercise
EnergyML readers and writers. It is not a geological study. Everything in this
package is written by `energyml-rust` from a recipe
(`recipe/recette.toml` of the `energyml-lutetia` repository).

## What is real

- **The area**: a 1 400 m × 1 600 m rectangle in Lambert-93 (EPSG:2154),
  X 650 600-652 000, Y 6 861 100-6 862 700, heights in NGF-IGN69 (EPSG:5720).
- **The boreholes named `BSS…`**: 19 boreholes of the BRGM's Banque du
  Sous-Sol - positions, ground elevations and lengths as the BSS gives them
  (Licence Ouverte 2.0). One, BSS004PSGA, has no elevation and is refused by
  name rather than placed at 0.
- **The stratigraphic units**: the BRGM's GeolTs chart (CC BY 4.0) - the
  Palaeogene, the Cretaceous and the Quaternary branch.
- **Measured tops**: five of the seven horizons are picked from the BSS logs;
  the top of the Chalk is measured at 62.7-87.3 m in the area.

## What is invented

- **The four `GTH-` wells** - a geothermal doublet on the Chalk aquifer, an
  observation well and its lateral - their trajectories, logs and production.
- **The horizons no borehole reaches**, the faults, the grid and its
  properties, the relief of the south-east, the time series.
- **Anything a borehole does not say**: depths extended below a borehole's
  end, interval heights where the BSS gives none.

## 200 m

Nothing goes deeper than **200 m of vertical depth below the ground**. The deep
Paris Basin (Dogger, Bathonian, the classic 1 600 m doublets) is left out on
purpose: the model stops in the Chalk.

## The `[ERROR]` model

A second `Model`, titled `[ERROR]`, is where objects that are **wrong on
purpose** go - each one against a written rule, every title prefixed `[ERROR]`,
and none of them referenced by a clean object. They exist to prove that a
checker speaks: a clean package only proves that it stays silent. Everything
outside `[ERROR]` is meant to check with no error and no warning. The recipe
says which of these objects are written today.

## This file

A part of the package (`media/README.md`, `text/markdown`), related to the
model it describes by the EPC relationship `destinationMedia`, and back by
`sourceMedia` (Energistics Packaging Conventions v1.0, §3.4.2).
