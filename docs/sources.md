# Sources of the inputs

Every input of the recipe under `recipe/donnees/`, with its origin and licence. The
packages are offered under CC BY 4.0 ([LICENSE-data](../LICENSE-data)), which every
licence below allows.

> **The BSS data were modified for this example.** Lutetia is an example, not a copy of
> the BSS: the positions, elevations and logged intervals of the boreholes come from the
> BSS, and the model adds synthetic content to them (boreholes extended below their
> logged base, invented horizons, logs, a geothermal doublet and its production;
> deliberate errors in `package-with-errors/`). Every synthetic object says so in its
> description. Do not use these packages as BSS data: the data themselves are served by
> the BRGM (<https://infoterre.brgm.fr>).

## Summary

| Input | Origin | In this repository | Licence | Attribution |
|---|---|---|---|---|
| `bss/forages.geojson` | BRGM Banque du sous-sol (BSS), its public GeoSciML web service, harvested on 23 and 24 September 2026 | yes: the API answers differently today ([build.md](build.md)) | Licence Ouverte 2.0 | BRGM - Banque du sous-sol (BSS) |
| `bss/passes-etages.csv` (+ `.template.json`) | transcribed by hand from the BSS validated logs and record sheets, linked to the GeolTs chart | yes | Licence Ouverte 2.0 for the BSS part, CC BY 4.0 for the GeolTs columns | BRGM |
| `bss/moisson/` (record sheets, a validated log image, their transcription) | BRGM InfoTerre, BSS views of 4 boreholes | no: they served to write `passes-etages.csv` | Licence Ouverte 2.0 | BRGM |
| GeolTs chart (compiled into the `energyml` CLI, step `colonne`) | BRGM, <https://data.geoscience.fr/ncl/GeolTs> | inside the CLI | CC BY 4.0 | BRGM |
| `emprise.geojson` | written for the recipe; the four corners of the area | yes | CC BY 4.0 | Geosiris |
| `erreurs/proprietes.csv`, `erreurs/proprietes.template.json` | written for the recipe; invented values | yes | CC BY 4.0 | Geosiris |
| `profils/coupe-lutetia.svg`, `.png` | computed from the package itself by the section view of `energyml` | yes | CC BY 4.0; the embedded font (Liberation Sans) is under the SIL OFL 1.1 | Geosiris |
| `media/symbols/doublet.png`, `puits-vertical.png` | two 16-pixel geometric pictograms drawn for the recipe | yes | CC BY 4.0 | Geosiris |
| `media/README.md` | written for the recipe | yes | CC BY 4.0 | Geosiris |

## The BRGM borehole data (BSS)

**Licence.** The BRGM publishes the data of InfoTerre, the BSS included, under the
Licence Ouverte / Open Licence 2.0 (Etalab): *"Les Données disponibles sur le site
InfoTerre (infoterre.brgm.fr) sont soumises à la licence Ouverte / Open Licence Etalab
Version 2.0"* ([conditions of use of the data](https://infoterre.brgm.fr/page/conditions-dutilisation-donnees)).
Reuse is free provided the source (BRGM) and the date of the last update are cited; the
same page asks that the data not be altered nor their meaning distorted, which is why
the modifications made for this example are stated above and in every synthetic object.

**What was taken, and when.** `bss/forages.geojson` holds 23 boreholes of the BSS
inside the area, as the BRGM web service returned them on 23 and 24 September 2026
(GeoSciML `Borehole` features, WGS 84), assembled from two harvests with no value
modified. `bss/passes-etages.csv` has one line per logged interval (14 boreholes from
the validated logs, 6 from the record sheets) with the stage the source gives, linked
to the GeolTs chart by code and label. Its columns, the rules followed and the checks
made on it are in `recipe/donnees/bss/README.md`.

**Why this repository carries them.** The service answers with what the BRGM holds at
the time of the request. On 14 October 2026 the area query of [build.md](build.md)
returned 85 boreholes; 9 of the 23 used here were not among them, and the 14 others came
back with other values. A replay from a new harvest therefore writes a different
package, so the recipe reads the copy of `bss/forages.geojson` kept here.
`bss/passes-etages.csv` cannot be fetched at all: it was written by hand from the
validated log images and the InfoTerre record sheets, which are not republished.

## The GeolTs chart

The stratigraphic column (step `colonne`) reads the BRGM GeolTs registry, which ships
inside the `energyml` library. Identifiers, notations and labels come from
<https://data.geoscience.fr/ncl/GeolTs>, which the registry publishes under CC BY 4.0.
Attribution: BRGM.

## Energistics dictionaries

The property kinds used by the CLI come from the Energistics PropertyKind dictionary
v2.3 and are cited by UUID in the template; see [NOTICE](../NOTICE).

## What is *not* used

No IGN data, no digital terrain model and no seismic data. The ground surface is
interpolated from the elevations of the BSS boreholes.
