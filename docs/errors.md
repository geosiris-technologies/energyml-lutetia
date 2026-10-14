# The deliberate errors

`package-with-errors/` is Lutetia plus a second `Model` titled `[ERROR] Lutetia - deliberate anomalies` and the objects it gathers. Each is wrong on purpose, against one written rule, to prove that a checker **speaks**: a clean package only shows that it stays silent. The inventory difference between the two variants is 39 data objects (1 341 against 1 302).

Rules of the variant:

- every `[ERROR]` object has a title that starts with `[ERROR]`;
- **no clean object references an `[ERROR]` object** (the objects are leaves; they may reference clean ones). The one exception is the provenance chain: activities that record the steps;
- the folder `[ERROR] Lutetia` (a `DataobjectCollection`) lists them;
- each defect is written by an ordinary operation and then changed in one field (`edit-object`), so the writers stay strict;
- everything outside `[ERROR]` is meant to check with no error.

To build the clean model from the same recipe: `--without erreur` ([build.md](build.md)).

## Catalogue

Ids are those of the recipe (`E-nn`). "Rule" cites the specification the checker cites. "`energyml check` report" is what `energyml check` 0.1.0 reports on the variant: eight errors and one warning (E-04), so it exits 1. The exact list, by object uuid, is [errors.expected.txt](errors.expected.txt), which the `check` workflow compares with every run.

| Id | What is wrong | Rule broken | Expected `energyml check` report |
|---|---|---|---|
| E-01 | A property is placed on the **abstract** property kind `force per length` (on the frame of `[ERROR] GTH-9`) | A kind marked abstract in the Energistics PropertyKind dictionary v2.3 is a category on which no value is placed: Energistics common technical reference guide section 11.9, such a kind "should be used only as the parent of a real property" | `properties` section: abstract kind `force per length`, on "[ERROR] GTH-9 - force per length" |
| E-02 | A property on the root kind `property` (abstract) | same | `properties`: abstract kind `property`, on "[ERROR] GTH-9 - property" |
| E-03 | A discrete property whose value `0` (sand) has no row in its lookup table (the key column holds 1, 2, 3) | Energistics common 2.3 technical reference, section 9.1 p. 190: the key column makes the table a lookup table. (House rule, not a schema rule.) | `house/discrete-value-in-lookup` on "[ERROR] GTH-9 - [ERROR] lithology" |
| E-04 | A `TimeSeriesData` whose `asset identifier` names `well(GTH-99)`, which no well of the package is | Energistics Identifier Specification v4.0 section 6.3 p. 14 (grammar of the identifier). That no well resolves is a house rule | `house/time-series-asset-resolves` on "[ERROR] GTH-99 - wellhead pressure" |
| E-05 | **Not written.** A unit `g/L` on a dimensionless kind. Written only when the check for unit/kind dimension exists | - | none in this version |
| E-06 | Two `Trajectory` objects with `Definitive = true` on the same `Wellbore` | WITSML Technical Reference Guide v2.1, section 16.6 p. 350: "There can only be one trajectory per wellbore with definitive=true" | `trg/one-definitive-trajectory-per-wellbore` on the Wellbore "[ERROR] GTH-9" |
| E-07 | A **reverse** fault (`F9`) that carries `IsListric` | `Interpretations.xsd` lines 659-662, RESQML TRG 2.2 section 6.20 p. 188: "Must be present if the fault is normal. Must not be present if the fault is not normal." | `trg/is-listric-iff-normal` on "[ERROR] F9 - interpretation" |
| E-08 | A collection with `HomogeneousDatatype = true` that mixes a `WellboreInterpretation` and a `HorizonInterpretation`, and an earth model whose wellbore set holds a non-wellbore | `Collection.xsd` lines 66-70 ("If true all data objects in the collection are of the same Energistics data type"); RESQML TRG 2.2 section 6.19 p. 187 (the collection must only contain `WellboreInterpretation`) | two findings: `trg/homogeneous-collection` on "[ERROR] wells"; `trg/wellbore-interpretation-set-holds-wellbores` on "[ERROR] Lutetia - deliberate anomalies" |
| E-09 | A structural contact whose subject is a **representation** (the surface of F9), not an interpretation or a feature | RESQML TRG 2.2 section 6.9 p. 173 | `trg/contact-element-is-geological` on "[ERROR] Lutetia - structure" |

Totals of the checker on this variant: 9 findings (E-01, E-02, E-03, E-04, E-06, E-07, two for E-08, E-09), eight errors and one warning (E-04); E-05 produces none. The clean model reports no error and no warning.

## Notes and open points

- The document references above are those the checker of the `energyml` repository cites; the page numbers are those of the specification PDFs it was written against.
- The severities are those of `energyml check` 0.1.0. A later version may grade a finding differently; `docs/errors.expected.txt` then moves with `recipe/energyml-version`.
- The `[ERROR]` wells are an invented well `GTH-9` (a 60 m vertical hole) and its WITSML side, so that the two trajectory defect and the property defects have a support. Its title never equals `GTH-9` alone, and E-04 names `GTH-99` to avoid any ambiguity.
