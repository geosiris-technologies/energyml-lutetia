# Lutetia - the BSS inputs: 23 boreholes, their intervals, the stage of each interval

> **Note.** The public `energyml-lutetia` repository carries this README, the
> column template, `forages.geojson` and `passes-etages.csv` (Licence Ouverte
> 2.0, source BRGM, harvests of 23 and 24/09/2026): what the recipe reads. The
> harvested record sheets, log images and transcriptions under `moisson/` are
> **not republished**. The API answers differently today (other boreholes, other
> values), so a replay reads the copy, not a new harvest; a new harvest is made with
> `energyml fetch brgm-bss boreholes --area <emprise.geojson> --where codeSpace=BRGM --out <forages.geojson>`.

Prepared on **24/09/2026** for the Lutetia recipe (borehole selection, GeolTs
matching, the fallback for boreholes without intervals, and the lithology
table). The four boreholes NXAD, NYRW, NTGZ and
NTWA were added to the original 19, making **23 boreholes**. The
transcriptions were **reviewed globally on 28/09** - every line of
`passes-etages.csv` now carries `relu = oui`, and the [To review](#to-review)
section remains the list of what was reviewed. The review was an overall one,
not line by line, so the boxes in that list are not ticked one by one. Lutetia
is a demonstration model, not meant for a real study: the data are meant to be
**coherent with each other**, not geologically exact, and coherence is what
counts for Lutetia.

The scripts that produced these files were throwaway and are kept out of the
repository; their results are here, with their provenance.

## Licences

- **Banque du sous-sol (BSS)** - boreholes, intervals, InfoTerre record sheets,
  validated GDM logs: **Licence Ouverte 2.0** (Etalab), dataset « Banque du
  sous-sol » on data.gouv.fr. Attribution: *BRGM - Banque du sous-sol (BSS)*.
  The record sheets and the logs state no licence of their own; they are served
  by BRGM as views of the same BSS (header of the README of the first harvest).
- **GeolTs register** (`GeolTs.csv`, shipped with `energyml-domain`; `https://data.geoscience.fr/ncl/GeolTs`) -
  identifiers, notations and labels of the `geolts_*` columns: **CC BY 4.0**
  (`dct:license` of the `/ncl/` registers). Attribution: *BRGM*.
- The property kinds of the template are those of the Energistics dictionary
  `PropertyKindDictionary_v2.3`, cited by uuid.

## The files

| file | what it is | shape |
|---|---|---|
| `forages.geojson` | the 23 selected boreholes, **GeoSciML features exactly as the harvest returns them** | `FeatureCollection`, 23 `Borehole` features, `crs` member = `urn:ogc:def:crs:EPSG::4326` |
| `passes-etages.csv` | one row per interval of the validated log (14 boreholes) or per level of the record-sheet section (6 boreholes), with the stage and its link to GeolTs | 194 rows + header, 19 columns; UTF-8 without BOM, comma, decimal point, LF line endings |
| `passes-etages.template.json` | the column template that `--template` reads: one `master-data--ColumnBasedTableTemplate:1.0.1` record | 2 `KeyColumns` + 15 `Columns` |
| `README.md` | this file | |
| `moisson/requetes.log` | the 5 requests made on 24/09 to complete the 4 added boreholes: UTC date, HTTP status, size, file, URL | 5 lines |
| `moisson/logs-valides/BSS000NTWA.png` | the validated GDM log of NTWA, **missing** from the 24/09 harvest (which holds only 13 logs) | PNG 850 × 691 |
| `moisson/fiches/BSS000{NXAD,NYRW,NTGZ,NTWA}.html` | the InfoTerre record sheets of the 4 added boreholes, **in Latin-1**: *Nombre de passes*, *Profondeur atteinte*, coded section | 4 files |
| `moisson/niveaux-fiches-ajouts.csv` | the coded section (B) of these 4 record sheets, flattened, same shape as `niveaux-fiches.csv` of the first harvest - **for the record**: for these boreholes the validated log (A) takes precedence and it is what is in `passes-etages.csv` | 32 levels |

Requests of `moisson/requetes.log` (same form as the `requetes.log` of the
first harvest, whose series they complete):

- `https://servicesgdm.brgm.fr/LGV_Internet/LGV_PostGIS/Log.aspx?HoleName=01836B0562&From=0.0&To=60` -
  `HoleName` = `parameter_indice_bss` of NTWA, `To` = the base of its last
  `…_GLU…` interval (the rule of the first harvest's README);
- `http://ficheinfoterre.brgm.fr/InfoterreFiche/ficheBss.action?id=<BSS>` for
  NXAD, NYRW, NTGZ, NTWA.

## `forages.geojson`

**Assembled from two harvest files, no value modified**:

| boreholes | taken from | original request |
|---|---|---|
| the 19 of the original selection | `boreholes.geojson` of the first harvest (23/09) | `gsmlbh:Borehole`, `bbox=48.850,2.330,48.856,2.340`, `outputFormat=application/json` |
| NXAD, NYRW, NTGZ, NTWA | `boreholes-brgm-emprise.geojson` of the second harvest (24/09) | `gsmlbh:Borehole` on the extent polygon, filter `collectionIdentifier/@codeSpace='BRGM'` |

The 10 boreholes present in both files are **identical** in them (compared as
parsed JSON). Every written feature was re-read and compared with its source:
23 out of 23 equal. What changes is the serialisation (indentation; key order of
`boreholes.geojson`, which had been reformatted on 23/09 with sorted keys) and
the leading members `numberMatched`, `numberReturned`, `totalFeatures`,
`timeStamp`, which are **removed**: they describe the original requests and
would be wrong for this assembled file. `type`, `crs` (the same in both
sources) and `features` stay. Order: the 19 in their original order, then the 4.

**What the import will do with it - read in the code, not run**
(`energyml-build`, `ops/sigeol_boreholes.rs` and `borehole.rs`):
`sigeol-boreholes` reads the features whose `@featureType` is `Borehole`, the
head in `geometry` (`Point`), the ground in
`referenceLocation.properties.elevation`, and **rebuilds the MDs from the bounds
of the `logElement`s**. Therefore:

- **14 boreholes are written** (the 10 with intervals and the 4 added). Their
  frame nodes are exactly the bounds of the `…_GLU…` intervals: checked on all
  14, the bounds of the lithology intervals (`<BSS>_<uuid>`) are all bounds of
  intervals (rechecked here against the first harvest's notes);
- **BSS004PSGA is dropped by name** - *« no `referenceLocation.elevation`:
  the ground is unknown »* -, the elevation test coming before the depth test:
  a known open point (a borehole without a known ground elevation);
- **the 8 others without intervals** (NSYT, NZNM, NZNP, PATK, NVHN, NVGR, CIKC,
  CIKW) are dropped too, with *« no `logElement`: nothing states a depth »*:
  the harvest gives them no interval. **Their frame cannot come from this
  file.** Six of them have a record-sheet section, which is in
  `passes-etages.csv`; PATK and NVGR have nothing (0 levels) and fall under the
  fallback for boreholes without intervals.

## `passes-etages.csv`

### The columns

| column | what it carries | source |
|---|---|---|
| `bss` | the BSS identifier | `forages.geojson` |
| `longitude`, `latitude` | the head, in degrees, **EPSG:4326**, verbatim (4 decimals) | `geometry.coordinates` |
| `epsg` | `4326` on every row | the `crs` member of both harvest files |
| `sol_m` | the ground elevation (m), verbatim | `referenceLocation.properties.elevation` |
| `toit_m`, `mur_m` | the interval bounds, **MD from the ground**, in m | validated log: `mappedIntervalBegin`/`End` of the WFS `…_GLU…` intervals, **never read off the image**; record sheet: `niveaux-fiches.csv` of the first harvest |
| `source_passe` | where the bounds come from: `log-valide` or `fiche` | |
| `id_passe_wfs` | the interval identifier (`https://data.geoscience.fr/id/BoreholeInterval/<id>`) - empty for a record-sheet row | WFS |
| `code_glu` | the formation code, `GLU000ATIV` (suffix of `collectionIdentifier`) - empty for a record-sheet row | WFS |
| `formation` | the formation label **as printed** on the validated log; empty when the *Formation* box of the log is empty (code `GLU000AAAA`) | transcription of the PNG |
| `etage` | the stage **as the source names it**: validated-log label (`Lutétien supérieur`) or record-sheet mnemonic (`LUTETIEN-SUP`); **empty** when the source gives none, and for `IMPRECIS` (see `note`) | PNG or record sheet |
| `source_etage` | `log-valide`, `fiche` or `aucune` | |
| `geolts_id`, `geolts_notation`, `geolts_libelle` | the GeolTs division: identifier (end of the URI `…/ncl/GeolTs/<id>`), notation (`skos:notation`), label (`skos:prefLabel@fr`); empty when the stage is | `GeolTs.csv` |
| `lithologie_fiche` | the *Lithologie* column of the record sheet, verbatim - record-sheet rows only | `niveaux-fiches.csv` of the first harvest |
| `note` | what to know about the row: stage absent and why, formation empty and the printed lithology, base under the declared length, what the other source says | |
| `relu` | `oui` on every row (reviewed globally, see the top of this file) | |

### The rows

| rows | boreholes | `source_passe` |
|---|---|---|
| 2-83 | the 10 with intervals from the original selection (82 intervals) | `log-valide` |
| 84-115 | NSYT (3), NZNM (4), NZNP (3), NVHN (12), CIKC (5), CIKW (5) | `fiche` |
| 116-195 | NXAD (6), NYRW (26), NTGZ (10), NTWA (38) | `log-valide` |

**Absent, for lack of any data**: PATK and NVGR (0 levels in the record sheet),
PSGA (no record sheet: *« BSS n° null introuvable »*). They are in
`forages.geojson`, not here.

`source_etage`: 159 `log-valide`, 15 `fiche`, 20 `aucune`. The 20 without a
stage: NSYW 0-6 and 6-8.6 (*Avant puits*), NUSX 0-3 (*Sous sol*), NSYT 0-6.1
(`IMPRECIS`), the 12 levels of NVHN, and the first two levels of CIKC and of
CIKW (the record sheet does not date `SOUS-SOL 1` nor
`SABLE ET GRAVIERS (ALLUVIONS)`).

### The choices

1. **The WFS bounds, the labels of the image.** An interval of the validated
   log is a row; thin intervals stay rows (NTGS has 28, NTWA 38), even when the
   stage is the same over a whole box of the image.
2. **(A) takes precedence over (B), and (B) does not fill in (A)** - for the 14
   boreholes with a validated log, no record-sheet row is written. Where (A)
   does not date an interval, the stage stays empty: **NSYW 0-8.6** stays
   without a stage although the record sheet writes `QUATERNAIRE` over 0-8.6 m;
   this is said in the note, not applied.
3. **No guessed stage.** *Avant puits*, *Sous sol* and `IMPRECIS` keep an empty
   `etage` and a note. For NSYT 0-6.1, the word `IMPRECIS` is in the note
   (*« aucune division de GeolTs ne porte ce nom : refusé par son nom »*), not
   in `etage` - see the question at the end of the file.
4. **NVHN is kept, without a stage**: its 12 record-sheet levels give bounds,
   not a stage; the free text (*« Calcaire grossier beige Lutetien »*) is
   **not read** (an open question: whether free text should be interpreted).
5. **The link to GeolTs**, by code **and** label:
   - validated-log label → the division whose `prefLabel@fr` is **exactly**
     this label; the 11 labels met are each unique among the 698;
   - record-sheet mnemonic → by label: accents and case ignored, `-SUP` /
     `-INF` read as *supérieur* / *inférieur*; each mnemonic met (`LUTETIEN`,
     `LUTETIEN-SUP`, `LUTETIEN-INF`, `QUATERNAIRE`, `EOCENE-MOYEN`) designates a
     single `valid` division - and gives back the code-to-stage table of the
     first harvest;
   - the written notation is the **first** `skos:notation` of the division
     (Quaternaire carries three, `q|Q|IV`: `q` is written);
   - **check**: `Chart::find(notation, label)` rewritten in Python
     (`energyml-domain/src/geolts.rs` l. 310: notation case-insensitive ASCII,
     fr or en label in lower case) returns **one and only one** division for
     each of the 13 written pairs - `e4a` + `Sparnacien` → 2173, not 1252.

   | `geolts_id` | notation | label | rows (A) | rows (B) |
   |---|---|---|---|---|
   | 1326 | `_z` | Holocène | 16 | - |
   | 1316 | `q3` | Pléistocène supérieur | 11 | - |
   | 1289 | `q` | Quaternaire | - | 5 |
   | 1258 | `e5c` | Lutétien supérieur | 51 | 2 |
   | 1257 | `e5b` | Lutétien moyen | 2 | - |
   | 1256 | `e5a` | Lutétien inférieur | 9 | 1 |
   | 1255 | `e5` | Lutétien | 18 | 6 |
   | 1254 | `e5-6` | Eocène moyen | - | 1 |
   | 2174 | `e4b` | Cuisien | 9 | - |
   | 2173 | `e4a` | Sparnacien | 35 | - |
   | 1251 | `e4` | Yprésien | 1 | - |
   | 1247 | `e2` | Sélandien | 4 | - |
   | 1234 | `c5` | Campanien | 3 | - |

6. **Intervals below `boreholeLength` are kept**, and each says so in its note:
   NUGK 30.2-30.5 (length 30.2), NUKL 26.8-27 (26.8), NUKM 29.7-30 (29.7), NTGZ
   72-78.65 (78.6), and **17 intervals of NTWA**, from 26.8-34 to 59.3-60, for a
   declared length of 30 m (the record sheet says *Profondeur atteinte :
   30.0 m*). Neither truncated nor corrected.

### What the import will read from it - read in the code, not run

`wells-and-properties-from-table` with `--template passes-etages.template.json`:

- roles (`wells_from_table.rs`, `ROLES`, by uuid): `bss` → *well name*,
  `longitude` / `latitude` → *x* / *y coordinate*, `sol_m` → *elevation*,
  `toit_m` → *top depth* (a row is an interval `[top, base]`), `mur_m` →
  *measured depth*, `epsg` → *projection code* (so the source code is read from
  the file);
- **`project` must be given** (EPSG:2154): the source is geographic, and a
  borehole in degrees is refused by name;
- **`units = geolts_notation`, `unitLabels = geolts_libelle`**: the operation
  looks up `Chart::find(code, label)`; the 20 rows without a stage have both
  empty and stay **without a unit, counted** (note `units-unknown`);
- the other declared columns become interval properties (discrete, with their
  code table); `note` and `relu` are not declared, hence ignored and counted
  (`columns-ignored`);
- no interval overlaps its neighbour, there is no gap, all start at 0 m
  (checked): `intervals()` will refuse nothing;
- for the 14 boreholes with a validated log, the interval limits are **the same**
  MDs as the frame nodes of `sigeol-boreholes`, and the head is the same (same
  `longitude`, `latitude`, `sol_m`): a borehole already imported by
  `sigeol-boreholes` will be **recognised** (title + head). With `units`, the
  match enters the identity of the frame: the operation will then write a second
  trajectory/frame on the same interpretation (note `continued`), not nothing.

## `passes-etages.template.json`

An `osdu:wks:master-data--ColumnBasedTableTemplate:1.0.1` record, the shape read
by `crates/energyml-build/tests/osdu.rs` (`a_whole_template_record_reads_the_same`,
`key_columns_are_columns_too`); the identifiers follow the form of that same
test, `namespace:reference-data--PropertyType:<uuid>:`.

Each uuid was **checked in the dictionary** (tag
`<eml:PropertyKind schemaVersion="2.3" uuid="…">`, title in `<eml:Citation>`):
present, in 2.3, neither abstract nor deprecated.

| column | kind | uuid | `ValueType` | unit |
|---|---|---|---|---|
| `bss` (key) | well name | `348c9a4d-e3e4-4beb-8456-f07a46660de1` | string | |
| `toit_m` (key) | top depth | `cb1166d9-3874-4267-abea-1cd97e4bf448` | number | m |
| `longitude` | x coordinate | `620cec71-5ce3-4ea5-9120-833756b427d7` | number | - |
| `latitude` | y coordinate | `cfcfdb04-02c1-4262-b66b-459b0aab3e8e` | number | - |
| `epsg` | projection code | `d48ef4e7-f82e-4e91-bda2-685146223a85` | integer | |
| `sol_m` | elevation | `8508cef4-0ade-454a-9ea4-e00d5905e677` | number | m |
| `mur_m` | measured depth | `c48c65d4-9680-4d10-903c-a1b2e30f66b5` | number | m |
| `source_passe` | source | `b186c384-a744-447b-bd5b-3359d2ffd4b4` | string | |
| `id_passe_wfs` | identifier | `311dcaba-6512-4144-aa7c-79a9de19b4ab` | string | |
| `code_glu` | code | `5f78f66a-ed1b-4827-a868-beb989febb31` | string | |
| `formation` | formation name | `48a02f88-8cfe-44e5-acb3-45038443d8f7` | string | |
| `etage` | name | `0eb70eac-c3d2-4448-b617-10260c4abee3` | string | |
| `source_etage` | source | `b186c384-a744-447b-bd5b-3359d2ffd4b4` | string | |
| `geolts_id` | identifier | `311dcaba-6512-4144-aa7c-79a9de19b4ab` | string | |
| `geolts_notation` | geologic age code | `f626d5a4-47dd-4abd-92db-3a17ddee73fe` | string | |
| `geolts_libelle` | name | `0eb70eac-c3d2-4448-b617-10260c4abee3` | string | |
| `lithologie_fiche` | litho description | `4487b6ca-c5bd-4667-b1d4-7a04dc0bcd5b` | string | |

The choices it carries:

- **`longitude` / `latitude` without a unit**: the *x/y coordinate* kinds are of
  class `length`, and these values are degrees; the system is stated by `epsg`.
  A `dega` unit on a length kind would be a written contradiction;
- **`geolts_id` as `string`**: as `number`, the operation would write a
  **continuous** property of identifiers; as text, a discrete property and its
  table;
- **two columns per kind, three times** (`name`, `identifier`, `source`): the
  operation keeps its tables by *(kind, column name)*, so they stay distinct.
  The dictionary has **no kind for the name of a geological age** nor for **a
  formation code**: `name` and `code` are the parents that the design of the
  tables-to-boreholes operation names for the local kinds it proposes, and a
  `PropertyTypeID` absent from the dictionary is refused at import today;
- **`source_etage` as `source`** (*« The source of an entity instance »*) rather
  than `identifier`: it is a text column. The lithology table of the Lutetia
  design, which will have integer keys, is another object;
- **`note` and `relu` are deliberately not declared**: they are review columns,
  not data to put on a frame.

## Checks

Every count confronted with two independent sources in this file:

| borehole | rows | WFS `…_GLU…` intervals | *Nombre de passes* of the record sheet |
|---|---|---|---|
| NSYW | 5 | 5 | 5 |
| NTCE | 5 | 5 | 5 |
| NTGS | 28 | 28 | 28 |
| NTUM | 9 | 9 | 9 |
| NTUS | 7 | 7 | 7 |
| NUGK | 7 | 7 | 7 |
| NUKL | 9 | 9 | 9 |
| NUKM | 7 | 7 | 7 |
| NUSX | 3 | 3 | 3 |
| NZWP | 2 | 2 | 2 |
| NXAD | 6 | 6 | 6 |
| NYRW | 26 | 26 | 26 |
| NTGZ | 10 | 10 | 10 |
| NTWA | 38 | 38 | 38 |

**14 out of 14, no discrepancy.** The record sheets are read as Latin-1; those
of the first 10 are in the first harvest's `fiches/` folder, those of the 4
added in `moisson/fiches/`. For the 6 boreholes with a record-sheet section
only, the number of rows equals the *Nombre de niveaux* of the record sheet:
NSYT 3, NZNM 4, NZNP 3, NVHN 12, CIKC 5, CIKW 5.

And beyond the counts:

- **the bounds** of the 162 validated-log rows are, to the bit, those of the WFS
  (triplet top, base, interval identifier);
- **the heads** (longitude, latitude, ground) of each row are those of
  `forages.geojson`;
- **`niveaux-fiches.csv` re-read against the HTML**: the 99 levels were
  re-extracted from the 19 record sheets by a second reader - 99 out of 99, same
  order, same bounds, same labels, to **one space** (discrepancy below);
- **the stage limits read off the image, against the geometry of the image**: in
  the *Stratigraphie* column of each PNG, the solid horizontal lines and the
  attachment points of the connectors of the displaced labels were detected by
  a script (grey threshold, linear scale from 0 m at line 49.5 px to the final
  MD at 680.5 px) and brought back to the nearest interval bound: **all 51
  transcribed stage limits are detected** (to within 0.35 m; 39 out of 51 to
  within 0.1 m), and nothing else is detected in the column, except three marks
  on NTWA (12.2, 13.6 and 22.0 m): connectors of the *Lithologie* column that
  overflow on the left edge - the inside of the *Stratigraphie* column is empty
  at these depths, checked on the rendered image. This check would have turned
  red on a misplaced limit: NUKM 5.6 m and not 6.5 m, for example. **It checks
  where the limits are, not what the labels say**: the labels remain a
  transcription.

## The discrepancies

- **The top of the Sparnacien, NSYW against NTCE**: +6.4 m NGF (ground 35 −
  28.6) against −2.57 m NGF (ground 37.55 − 40.12), that is **8.97 m** between
  two boreholes ~166 m apart. **Not explained**, recomputed here, **not to be
  frozen**: no value is derived from it.
- **Intervals below `boreholeLength`**: see choice 6. NTGZ 78.65 against 78.6 is
  the smallest (0.05 m); NTWA 60 against 30, the largest.
- **(A) and (B) differ for the 4 added boreholes** (`moisson/niveaux-fiches-ajouts.csv`),
  and not only in the stage: the Marnes de Meudon are `MONTIEN` in (B) and
  *Sélandien* in (A) (NXAD, NYRW, NTGZ); the Craie of NTGZ is `SENONIEN` in (B)
  and *Campanien* in (A); NXAD 0-19.56 is `IMPRECIS` in (B) and *Holocène* in
  (A); NXAD 23.7-54 is `CUISIEN` then `SPARNACIEN` in (B), *Yprésien* in one
  piece in (A); NTWA 23.9-30 is `YPRESIEN` in (B) whereas (A) puts *Lutétien
  inférieur* then *Cuisien* there; and the bounds do not coincide (NXAD 54
  against 53.96, NTGZ 63.8 / 65.8 / 74.3 against 65.6 / 72). **Not explained
  here**; (A) is retained by the precedence rule, and (B) is kept alongside.
- **NXAD 0-19.56 m**: 19.56 m of *Remblais* dated *Holocène* by (A), with the
  lithology *« Remblais et marnes et caillasses (Lutétien)? »* on the image -
  the question mark is **on the log**. Nothing is corrected; the row is to be
  reviewed.
- **NTUM**: the validated log stops at 20.1 m, the record sheet says 20.4 m
  reached (first harvest's notes). The rows stop at 20.1.
- **`niveaux-fiches.csv` is not verbatim in one place**: NVHN 7.5-11 m, the
  record sheet writes *« Marnes beiges,blanchatres&nbsp;&nbsp;petits bancs »*
  (two spaces), the CSV one. The record-sheet rows of `passes-etages.csv` come
  from the CSV, as asked; the discrepancy is one blank. The `¿` of *« Calcaire
  dur ¿ glauconie »* (NVHN 28-28.8) **is** in the record sheet (byte `0xBF` in
  Latin-1): kept as is.
- **`GeolTs.csv` is UTF-8, not Latin-1**: the file decodes as UTF-8
  without error, and read as Latin-1 it gives *« LutÃ©tien »* - a label that
  `Chart::find` would not find. `crates/energyml-domain/build.rs` reads it with
  `read_to_string`, hence as UTF-8. It is the **record sheets** that are
  Latin-1.

## To review

### 1. The labels transcribed from the images - 14 boreholes, 162 rows

For each box of the *Formation* column of the validated log: the formation and
the stage read. The bounds are not to be reviewed (they come from the WFS, and
each stage limit was found again on the image, see *Checks*); what is to be
ticked is **the text**. The numbers are those of the rows of
`passes-etages.csv` (header = row 1). Each log is the PNG of the same name,
`BSS000<code>.png`, in the first harvest's `logs-valides/` folder (NTWA's is in
`moisson/logs-valides/`).

**BSS000NSYW** - `BSS000NSYW.png`, rows 2-6

- [ ] rows 2-3 (2 intervals, 0-8.6 m, `GLU000AAAA`): *(formation empty; lithology « Avant puits »)* → *(no stage)*
- [ ] row 4 (1 interval, 8.6-28.6 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] row 5 (1 interval, 28.6-37.6 m, `GLU000ATMW`): « Fausses glaises du Vexin » → « Sparnacien »
- [ ] row 6 (1 interval, 37.6-52.3 m, `GLU000ATND`): « Sables d'Auteuil » → « Sparnacien »

**BSS000NTCE** - `BSS000NTCE.png`, rows 7-11

- [ ] row 7 (1 interval, 0-3.8 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] rows 8-9 (2 intervals, 3.8-20.4 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 10 (1 interval, 20.4-40.12 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] row 11 (1 interval, 40.12-53.1 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »

**BSS000NTGS** - `BSS000NTGS.png`, rows 12-39

- [ ] row 12 (1 interval, 0-2.4 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] rows 13-14 (2 intervals, 2.4-9.3 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] rows 15-34 (20 intervals, 9.3-18 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] rows 35-39 (5 intervals, 18-20 m, `GLU000ATIV`): « Calcaire grossier supérieur d'Ile-de-France » → « Lutétien supérieur »

**BSS000NTUM** - `BSS000NTUM.png`, rows 40-48

- [ ] row 40 (1 interval, 0-2.1 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] rows 41-42 (2 intervals, 2.1-9.4 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 43 (1 interval, 9.4-12.5 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] rows 44-45 (2 intervals, 12.5-16.2 m, `GLU000ATIV`): « Calcaire grossier supérieur d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 46 (1 interval, 16.2-17 m, `GLU000ATJG`): « Banc vert d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 47 (1 interval, 17-19 m, `GLU000ATIV`): « Calcaire grossier supérieur d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 48 (1 interval, 19-20.1 m, `GLU000ATIV`): « Calcaire grossier moyen d'Ile-de-France » → « Lutétien moyen »

**BSS000NTUS** - `BSS000NTUS.png`, rows 49-55

- [ ] row 49 (1 interval, 0-2.2 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] row 50 (1 interval, 2.2-2.9 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 51 (1 interval, 2.9-11.3 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 52 (1 interval, 11.3-15 m, `GLU000ATJG`): « Banc vert d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 53 (1 interval, 15-23.25 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] rows 54-55 (2 intervals, 23.25-26.7 m, `GLU000ATJT`): « Calcaire et sables à Nummulites laevigatus » → « Lutétien inférieur »

**BSS000NUGK** - `BSS000NUGK.png`, rows 56-62

- [ ] row 56 (1 interval, 0-5 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] rows 57-58 (2 intervals, 5-6.4 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 59 (1 interval, 6.4-15 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 60 (1 interval, 15-17.35 m, `GLU000ATJG`): « Banc vert d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 61 (1 interval, 17.35-30.2 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] row 62 (1 interval, 30.2-30.5 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »

**BSS000NUKL** - `BSS000NUKL.png`, rows 63-71

- [ ] row 63 (1 interval, 0-3.9 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] row 64 (1 interval, 3.9-5 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 65 (1 interval, 5-5.7 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] rows 66-68 (3 intervals, 5.7-11.6 m, `GLU000ATIV`): « Calcaire grossier supérieur d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 69 (1 interval, 11.6-14 m, `GLU000ATJG`): « Banc vert d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 70 (1 interval, 14-26.8 m, `GLU000ATIV`): « Calcaire grossier moyen d'Ile-de-France » → « Lutétien moyen »
- [ ] row 71 (1 interval, 26.8-27 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »

**BSS000NUKM** - `BSS000NUKM.png`, rows 72-78

- [ ] row 72 (1 interval, 0-4.6 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] row 73 (1 interval, 4.6-5.6 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 74 (1 interval, 5.6-6.5 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 75 (1 interval, 6.5-14.6 m, `GLU000ATIV`): « Calcaire grossier supérieur d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 76 (1 interval, 14.6-16.8 m, `GLU000ATJG`): « Banc vert d'Ile-de-France » → « Lutétien supérieur »
- [ ] row 77 (1 interval, 16.8-29.7 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] row 78 (1 interval, 29.7-30 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »

**BSS000NUSX** - `BSS000NUSX.png`, rows 79-81

- [ ] row 79 (1 interval, 0-3 m, `GLU000AAAA`): *(formation empty; lithology « Sous sol »)* → *(no stage)*
- [ ] row 80 (1 interval, 3-7.5 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] row 81 (1 interval, 7.5-24.5 m, `GLU000AAAA`): *(formation empty; lithology « Calcaire »)* → « Lutétien »

**BSS000NZWP** - `BSS000NZWP.png`, rows 82-83

- [ ] row 82 (1 interval, 0-10.5 m, `GLU000AEKR`): « Fy-z » → « Holocène »
- [ ] row 83 (1 interval, 10.5-16.5 m, `GLU000ATIT`): « Marnes et caillasses lutétiennes inférieures » → « Lutétien supérieur »

**BSS000NXAD** - `BSS000NXAD.png`, rows 116-121

- [ ] rows 116-117 (2 intervals, 0-19.56 m, `GLU000AAVG`): « Remblais » → « Holocène » - *printed lithology « Remblais et marnes et caillasses (Lutétien)? »*
- [ ] row 118 (1 interval, 19.56-23.7 m, `GLU000AAAA`): *(formation empty; lithology « Ensemble indifférencié comprenant de haut en bas les marnes et caillasses et les calcaires grossiers »)* → « Lutétien »
- [ ] row 119 (1 interval, 23.7-53.96 m, `GLU000AAAA`): *(formation empty; lithology « Sable et argile »)* → « Yprésien »
- [ ] row 120 (1 interval, 53.96-63.3 m, `GLU000ATRI`): « Marnes de Meudon » → « Sélandien »
- [ ] row 121 (1 interval, 63.3-150.7 m, `GLU000ATVX`): « Craie à silex » → « Campanien »

**BSS000NYRW** - `BSS000NYRW.png`, rows 122-147 - *the most displaced image: 26 intervals, labels with call-out lines*

- [ ] rows 122-123 (2 intervals, 0-6.8 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] rows 124-128 (5 intervals, 6.8-21 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 129 (1 interval, 21-43.2 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] rows 130-132 (3 intervals, 43.2-50.8 m, `GLU000ATLY`): « Sables du Soissonnais (terme de sondeur) » → « Cuisien »
- [ ] row 133 (1 interval, 50.8-53.4 m, `GLU000ATMW`): « Fausses glaises du Vexin » → « Sparnacien »
- [ ] rows 134-135 (2 intervals, 53.4-60.4 m, `GLU000ATND`): « Sables d'Auteuil » → « Sparnacien »
- [ ] rows 136-145 (10 intervals, 60.4-77.8 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »
- [ ] row 146 (1 interval, 77.8-87.3 m, `GLU000ATRI`): « Marnes de Meudon » → « Sélandien »
- [ ] row 147 (1 interval, 87.3-135 m, `GLU000ATVX`): « Craie à silex » → « Campanien »

**BSS000NTGZ** - `BSS000NTGZ.png`, rows 148-157

- [ ] row 148 (1 interval, 0-3.8 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] row 149 (1 interval, 3.8-7 m, `GLU000AEKR`): « Fy-z » → « Holocène »
- [ ] row 150 (1 interval, 7-10.4 m, `GLU000ATIN`): « Marnes et caillasses lutétiennes » → « Lutétien supérieur »
- [ ] row 151 (1 interval, 10.4-28.5 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] row 152 (1 interval, 28.5-37.6 m, `GLU000ATLW`): « Sables de Cuise » → « Cuisien »
- [ ] row 153 (1 interval, 37.6-41.5 m, `GLU000ATMW`): « Fausses glaises du Vexin » → « Sparnacien »
- [ ] row 154 (1 interval, 41.5-50 m, `GLU000ATND`): « Sables d'Auteuil » → « Sparnacien »
- [ ] row 155 (1 interval, 50-65.6 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »
- [ ] row 156 (1 interval, 65.6-72 m, `GLU000ATRI`): « Marnes de Meudon » → « Sélandien »
- [ ] row 157 (1 interval, 72-78.65 m, `GLU000ATVX`): « Craie à silex » → « Campanien »

**BSS000NTWA** - `moisson/logs-valides/BSS000NTWA.png`, rows 158-195 - *harvested on 24/09 for this folder; never read by anyone else; the lithology texts are illegible there, the Formation and Stratigraphie columns legible*

- [ ] rows 158-159 (2 intervals, 0-8 m, `GLU000AAVG`): « Remblais » → « Holocène »
- [ ] row 160 (1 interval, 8-9 m, `GLU000BIOG`): « Fy-Seine » → « Pléistocène supérieur »
- [ ] rows 161-169 (9 intervals, 9-17 m, `GLU000ATIV`): « Calcaire grossier s.l. d'Ile-de-France » → « Lutétien »
- [ ] rows 170-176 (7 intervals, 17-24.7 m, `GLU000ATJT`): « Calcaire et sables à Nummulites laevigatus » → « Lutétien inférieur »
- [ ] rows 177-178 (2 intervals, 24.7-26.8 m, `GLU000ATLW`): « Sables de Cuise » → « Cuisien »
- [ ] rows 179-181 (3 intervals, 26.8-35.2 m, `GLU000ATLY`): « Sables du Soissonnais (terme de sondeur) » → « Cuisien »
- [ ] rows 182-186 (5 intervals, 35.2-40.5 m, `GLU000ATMW`): « Fausses glaises du Vexin » → « Sparnacien »
- [ ] row 187 (1 interval, 40.5-45.3 m, `GLU000ATND`): « Sables d'Auteuil » → « Sparnacien »
- [ ] rows 188-194 (7 intervals, 45.3-59.3 m, `GLU000ATNX`): « Argile plastique » → « Sparnacien »
- [ ] row 195 (1 interval, 59.3-60 m, `GLU000ATRI`): « Marnes de Meudon » → « Sélandien »

For the first 10, this reading is the **second** one: it reproduces, box by box,
the reading made by the agent of the first harvest. Two readers agreeing on the
same image do not make a proof - hence this list. For NXAD, NYRW, NTGZ, the
first harvest's notes gave only the tops of the Craie and of the Marnes de
Meudon and the code → stage table; NTWA had never been read.

### 2. The record-sheet rows - 6 boreholes, 32 rows (84-115)

Not an image, but a transcription of HTML (`niveaux-fiches.csv`, marked *« à
relire »* in the first harvest's notes), found again here by a second reader to
within a blank. To tick: the link of the record-sheet mnemonics to GeolTs.

- [ ] rows 84-86, **BSS000NSYT**: `IMPRECIS` → no stage; `QUATERNAIRE` → 1289 Quaternaire; `EOCENE-MOYEN` → 1254 Eocène moyen
- [ ] rows 87-90, **BSS000NZNM**: `QUATERNAIRE` → 1289; `LUTETIEN-SUP` → 1258 Lutétien supérieur; `LUTETIEN-INF` → 1256 Lutétien inférieur
- [ ] rows 91-93, **BSS000NZNP**: `QUATERNAIRE` → 1289; `LUTETIEN-SUP` → 1258
- [ ] rows 94-105, **BSS000NVHN**: 12 levels, **no stage** (free text not read; open question)
- [ ] rows 106-110, **BSS003CIKC**: 2 levels without a stage; `LUTETIEN` → 1255 Lutétien (×3)
- [ ] rows 111-115, **BSS003CIKW**: same as CIKC, level for level

### 3. Three decisions taken here, to confirm

- [ ] **`IMPRECIS` outside the `etage` column** (NSYT row 84): the instruction
  received files it with the intervals without a stage, so `etage` is empty and
  the word is in the note. The Lutetia model wants it *« refusé par son nom »*
  (refused by name): as it stands, the import counts it among the intervals
  without a unit **without being able to name it**. The other choice: write
  `IMPRECIS` in `etage` (which is what the record sheet says), the `geolts_*`
  columns staying empty.
- [ ] **NSYW 0-8.6 m without a stage** although the record sheet says
  `QUATERNAIRE`: (A) takes precedence and does not date these intervals; (B) is
  not used to fill in (A).
- [ ] **NVHN present with its record-sheet bounds and without a stage**, rather
  than absent: the fallback for boreholes without intervals may give it stages
  read off the horizons; its record-sheet bounds, for their part, are facts.
