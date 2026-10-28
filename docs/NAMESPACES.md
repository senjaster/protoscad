# Namespaces and binding dialects

Status: **design, not implemented**. The probes below are verified against
real OpenSCAD (mirrored in [QUIRKS.md](QUIRKS.md)); everything else is the
agreed direction. Nothing here has landed in the code yet.

## Background

OpenSCAD keeps three separate namespaces — variables, functions, modules —
and picks one by grammatical position:

| Position | Namespace |
|---|---|
| expression atom `x` | variables |
| call in expression `x(...)` | functions, with a callable-variable override (see probes) |
| call statement `x(...);` | modules |

Coexistence is legal and unambiguous — the parser always knows which world
it is in:

```
x = 2;
function x(x) = x + 1;
module x(x) cube(x(x));  // x(x) inside is the FUNCTION
x(x);                    // statement position: the MODULE
```

The price is that modules and geometry cannot be stored in variables — the
single biggest expressiveness complaint about the language. The
single-namespace model (one name — one binding, the Python/JS/Julia route)
fixes that but forbids coexistence, so it is incompatible with OpenSCAD.
The goal of this document: support **both semantics as a dialect toggle**,
with OpenSCAD compatibility as the default.

## Verified OpenSCAD behavior

Function literals (OpenSCAD 2021+) already force a priority rule in
expression-call position:

```
f = function(x) x + 2;
function f(x) = x + 1;
echo(f(1));  // 3 — the VARIABLE holding a function literal WINS

f = 5;
function f(x) = x + 1;
echo(f(1));  // 2 — a non-callable variable does NOT shadow the function
```

Derived rule for a call in expression position:

1. if the name is bound in the variable namespace **and** holds a function
   literal — call that;
2. else the named function, if any;
3. else unknown-name error.

Not yet probed (worth a QUIRKS.md pass before this design lands):

- a callable variable in an outer scope vs a named function in an inner
  scope;
- a call textually *before* the function-literal binding (variables are
  evaluated at compile time, so the variable likely still wins).

Documented (manual, not probed): `use <lib.scad>` imports functions and
modules but **not** variables, while `include` imports everything — the
namespaces are also import granularity.

## Design

### Storage: one general substrate

`Environment` stores all bindings in one structure:

```python
class BindingKind(Enum):
    VALUE = auto()  # numbers, strings, vectors, function literals
    FUNCTION = auto()  # named function declarations
    MODULE = auto()  # builtins and ModuleClosures


bindings: dict[str, dict[BindingKind, Slot]]
```

Both dialects are views over this structure. OpenSCAD mode allows several
kinds under one name; single-namespace mode enforces the invariant *at most
one kind per name per scope*. Principle: **general storage, constrained
semantics via policy** — the scope chain, lazy forcing, `$`-variable
dynamic scoping and the resolver strategies are shared unchanged.
`lookup_module(name)` becomes `lookup(name, MODULE)` and so on; the public
`Environment` API barely moves.


### Three orthogonal axes

Name resolution decomposes into three independent policies; no mode enum
entangles them:

1. **Within-kind ordering** of variable definitions in a scope — the
   existing `BindingResolver` strategies (`DeclarativeResolver`,
   `OpenScadResolver`).
2. **Cross-kind coexistence** — this document's toggle.
3. **Call-position preference** when several kinds could answer — fixed by
   the probes: a callable variable outranks a named function.

### BindingPolicy

```python
class BindingPolicy(Protocol):
    def bind(self, scope: Scope, name: str, kind: BindingKind) -> None:
        """Validate (and record) that `name` gains a binding of `kind`."""

    def resolve(self, position: Position) -> tuple[BindingKind, ...]:
        """Kinds to consult for a name used in this grammatical position,
        in priority order."""
```

`OpenScadBindingPolicy`:

- `bind` writes the slot; kinds coexist.
- `resolve`: atom → `VALUE`; expression call → `VALUE` (only when it holds
  a function literal), then `FUNCTION`; statement → `MODULE`.
- Observable behavior identical to today's OpenSCAD.

`SingleNamespacePolicy`:

- `bind`: if a **different** kind already occupies the name **in the same
  scope**, raise `ProtoSCADError(code="name-kind-conflict")` with the span
  of the second definition. Same-kind redefinition follows the chosen
  `BindingResolver` unchanged.
- Cross-scope shadowing is allowed regardless of kind — a local `cube = 5`
  shadowing the builtin module is ordinary lexical shadowing, not an error.
- `resolve`: the name has at most one kind; using it in a position that
  expects another kind is a clean kind-mismatch error pointing at the use
  site (a name means one thing, so this is a type error, never ambiguity).
- Enforcement happens at **bind time**, not lookup time: diagnostics point
  at the offending definition, and dead conflicts cannot pass silently.

### Dialect object

```python
@dataclass(frozen=True)
class Dialect:
    resolver: BindingResolver
    binding: BindingPolicy


OPENSCAD = Dialect(OpenScadResolver(), OpenScadBindingPolicy())
SINGLE = Dialect(OpenScadResolver(), SingleNamespacePolicy())
```

`evaluate(root, modules, dialect=OPENSCAD)`; the CLI gains
`--dialect=openscad|single` (default `openscad` — compatibility is the
default). `Dialect` is the single configuration point for intentional
divergences; the documented `$fn` divergence is a candidate to move here
later.

New error code `name-kind-conflict`; see [ERROR_REPORTING.md](ERROR_REPORTING.md)
for the recipe (code, span at the second definition, span asserted in a
test).

## Implementation plan

Each step leaves the suite green; none depends on named functions or the
wider expression-language work landing first.

1. Refactor `Environment` to `dict[str, dict[BindingKind, Slot]]` storage —
   pure internal change, no behavior change.
2. Introduce `BindingPolicy` with `OpenScadBindingPolicy` reproducing
   current behavior (and the probe rule once named functions exist).
3. Add `SingleNamespacePolicy`, `Dialect`, the `name-kind-conflict` code.
4. Wire `--dialect` into the CLI.
5. Parameterize the evaluator test suite over both dialects; add
   dialect-specific cases: the coexistence probes must pass under
   `openscad` and raise spanned `name-kind-conflict` under `single`.

## Future: first-class geometry and modules

The kind-slot model is the substrate for eventually storing geometry (lazy
CSG node references — the same seam that enables caching) and module
references in variables: new `BindingKind`s with position-based priority
fallbacks. For programs written against today's OpenSCAD those fallbacks
are unreachable — no legacy variable can hold a module or geometry — so
they extend the language without changing it.
