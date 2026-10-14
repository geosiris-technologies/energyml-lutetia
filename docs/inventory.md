# Inventory

> **Generated** by `scripts/inventory.py` from `package/Lutetia.epc`. Do not edit by hand: CI regenerates this file and fails if it differs.

Objects are counted from the part names (`<Type>_<uuid>.xml`) and checked against the root element of each part; the schema version is the `schemaVersion` attribute of that element.

- Data objects: **1302**
- Distinct object types: **67**
- Relationship parts (`.rels`): 1312
- Other parts (attachments, properties, content types): 11

## By standard and schema version

| Standard | Schema version | Objects |
|---|---|---:|
| EML (common) | 2.3 | 286 |
| PRODML | 2.3 | 24 |
| RESQML | 2.2 | 932 |
| WITSML | 2.1 | 60 |

## By type

| Standard | Schema version | Type | Objects |
|---|---|---|---:|
| EML (common) | 2.3 | `Activity` | 106 |
| EML (common) | 2.3 | `ActivityTemplate` | 48 |
| EML (common) | 2.3 | `Attachment` | 4 |
| EML (common) | 2.3 | `BusinessAssociate` | 2 |
| EML (common) | 2.3 | `CollectionsToDataobjectsAssociationSet` | 30 |
| EML (common) | 2.3 | `ColumnBasedTable` | 11 |
| EML (common) | 2.3 | `DataobjectCollection` | 47 |
| EML (common) | 2.3 | `GraphicalInformationSet` | 4 |
| EML (common) | 2.3 | `LocalEngineering2dCrs` | 2 |
| EML (common) | 2.3 | `LocalEngineeringCompoundCrs` | 4 |
| EML (common) | 2.3 | `ProjectedCrs` | 1 |
| EML (common) | 2.3 | `ReferencePointInALocalEngineeringCompoundCrs` | 23 |
| EML (common) | 2.3 | `TimeSeries` | 3 |
| EML (common) | 2.3 | `VerticalCrs` | 1 |
| PRODML | 2.3 | `DtsInstalledSystem` | 1 |
| PRODML | 2.3 | `DtsInstrumentBox` | 1 |
| PRODML | 2.3 | `DtsMeasurement` | 1 |
| PRODML | 2.3 | `Facility` | 1 |
| PRODML | 2.3 | `FiberOpticalPath` | 1 |
| PRODML | 2.3 | `FluidCharacterization` | 1 |
| PRODML | 2.3 | `FluidSample` | 1 |
| PRODML | 2.3 | `FluidSampleAcquisitionJob` | 1 |
| PRODML | 2.3 | `FluidSampleContainer` | 1 |
| PRODML | 2.3 | `FluidSystem` | 1 |
| PRODML | 2.3 | `InjectionFlowTest` | 1 |
| PRODML | 2.3 | `PressureTransientAnalysis` | 1 |
| PRODML | 2.3 | `ProductFlowModel` | 1 |
| PRODML | 2.3 | `ProductionWellTests` | 1 |
| PRODML | 2.3 | `ReportingEntity` | 3 |
| PRODML | 2.3 | `TimeSeriesData` | 3 |
| PRODML | 2.3 | `TimeSeriesStatistic` | 1 |
| PRODML | 2.3 | `WaterAnalysis` | 1 |
| PRODML | 2.3 | `WellProductionParameters` | 2 |
| RESQML | 2.2 | `BlockedWellboreRepresentation` | 2 |
| RESQML | 2.2 | `BoundaryFeature` | 41 |
| RESQML | 2.2 | `BoundaryFeatureInterpretation` | 1 |
| RESQML | 2.2 | `ContinuousColorMap` | 1 |
| RESQML | 2.2 | `ContinuousProperty` | 69 |
| RESQML | 2.2 | `CulturalFeature` | 2 |
| RESQML | 2.2 | `DiscreteProperty` | 449 |
| RESQML | 2.2 | `EarthModelInterpretation` | 2 |
| RESQML | 2.2 | `FaultInterpretation` | 4 |
| RESQML | 2.2 | `GenericFeatureInterpretation` | 2 |
| RESQML | 2.2 | `GeologicUnitOccurrenceInterpretation` | 2 |
| RESQML | 2.2 | `Grid2dRepresentation` | 9 |
| RESQML | 2.2 | `HorizonInterpretation` | 38 |
| RESQML | 2.2 | `IjkGridRepresentation` | 3 |
| RESQML | 2.2 | `LocalGridSet` | 1 |
| RESQML | 2.2 | `Model` | 4 |
| RESQML | 2.2 | `NonSealedSurfaceFrameworkRepresentation` | 1 |
| RESQML | 2.2 | `PointSetRepresentation` | 26 |
| RESQML | 2.2 | `PolylineSetRepresentation` | 6 |
| RESQML | 2.2 | `RockVolumeFeature` | 53 |
| RESQML | 2.2 | `StratigraphicColumn` | 3 |
| RESQML | 2.2 | `StratigraphicColumnRankInterpretation` | 13 |
| RESQML | 2.2 | `StratigraphicUnitInterpretation` | 53 |
| RESQML | 2.2 | `StructuralOrganizationInterpretation` | 3 |
| RESQML | 2.2 | `SubRepresentation` | 1 |
| RESQML | 2.2 | `TriangulatedSetRepresentation` | 7 |
| RESQML | 2.2 | `WellboreFeature` | 24 |
| RESQML | 2.2 | `WellboreFrameRepresentation` | 44 |
| RESQML | 2.2 | `WellboreInterpretation` | 24 |
| RESQML | 2.2 | `WellboreTrajectoryRepresentation` | 44 |
| WITSML | 2.1 | `Log` | 7 |
| WITSML | 2.1 | `Trajectory` | 18 |
| WITSML | 2.1 | `Well` | 17 |
| WITSML | 2.1 | `Wellbore` | 18 |

## Consistency

Part names and root elements agree for every object.
