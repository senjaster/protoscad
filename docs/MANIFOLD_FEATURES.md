# New language features unlocked by Manifold

ProtoSCAD sits on manifold3d, which can do things OpenSCAD's engine cannot.
This document proposes language features built on those capabilities, filtered
through the language's own design rules. Companion to
[MISSING_FEATURES.md](MISSING_FEATURES.md).

## The filter a proposal must pass

1. **A module maps one geometry to one geometry.** A call receives the single
   geometry of its children (or their implicit union) and returns one geometry
   for its parent. OpenSCAD's tree model is built on this contract; features
   that produce several addressable results or select among results have no
   consumer in the language.
2. **The expression language has no geometry values.** Measurements (volume,
   bounds, gaps) cannot be exposed to expressions — there is nothing to apply
   them to. They are only useful where a module consumes them *internally* to
   produce geometry. OpenSCAD's `resize` is the precedent: it measures the
   children and acts on the result, which is why it exists while `volume()`
   does not.
3. **Function-valued parameters wait for user-defined functions**
   (MISSING_FEATURES.md #4). Until then, deformations ship as parameterized
   builtin modules.

Every item below passes all three unless explicitly marked otherwise.

## Features that fit the language today

Each is a `BuiltinModule` in the existing `builtins/` registry — no grammar
changes.

### `offset3d(delta [, element])` — Minkowski erosion and dilation

`Manifold.minkowski_sum` / `Manifold.minkowski_difference`. Positive delta
dilates by `element` (default: sphere of |delta|), negative delta erodes — the
3D analogue of OpenSCAD's 2D `offset()`. The existing `minkowski` module
already covers the explicit-element sum, so this completes the family.

What it unlocks in normal modeling:

- **shells**: `difference() { original; offset3d(-t) original; }` — hollowing
  with exact wall thickness
- **clearance insets**: shrink a part by the fit tolerance for printed fits
- **edge rounding**: `offset3d(-r) offset3d(r) part` (dilate-then-erode =
  morphological closing) rounds convex edges; the reverse order fillets
  concave ones. These chains are the 3D `offset`-rounding idiom that OpenSCAD
  cannot express at all.

### `trim_by_plane(normal, offset)` — cut with an infinite plane

`Manifold.trim_by_plane` keeps the single half of the children behind the
plane `normal · x = offset`. No giant cutting cube, no `difference`. Want both
halves? Call it twice with a negated normal — the tree model evaluates each
branch separately, so that is the *correct* usage, not a workaround. (This is
why `split_by_plane`, which returns two solids, was rejected: the second
result has no addressable place in the language.)

### `smooth(n)` — subdivision smoothing of any solid

`Manifold.smooth_out(min_sharp_angle)` computes edge tangents;
`Manifold.refine(n)` subdivides for interpolation (`refine_to_length` /
`refine_to_tolerance` are adaptive variants). A `smooth(iterations)` module
rounds any mesh — user polyhedra and imported STLs included. Organic shaping
and cleanup of voxelated imports, neither possible in OpenSCAD.

### `center()` — a measurement feature that fits rule 2

`Manifold.bounding_box` measured inside the module, `translate` to move the
bbox center to the origin. This is what "measurement" looks like in a language
without geometry values: consumed internally, one geometry out. The general
OpenSCAD-idiom version of per-primitive `center = true`, and the thing library
authors fake today with the `%`-hull bounding-box visualization trick (which
only *shows* the box). `resize` (MISSING_FEATURES.md #11) is the sibling of
this item.

### `twist` / `bend` / `taper` — parameterized warps

`Manifold.warp(fn)` displaces vertices while preserving topology, and Manifold
validates the result (`status`), so a non-injective map errors instead of
corrupting. Parameterized builtin versions need no language support:

- `twist(degrees, [axis])` — rotation proportional to height (OpenSCAD only
  twists inside `linear_extrude`, at extrusion time, not on existing solids)
- `bend(axis, radius)` — wrap a flat part around a cylinder
- `taper(scale_start, scale_end, [axis])`

Arbitrary user-supplied `warp(fn)` waits for functions (rule 3).

### `simplify(tolerance)` — mesh decimation

`Manifold.simplify(tol)` decimates triangles. Minkowski and smooth results can
be heavy; useful as a module and as a `--simplify` flag on the STL export path.

### `polyhedron(points, faces)` and `hull_points(pts)`

The data-to-geometry leaf category: modules whose parameters are *values*
(vectors of points), producing one geometry — the same shape as OpenSCAD's
`polyhedron`, which is MISSING_FEATURES.md parity and falls out of
`manifold3d.Mesh` + the `triangulate` helper. `hull_points` is the hull of a
bare point list (the no-tiny-spheres version of a common hack); same
category, lower priority.

## With the 2D workstream (MISSING_FEATURES.md #5)

- `Manifold.slice(height)` and `Manifold.project()` are exactly
  `projection(cut = true/false)` — parity for free once 2D geometry exists.
- `CrossSection.offset` supports `JoinType.Round/Miter/Square`; Square join is
  beyond OpenSCAD's `offset(r, delta, chamfer)`.

## `level_set` used internally: implicit modeling without exposing SDFs

`Manifold.level_set(f, bounds, edge_length, level)` builds a manifold from a
signed-distance function (marching tetrahedra on a body-centered cubic grid —
manifoldness guaranteed; sign convention: *positive inside*). It takes a
*callable*, which the language does not have — so it is never exposed raw.
Instead the interpreter synthesizes the field itself, either from **data** the
language already holds (vectors of numbers) or from the **geometry of
children** (mesh → sampled distance grid). In both forms the user never writes
a function or bounds: the module computes the grid extent from its inputs
(union of input bboxes, padded by the blend radius), and `edge_length` follows
a resolution parameter (candidate default: `$fs`-aware). The `level` parameter
is free inset/outset.

### `metaballs([[x,y,z,r], ...], blend = 2, resolution)` — field from data

Status: **implemented** (`builtins/metaballs.py`, `tests/test_metaballs.py`).
Positional order is `balls, blend, resolution`; `resolution` defaults to the
`$fs` visible at the call (the same "minimum detail size" variable the curved
primitives read), and Manifold's field convention there is *positive inside*.

Smooth-min over sphere SDFs (optional capsule entries `[x1,y1,z1,x2,y2,z2,r]`
for limb chains), bounds = union of the balls padded by `blend`. A leaf module
in the polyhedron/`hull_points` category: parameters are values, one geometry
out. Use cases: organic multi-lobe shapes (handles, pebbles, pads) and fillet
blobs at primitive junctions. Verified against manifold3d 3.5.4: three balls at
0.5 mm edge length → valid manifold, ~81k triangles, 0.78 s (Python-field
callback; cost scales with ball count × grid points).

### `blend(k) { a; b; ... }` — field from children

The generalization: smooth-min over the *distance fields of arbitrary solids*.
Each child mesh is sampled once onto a grid (nearest-point query with
winding-number sign, e.g. via trimesh proximity on the watertight manifold
mesh); grids are smooth-minned; `level_set` is then driven by a cheap
trilinear-interpolation callable so the expensive distance queries run once in
vectorized form, not once per marching-tetrahedra evaluation. Payoff: organic
filleted unions between arbitrary parts (a shaft blending into a flange,
cylinders melting into a box) — unmodelable in OpenSCAD without page-long
minkowski/hull tricks. Honest costs: resolution-limited (voxel size parameter)
and one-time grid sampling — but the limit matches 3D-print resolution anyway.

### `voxels(matrix, voxel_size, iso)` — field from a 3D matrix

A 3D density field → iso-surface, bounds from the matrix dimensions. Pure
value-parameter leaf. The data shape decides the tool: **2D height data (a
height map, OpenSCAD's `surface()`) must NOT go through `level_set`** — it is
O(W·H·D) marching evaluations plus per-point callback cost to reconstruct what
is already an explicit graph surface, and the snapped, smoothed result breaks
`surface()`'s piecewise-linear pixel-exact parity. A height map is a direct
`Mesh` construction (vertex per pixel, two triangles per quad, side walls,
bottom cap — the `polyhedron` machinery, O(W·H), exact). Marching is for
**3D** density data, where there is no direct mesh to build. (If a terrain
should *blend* organically with other solids, that is an implicit-composition
feature on top of `surface` parity, not a replacement for it.)

The synergy: once list comprehensions land (MISSING_FEATURES.md #7), a
comprehension *is* a user-function materialized as data —

```
voxels([for (x = [-5:5]) [for (y = [-5:5]) [for (z = [-5:5])
    sqrt((x-2)^2 + y^2 + z^2) - 3 ]]]);
```

— so SDF-style procedural modeling arrives in pure declarative OpenSCAD idiom,
with no function-call syntax. Caveat: one interpreter evaluation per cell, so
gradients-heavy work stays at modest grid sizes until evaluation is
vectorizable. (A builtin noise/`terrain` variant is a trivial parameterized
showcase on the same machinery.)

## Explicitly rejected — do not fit the language model

Recorded so they are not re-proposed by accident:

- **`split`/`split_by_plane` as a two-result module** — a second solid cannot
  be addressed; `trim_by_plane` called twice is the correct tree-model usage.
- **`separate()` / `keep_largest()` / component selection** — "which
  component" is a question the language cannot ask; there is no way to name
  the second smallest piece or route components to different operations.
- **`measure()` / `clearance()` echo modules** — numbers with no consumer;
  measurements only matter when something acts on them (`center()`, `resize`)
  or when geometry becomes a value.

## Deferred until the prerequisites land

- **`warp(fn)` with user functions** — arbitrary vertex displacement needs
  functions in expression position (the parameterized `twist`/`bend`/`taper`
  above need none). Raw SDF exposure (`level_set(sdf, ...)`) additionally
  needs a bounds story; until then `level_set` stays internal (section above).
- **Measurement functions in expressions** (`volume`, `bbox`, `min_gap`) —
  geometry-as-value, the seam named in the "Future" section of NAMESPACES.md.
- **Position-driven color via `Manifold.set_properties`** — rides along with
  `color()` (MISSING_FEATURES.md #10): same vertex-property overlay mechanism;
  two-color gradients are parameterizable without user functions.

## Suggested ordering

`offset3d` → `trim_by_plane` → `smooth` → `center` → `twist`/`bend`/`taper` →
`polyhedron` → `metaballs` (same leaf machinery) → `simplify`/CLI →
`hull_points`, then `blend` (reuses the mesh handling of `smooth`) and
`voxels` (shines once comprehensions land), with the `$fn` setter mapping
folded into MISSING_FEATURES.md #2. The headline is `offset3d`: Minkowski
difference alone delivers shells, fits, and rounding chains that OpenSCAD
approximates with page-long CSG or cannot do at all — and here it is one
method call.
