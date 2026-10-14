# Context: the geology, and what is real

Lutetia takes its name from the Roman city on the site of Paris and from the **Lutetian**, the Middle Eocene stage whose limestones ("Calcaire grossier") built much of Paris. The model sits in the Paris Basin, around the Louvre.

## The area

A rectangle in Lambert-93 (EPSG:2154), 1 400 m west to east and 1 600 m south to north:

| Corner | X (m) | Y (m) |
|---|---|---|
| SW | 650 600 | 6 861 100 |
| SE | 652 000 | 6 861 100 |
| NE | 652 000 | 6 862 700 |
| NW | 650 600 | 6 862 700 |

Heights are in NGF-IGN69 (EPSG:5720). The rectangle contains the left-bank boreholes (Institut de France, quai Malaquais, rue de Seine), the Seine, the Pont des Arts, Pont Royal and Pont Neuf, the Cour Carree and the Pyramid. `recipe/donnees/emprise.geojson` gives the four corners in WGS 84; reprojected to Lambert-93 they give the rectangle above to within 5 cm.

## The geological setting

Under the area, the boreholes read (from the top):

- **Made ground** (remblais), 0 to about 5 m, dated Holocene by the BRGM logs.
- **Quaternary alluvium of the Seine**, with its base between 2.9 and 10.5 m.
- **Lutetian** (Middle Eocene): marls and caillasses, "Banc vert", Calcaire grossier. Its base is found from 26.8 m to 40.1 m in the boreholes retained.
- **Ypresian**: the Sparnacian clays and sands (Fausses glaises, Sables d'Auteuil, Argile plastique) and the Cuisian sands.
- **Selandian**: the Marnes de Meudon.
- **Campanian**: the chalk (Craie a silex), whose top is measured at 62.7 to 87.3 m, that is between -27.7 and -48.3 m NGF.

No borehole reads Thanetian, Danian or Maastrichtian layers: the gaps are real and are kept as gaps (the grid has a K gap at the Marnes de Meudon).

## What is real

- **The area and its coordinate systems** (EPSG:2154, EPSG:5720).
- **The boreholes named `BSS...`**: boreholes of the BRGM subsurface databank (Banque du sous-sol), with positions, ground elevations, lengths and, for 14 of them, the interval-by-interval stratigraphy read from the validated BSS logs or from the BSS record sheets. Of the 23 boreholes in the input file, 14 are written as wellbores; the others are skipped by name (no logged interval, or no ground elevation: BSS004PSGA is refused rather than placed at 0).
- **The stratigraphic units**: the BRGM GeolTs chart (Quaternary, Palaeogene and Cretaceous branches, with their ancestors).
- **Measured horizon tops**: the base of the Quaternary (H1), the base of the Lutetian = top of the Ypresian (H3), the top of the Sparnacian (H4), the top of the Selandian (H5) and the top of the Chalk (H6) are interpolated from tops picked in the BSS logs. The ground surface is interpolated from the elevations of the boreholes.

## What is synthetic

- **The four `GTH-` wells**: a geothermal doublet on the Chalk aquifer (a deviated producer, a horizontal injector, an observation well and its sidetrack), with their trajectories, logs, WITSML and PRODML records.
- **The horizons no borehole reaches**: H7 (top of the Santonian) is laid 95 m below H6; H2 (top of the Lutetian) is defined by a law but is not played in this version: the recipe step is on hold because the Lutetian top is eroded everywhere in the area, see [build.md](build.md). The faults, their throws, the structural organisation, the IJK grids and their properties (porosity, net-to-gross, permeability, pressure, temperature), the time series, the velocity law between depth and time, the fluid samples and tests.
- **Anything a borehole does not state**: depths below the end of a borehole (the 200 m extension of the BSS holes is a straight vertical continuation), interval heights where the databank gives none.
- **Dates**: the construction dates of the doublet and its production are invented. The package creation time is fixed to 2026-09-24T00:00:00Z so that two runs give the same bytes.

Synthetic objects say so in their citation description and give the law or assumption used; this is also stated in each step of the recipe. Values are plausible orders of magnitude, **not measurements**: do not use Lutetia for any study.

## Depth limit

Nothing is deeper than **200 m of vertical depth below the ground**. The deep Paris Basin (Dogger and the classical 1 600 m geothermal doublets) is left out on purpose.

## Two variants

`package/` is the clean model. `package-with-errors/` adds a second `Model` and the objects it holds, all prefixed `[ERROR]`, which are wrong on purpose and which no clean object references. See [errors.md](errors.md).
