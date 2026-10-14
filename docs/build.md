# How Lutetia is built, and how to replay it

The packages are the output of one recipe, `recipe/recette.toml`, played by the `energyml` CLI (`energyml create --recipe`). Each `[[etape]]` (step) names an operation, its inputs (files, or the output of an earlier step), its settings, and optionally a free-text list of what it serves (`sert`, left empty in this recipe). Steps are played in order into a single package. The creation time and the author are written in the recipe and every UUID is derived from the content, so **the same inputs always give the same bytes**.

> The comments of the recipe are in English. The keys the parser reads (`etape`, `nom`, `operation`, `sert`, `attente`...) and the step names are French, and so are some titles, which are data written into the package. Step names below are the names in the file.

## The BSS inputs are in this repository

The recipe reads two BRGM inputs, both under `recipe/donnees/bss/`: `forages.geojson`, the
23 boreholes as the BRGM web service returned them on 23 and 24 September 2026, and
`passes-etages.csv`, the stage of each logged interval, transcribed by hand from the
validated logs and the record sheets ([sources.md](sources.md)). A replay reads these
copies and fetches nothing.

The web service answers with what the BRGM holds at the time of the request, and it has
moved since: on 14 October 2026 the area query below returned 85 boreholes, 9 of the 23
were not among them and the 14 others came back with other values. To see what it answers
today (the `replay` workflow does it every week, for information):

```bash
# the quote first: how many boreholes, how many pages (nothing is written)
energyml fetch brgm-bss boreholes --area recipe/donnees/emprise.geojson --where codeSpace=BRGM

# then write the answer, verbatim (one page of up to 1000 features: one file)
energyml fetch brgm-bss boreholes --area recipe/donnees/emprise.geojson --where codeSpace=BRGM --out fresh.geojson
```

Building Lutetia from a new harvest is possible (point the recipe's step `forages` at the
new file), but it writes another model: the uuids, derived from the content, follow the
values.

## Replay

Install the `energyml` CLI at the version in `recipe/energyml-version`, built with HDF5 support (the steps that write arrays need it). Then `python scripts/replay.py` plays both variants into `package/` and `package-with-errors/` and writes `written-on` (the platform that decides whether a later replay is compared byte for byte or up to float noise; see the [README](../README.md#the-energyml_lutetia_dir-contract)). By hand, the same thing is:

```bash
# the plan: every step, nothing written
energyml create --recipe recipe/recette.toml --plan

# the clean model: leave out the group "erreur"
energyml create --recipe recipe/recette.toml --without erreur --out out/clean/Lutetia.epc

# the model with deliberate errors: play everything (its own folder: both write Lutetia.h5)
energyml create --recipe recipe/recette.toml --out out/errors/Lutetia.epc
```

**When a recipe edit moves uuids: `python scripts/replay.py --redraw`.** The `coupe` step (operation `section-view`) takes the stored drawing `recipe/donnees/profils/coupe-lutetia.svg` and `.png`, which name by full uri the objects they were drawn from. After an edit that changes an object's uuid (a changed `source` text, for instance), the step refuses ("the drawing was computed from <uri>, which this package does not hold") and the recipe no longer plays. `--redraw` then (1) plays a temporary copy of the recipe, with the `coupe` step awaited and out of the project, `--without erreur`; (2) runs `energyml profile` on that package to overwrite the stored SVG and PNG; (3) does the normal replay of both variants. Needs a CLI built with `hdf5` **and `png`**. The profile options are hard-coded in the script (`PROFILE_ARGS`) and must match the stored drawing; `profile --from-svg` cannot be used because it looks up the very uris that moved. Commit the new drawing with the new packages.

- `--without <group>` leaves out the steps whose `groupe` is `<group>`; `erreur` is the only group.
- File names in the recipe (`donnees/...`) are relative to the recipe's own folder, wherever you run the command.
- The `.h5` is written next to the `.epc`, under the name the recipe gives (`donnees = "Lutetia.h5"`), and the EPC refers to it by that name. For that reason the committed `package-with-errors/` currently uses the file names `Lutetia.epc` / `Lutetia.h5` too. `TODO(verify)`: decide whether to rename the variant (the recipe would need to write its own `donnees` name, or use `energyml rename`).
- To compare a replay with the committed files: `cmp out/clean/Lutetia.epc package/Lutetia.epc && cmp out/clean/Lutetia.h5 package/Lutetia.h5` (and the same for `out/errors` and `package-with-errors`); remember that a byte-for-byte comparison only holds on the platform in `written-on`. The CI workflow `replay.yml` fetches the BSS inputs, replays, compares, and **reports a difference** (a changed API answer is a possible cause, not necessarily a bug).

## The steps

All steps are listed here in recipe order, grouped as the recipe groups them. The operation is the `operation` key; run `energyml create --list` for what each does.

| Phase | Steps (operation) | What they make |
|---|---|---|
| 1. Frames, boundary, column, time | `repere-profondeur`, `repere-temps`, `repere-grille` (`crs`); `bord` (`polylines`); `colonne` (`stratigraphy-from-geolts`); `temps-forage`, `temps-exploitation`, `temps-mensuel` (`time-series`); `brgm`, `etude` (`business-associate`) | Lambert-93 + NGF-IGN69 CRS, depth and time compounds, a grid CRS rotated 30 degrees; the model frontier; the stratigraphic column from GeolTs; three chained time series; the data provider and the model author |
| 2. BSS boreholes | `forages` (`sigeol-boreholes`); `etages` (`wells-and-properties-from-table`) | wellbores, trajectories and frames from the BSS file; the stage of each interval from the table |
| 3. Contacts and surfaces | `sol-collets` (`pointset-from-wellheads`); `sol` (`interpolate`); `dtm-pendage`, `dtm-azimut` (`surface-map`); `dtm-pendage-carte` (`colormap`); `dtm-pendage-couleurs` (`graphical-information`); `contacts`, `h1-points`, `h3-points` (`contacts-from-frames`); `h1`, `h3`, `h4`, `h5`, `h6` (`interpolate`); `h6-profondeur`, `h6-temps` (`change-frame`); `h3-triangulee` (`triangulate`) | ground surface and its slope maps with a colour map; contact point sets; horizons H1, H3 to H6 on the ground lattice; H6 in depth and in time; H3 as triangles |
| 4. Unmeasured horizons | `h7`, `h2` (`horizon-from-law`); `forages-etendus` (`extend-boreholes`) | H7 laid below H6 (95 m); H2 (**on hold**, see below); BSS holes extended to 200 m |
| 5. Grid | `grille` (`ijk-grid-from-horizons`); `pression-grille`, `temperature-grille`, `porosite-grille`, `ntg-grille`, `permeabilite-grille` (`grid-properties`); `grille-locale` (`local-grid`); `pression-grille-serie`, `temperature-grille-serie` (`property-time-series`); `reservoir` (`subrepresentation`); `grilles-craie` (`representation-set`, **on hold**) | IJK grid with a K gap, its properties, a local refined grid, ten-year series, a reservoir sub-representation |
| 6. The doublet | `gth-1`, `gth-2`, `gth-3`, `gth-3-st1` (`well-from-plan`); `gth-1-bloque`, `gth-2-bloque` (`blocked-wellbore`) | four planned trajectories (deviated, horizontal, vertical, sidetrack) and blocked wellbores through the grids |
| 7. Well properties | `temperature-doublet`, `pression-doublet`, `temperature-forages`, `pression-forages` (`well-logs`); `pression-gth-1-annuelle`, `pression-gth-1-mensuelle` (`property-time-series`) | logs laid by declared synthetic laws |
| 8. WITSML and PRODML | `witsml-doublet`, `witsml-forages` (`witsml-wells`); `prodml-doublet`; `echantillon-gth-1` (`fluid-sample`); `fibre-gth-3` (`dts-installation`); `test-injectivite-gth-2` (`injection-test`); `pta-gth-2` (`pressure-transient-analysis`); `reseau-doublet` (`product-flow-model`); `logs-doublet`, `logs-doublet-h5` (`witsml-logs`) | Well/Wellbore/Trajectory, production data, fluid sample, DTS fibre, injection test and analysis, flow model, channel logs |
| 9. Structure | `f1` to `f4` (`fault-from-sticks`); `structure-a`, `structure-b` (`structural-organisation`); `h6-rejet`, `h7-rejet` (`fault-throw`); `cadre-b` (`surface-framework`) | four faults, two structural organisations, throw applied to H6 and H7, a surface framework |
| 10. Organisation | `puits-du-modele`, `puits-verticaux`, `repli-*`, `projet` (`collection`); `tete-puits-verticaux`, `tete-gth-1` (`attach`); `modele` (`earth-model`); `modele-eocene` (`earth-model-from-stratigraphy`); `grille-represente`, `grille-locale-represente`, `reservoir-represente` (`edit-object`); `grille-faillee` (`faulted-ijk-grid`) | collections, head images, the earth models, a faulted grid; `repli-*` steps exercise colour fall-back rules |
| 11. Attachments, colours, section | `lisez-moi` (`media`); `export-emprise`, `export-h3`, `export-grille` (`export-media`); `couleurs`, `couleurs-replis` (`graphical-information`); `h3-triangulee-v2` (`new-version`); `coupe` (`section-view`) | README, OBJ/GeoJSON/VTU attachments, colours, a new object version, the A-A' section |
| 12. `[ERROR]` model (group `erreur`) | `erreur-*` | deliberate errors, only in the variant with errors: see [errors.md](errors.md) |

### Steps on hold

A step with `attente = "reason"` is checked and reported but not played. In this version `h2` (the top of the Lutetian is eroded everywhere in the area, so a 40 m layer above H3 lies above H1 and the operation refuses an empty surface), `grilles-craie` (it waits for grids that no step writes) and `couleurs` (one colour is still to be decided) are on hold. The recipe's header explains the rule: a step is never commented out, it is put on hold with its reason.

## Recipe language

The recipe is the file copied from the `energyml` repository. Its comments are in English; its keys and step names stay French because the parser reads them. `TODO(verify)`: whether the CLI will accept English aliases of the keys.
