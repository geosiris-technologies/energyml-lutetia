# Coverage

What Lutetia contains, and, as important, what it does not. Counts come from [inventory.md](inventory.md), which is generated from the package.

## Types by standard and version

Lutetia is written in **one version per standard**: RESQML 2.2, Energistics common (EML) 2.3, WITSML 2.1, PRODML 2.3. It contains 67 object types; the matrix has a single populated column per row, by design.

| Standard | Version | Types present |
|---|---|---|
| RESQML | 2.2 | `BlockedWellboreRepresentation`, `BoundaryFeature`, `BoundaryFeatureInterpretation`, `ContinuousColorMap`, `ContinuousProperty`, `CulturalFeature`, `DiscreteProperty`, `EarthModelInterpretation`, `FaultInterpretation`, `GenericFeatureInterpretation`, `GeologicUnitOccurrenceInterpretation`, `Grid2dRepresentation`, `HorizonInterpretation`, `IjkGridRepresentation`, `LocalGridSet`, `Model`, `NonSealedSurfaceFrameworkRepresentation`, `PointSetRepresentation`, `PolylineSetRepresentation`, `RockVolumeFeature`, `StratigraphicColumn`, `StratigraphicColumnRankInterpretation`, `StratigraphicUnitInterpretation`, `StructuralOrganizationInterpretation`, `SubRepresentation`, `TriangulatedSetRepresentation`, `WellboreFeature`, `WellboreFrameRepresentation`, `WellboreInterpretation`, `WellboreTrajectoryRepresentation` |
| EML (common) | 2.3 | `Activity`, `ActivityTemplate`, `Attachment`, `BusinessAssociate`, `CollectionsToDataobjectsAssociationSet`, `ColumnBasedTable`, `DataobjectCollection`, `GraphicalInformationSet`, `LocalEngineering2dCrs`, `LocalEngineeringCompoundCrs`, `ProjectedCrs`, `ReferencePointInALocalEngineeringCompoundCrs`, `TimeSeries`, `VerticalCrs` |
| WITSML | 2.1 | `Log`, `Trajectory`, `Well`, `Wellbore` |
| PRODML | 2.3 | `DtsInstalledSystem`, `DtsInstrumentBox`, `DtsMeasurement`, `Facility`, `FiberOpticalPath`, `FluidCharacterization`, `FluidSample`, `FluidSampleAcquisitionJob`, `FluidSampleContainer`, `FluidSystem`, `InjectionFlowTest`, `PressureTransientAnalysis`, `ProductFlowModel`, `ProductionWellTests`, `ReportingEntity`, `TimeSeriesData`, `TimeSeriesStatistic`, `WaterAnalysis`, `WellProductionParameters` |

## Functions exercised

Each is produced by a recipe step ([build.md](build.md)): coordinate reference systems (projected, vertical, local, compound; depth and time axes); stratigraphic column and units from an external chart; wellbores from real boreholes and from planned trajectories (vertical, deviated, horizontal, sidetrack); wellbore frames with properties and units; blocked wellbores; surfaces as 2D grids, point sets and triangulated sets; faults, structural organisation and a surface framework; an IJK grid with a K gap, a local refined grid and a sub-representation; continuous and discrete properties, lookup tables, property time series; colour maps and graphical information; collections, attachments (parts of the package) and activities with templates; WITSML wells, trajectories and logs; PRODML production, fluid, DTS, injection test and flow model; export attachments (OBJ, GeoJSON, VTU); a section view.

## What Lutetia does not cover

Compared with the reference packages used elsewhere in the test suite of `energyml` (written by other tools), Lutetia lacks about 25 types, among them:

- `UnstructuredGridRepresentation`, `GridConnectionSet`
- `PlaneSetRepresentation`, `PointsProperty`
- `SealedSurfaceFrameworkRepresentation`, `RepresentationSet`
- local `PropertyKind` objects, `PropertySet`, `DiscreteColorMap`
- seismic objects (`SeismicLatticeFeature` and related)
- `Geobody` and rock-fluid objects
- `WellboreMarker`, `WellboreCompletion`, `WellboreGeometry`

It also has **no RESQML 2.0.1**, no earlier version of any standard, and no mixed-version package.

Two limits of principle:

- Lutetia is **written by the `energyml` library itself**. Reading it back with the same library asks the library to check itself. It covers the functions, **not interoperability**.
- The recipe's `grilles-craie` and `h2` steps are on hold (see [build.md](build.md)), so a representation set and a top-of-Lutetian surface are absent.

## Where the rest is covered

Interoperability and RESQML 2.0.1 are covered in the `energyml` repository by packages written by other tools, pinned by commit and checksum and downloaded in CI only: the example packages of the FESAPI-based programme (RESQML 2.0.1 and 2.2) and the examples of RESQML-py (2.0.1). The missing types above appear in those packages. Edge cases and refusals are covered by data built inside the tests. `TODO(verify)`: replace this paragraph with links to the final `tests/fixtures.lock` of `energyml-rust` once it exists.
