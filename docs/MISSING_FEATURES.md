# Missing features vs OpenSCAD, by priority

A gap analysis of ProtoSCAD against the official OpenSCAD 2021.01 feature set
(cheat sheet), verified with live probes through the interpreter.

## What already exists

3D primitives `cube`/`sphere`/`cylinder`; booleans `union`/`difference`/`intersection`;
transforms `translate`/`rotate`/`scale`/`mirror`; `hull`, `minkowski`, `for`,
`intersection_for`, `let`; user modules with named/`$`-args, indexed `children(i)`,
bare and vector `children()` selection, and the `$children` count; user variables
with two scoping dialects (`DeclarativeResolver`, `OpenScadResolver`); the full
math/vector builtin function set; `.x/.y/.z` accessors; STL export.

The engine (manifold3d) also ships 2D `CrossSection` support, which matters for
priority 4 below.

The 2D pipeline has started and is now broad: `square`, `circle(r|d)`,
`polygon(points, paths)` produce planar `CrossSection` geometry;
`offset(r|delta, chamfer)` grows/shrinks it; `linear_extrude` and
`rotate_extrude(angle)` turn it into solids; `projection(cut)` goes the
other way (Manifold `slice`/`project`); and `union`/`difference`/
`intersection`, `hull`, `translate`/`rotate`/`scale`/`mirror`/`resize`/
`multmatrix` are all dimension-aware (details in item 4).

`if` / `else` statements exist: the grammar lowers the construct to an `if`
module call whose children are exactly the branches — the true branch, then
the false branch, each one implicit-union scope. `IfModule` is therefore an
ordinary module: it evaluates child 0 or child 1 and nothing else. Works as
a statement, in module-call chains (`for(...) if(...) ...`), with `else if`
ladders and C-style innermost dangling-else binding.

`$fn`/`$fa`/`$fs` resolve the fragment count for `sphere` and `cylinder` via
OpenSCAD's `get_fragments_from_r` rule (see `builtins/_fragments.py`). The
sphere keeps manifold's tetrahedron-refinement construction — the resolved
count only steers how fine that refinement gets.

`echo()` and `assert()` exist in the module form as plain builtin modules
(`builtins/echo.py`, `builtins/assertion.py`) — ordinary registry entries
alongside `cube`, with no grammar support. `echo` prints `ECHO: ` lines in
OpenSCAD console format (quoted strings, `name = value` bindings) and
passes children through; with no children it contributes no geometry.
`assert(condition, message?)` raises `assertion-failed` with the assert's
span (message printed the way `echo` shows values, "Assertion failed"
without one) and is likewise a pass-through scope for children, so it can
guard a user module. Unlike OpenSCAD, the words are not reserved: `echo`
and `assert` are ordinary identifiers (a user module of the same name
shadows the builtin). The expression forms (`x = assert(cond) value;`,
`y = echo("dbg") x + 1;` — OpenSCAD's `expr_or_empty` prefixes) are not
implemented: in expression position the calls resolve as unknown functions.
They are worth adding together with user-defined functions (item 3), whose
bodies are where library code uses them.

## Tier 1 — blocks real-world CSG models

### 3. User-defined functions

`function f(x) = x + 1;` is a syntax error, and expression calls resolve only
against the builtin registry (`tree/expression.py`, `Call.evaluate`). Function
literals (`f = function(x) x + 2;`) are 2021.01 features. Many community
libraries use functions heavily. [NAMESPACES.md](NAMESPACES.md) already
contains the full design (kind-slot storage, callable-variable-wins priority,
verified probes) — this is a designed-but-unstarted item. The `echo`/`assert`
expression forms (the former item 2, shipped module-only) fold naturally into
this work: they are grammar prefixes over an argument list, like `let`.

### 4. 2D primitives and the extrusion pipeline

The stream is nearly complete. On the `square` + `linear_extrude` base (see
git history for the details: OpenSCAD slice-count rules ported verbatim,
`GeometryError` located at the innermost call by `Invocation`), these have
landed since, all against manifold3d's `CrossSection`:

- `circle(r|d)` — the OpenSCAD fragment rule picks the polygon (`circle(1)`
  is the default pentagon), manifold draws it.
- `polygon(points, paths)` — contours fill by winding (holes are
  oppositely-wound paths, OpenSCAD's convention); out-of-bounds indices
  and non-pair points are located `invalid-argument` errors where OpenSCAD
  warns and skips.
- `offset(r|delta, chamfer)` — OpenSCAD's offset.cc reading: `r` rounds
  (arc segments sized by `$fa`/`$fs`), `delta` miters, `delta` +
  `chamfer` squares the corners, `r` wins over `delta`, bare `offset()` is
  `r = 1`.
- `rotate_extrude(angle, convexity)` — `CrossSection.revolve`; the
  fragment budget comes from the profile's x-span scaled by angle/360 (the
  OpenSCAD rule), out-of-range angles clamp to a full turn, a profile
  straddling the axis is an error, an all-negative-x profile is mirrored
  first (OpenSCAD revolves `|x|`; Manifold only accepts positive x), and
  negative angles revolve `|angle|` then mirror — Manifold returns an
  inside-out solid for negative degrees.
- `projection(cut)` — `cut=true` is `Manifold.slice(0)`; the default is
  `Manifold.project()` re-run through the positive fill rule (Manifold's
  projected outline can self-intersect).
- 2D dispatch in `hull` (`CrossSection.batch_hull`), `resize` (bounds +
  2-axis scale), and `multmatrix` (the 4x4's in-plane 2x3).

Still true from the first cut of this stream: manifold3d's `CrossSection`
is a peer geometry kind flowing through the ordinary module tree — shared
boolean/union helpers (implicit scopes, `for`, `intersection_for`, `let`)
dispatch on it, mixing 2D and 3D children in one operation is a located
`type-error` where OpenSCAD warns and drops, `linear_extrude`'s default
slice count is the verbatim calc.cc port (`builtins/_fragments.py`), and
at the CLI a 2D top level previews flat in the mesh viewer and exports
`.svg`/`.dxf` (a dimension/format mismatch is `export-format-mismatch`).

Remaining in this workstream: `text` (font shaping — deliberately deferred)
and 2D `minkowski` (no Manifold API; would need an offset-convolution
implementation). SVG/DXF *import* belongs to the `include`/`import`
workstream (item 8/9).

### 5. `children()` with a range

The bare form (`children()` = all children), vector selection
(`children([0, 2])`, order and repeats kept), and the `$children` count are
in. `$children` binds as a constant in the module body scope
(`ModuleClosure.instantiate`), so call arguments still see the caller's `$`
bindings and a nested module call shadows it with its own count (0 for a
bare call). Binding it flushed out a pre-existing scoping bug, fixed along
the way: sibling top-level modules — and a module recursing into its own
name — were unresolvable from a module body, because `ModuleClosure`
captured its definition scope before the sibling modules were registered;
`Invocation.build_child_scope` now re-points the closures at the finished
scope. Remaining: `children([0:1])` — `ChildrenModule` accepts scalars and
vectors only, so a range argument currently selects nothing.

## Tier 2 — common in existing .scad libraries

### 7. List comprehensions

`[for (i = [0:3]) i]` is a syntax error. Needed forms: `[for ...]`,
`[each ...]`, `[if ... else ...]`, `let` inside comprehensions, and the C-style
`for(init;cond;next)`. Required to port virtually any advanced library
(involute gears, BSplines). Grammar + a vector-valued evaluator path.

### 8. `include` / `use <file.scad>`

No import syntax at all. This is what makes libraries usable; the namespace
semantics (use = functions+modules, include = everything) are already
documented in [NAMESPACES.md](NAMESPACES.md). Natural prerequisite:
user-defined functions (item 3).

### 9. `import("file.stl")` and `surface()`

Mesh reuse. trimesh is already a dependency and can load STL/OFF/3MF into
something manifold accepts; probably the single easiest Tier 2 item.

### 10. `color()`

Least important for pure CSG, but note `render.py` *already handles* vertex
color channels from manifold (`manifold2trimesh` reads the 4-component
property buffer), so `color` is mostly a matter of threading an RGBA overlay
through child geometry. Keep it low, but it's cheaper than it looks.

### 11. `resize()`, `multmatrix()`, `render()` (no-op)

Cheap completeness items in the transform/operation registry; `multmatrix`
also becomes the internal implementation detail for other transforms.

### 12. Remaining builtin functions

`search()`, `lookup()`, `version()`, `version_num()`, `parent_module()`.
`search` is the only nontrivial one.

## Tier 3 — polish and parity

### 13. OpenSCAD variable semantics as the default dialect

The `OpenScadResolver` ("last definition + first position" rule, verified in
[QUIRKS.md](QUIRKS.md)) exists but the default is `DeclarativeResolver`, which
diverges on cases like `m=5; union() { y=m; m=1; }` (OpenSCAD: y=5, here: y=1).
Files from the wild assume the OpenSCAD rule; consider making it the default or
at least parameterizing tests over both, ahead of the NAMESPACES dialect work.

### 14. Modifier characters `* ! # %`

Disable / show-only / debug / transparent — grammar-level; matters once there
is a preview workflow.

### 15. `text()`

2D text needs font shaping; genuinely big, keep last among geometry.

### 16. Animation/camera special variables

`$t`, `$preview`, `$vpr/$vpt/$vpd/$vpf` — only meaningful with a GUI preview
loop; `$t` should at least be defined (currently referencing it errors) so
files referencing it parse.

### 17. Warning system

The project deliberately raises errors where OpenSCAD warns (unknown variable,
redefinition). Documented divergence; fine as long as it's intentional, but
real files often rely on `undef` semantics (e.g. guarded `is_undef(x)` on a
never-assigned name), which currently can't even evaluate.

## Suggested sequencing

**3 → 4 (continued)** (item 5 is done except the `children([0:1])` range
form, a few lines in `ChildrenModule`): functions and the 2D pipeline are
the two larger designed workstreams; 2D has `square` + `linear_extrude`
landed, with the primitive/extrusion list in item 4 left to go. (The
former item 2, `echo`/`assert`, shipped as ordinary builtin modules; its
expression forms fold into item 3.)

## Incidental observation

`builtin_functions.py` uses PEP 758's bare `except ValueError, OverflowError:`
— valid on the project's Python 3.14, so not a bug, but it will break anyone
backporting to ≤ 3.13.
