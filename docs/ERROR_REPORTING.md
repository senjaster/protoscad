# Error reporting

How ProtoSCAD reports failures: one structured `Diagnostic` built at the raise
site, rendered on demand as human-readable text or tooling-friendly JSON.

## Architecture

```
raise sites                          renderers
-----------                          ---------
ProtoSCADError ── .diagnostic ──► Diagnostic ──► render_text()  rustc-style, stderr
(ParseError = syntax)                        └─► render_json()  LSP-shaped, stdout
```

Everything lives in `protoscad.diagnostics`:

- `SourceSpan` (`spans.py`) — a half-open source region, 1-based lines,
  0-based columns. The AST visitor fills it on statements **and on every
  expression node** (constant folding preserves it); the root re-exports it
  as `protoscad.tree.statement.SourceSpan`. On `Expression` the field is
  `compare=False`, so node equality compares shape only.
- `Diagnostic` (`diagnostic.py`) — `code`, `message`, optional `span`,
  `severity`, `notes`. Format-neutral: no filename (errors are raised deep in
  evaluation where no filename is known — the reporting boundary attaches it).
- `ProtoSCADError` (`errors.py`) — the single exception class for every
  user-facing failure (syntax, name resolution, evaluation). Carries its
  `Diagnostic`; `str(error)` is the bare message so tracebacks stay readable.
- `render_text` / `render_json` (`render.py`) — pure functions
  `(diagnostics, source, file) -> str`. Neither is involved when the error is
  created.

Internal invariants that cannot come from user source (unknown binary
operator, the `Undefined` sentinel backstop) are also `ProtoSCADError`, just
without a span.

## Error codes

Codes are stable kebab-case strings (`ErrorCode`); messages are free to
change, codes are not. They key IDE-side filtering and documentation.

| Code | Raised by |
|---|---|
| `syntax` | the parser's fail-fast listener (lexical and syntax errors) |
| `unknown-module` | `Invocation` |
| `unknown-parameter` | `ModuleDefinition.bind_args` — points at the offending argument expression |
| `too-many-positional-args` | `ModuleDefinition.bind_args` — points at the first excess argument |
| `missing-required-parameter` | `Invocation` (at bind time, pointing at the call — not when the value is read) |
| `unknown-variable` | `DeclarativeResolver` / `OpenScadResolver` |
| `use-before-assignment` | `OpenScadResolver` |
| `circular-dependency` | `OpenScadResolver._topological` / `Environment._force` |
| `unknown-operator` | internal invariant (`BinaryOp`) |

## Parse behavior

Parsing stops on the **first** syntax error: a custom ANTLR error listener
raises `ProtoSCADError(code=syntax)` with the offending token's span (a
zero-width point for lexer errors, which carry no token). ANTLR's default
stderr reporting is disabled — a broken tree is never evaluated. Parsing
lives in `protoscad/parser.py`; `protoscad.render` only renders meshes.

## Output formats

Plaintext (default; stderr), columns displayed 1-based:

```
error[unknown-module]: Unknown module: 'cbe'
  --> model.scad:3:1
  |
3 | cbe(10);
  | ^^^^^^^
```

JSON (`--err-format json`; stdout), LSP-shaped so a language server can map it
directly: `range` is 0-based line/character, `end` exclusive.

```json
{
  "diagnostics": [
    {
      "severity": "error",
      "code": "unknown-module",
      "message": "Unknown module: 'cbe'",
      "file": "model.scad",
      "range": {"start": {"line": 2, "character": 0}, "end": {"line": 2, "character": 7}},
      "notes": []
    }
  ]
}
```

Any error exits with status 1.

## Adding a new error

1. Add a code to `ErrorCode` (a stable string).
2. Raise `ProtoSCADError(message, code=..., span=...)` — pass the span of the
   node the user wrote wrong. Statements and expressions all carry spans
   (named-argument spans cover the whole `name = value`); `None` is the last
   resort.
3. Assert the span in a test (`tests/test_error_spans.py` has the pattern:
   one statement per line, so spans read as `(line, 0, line, len)`).

Multi-error collection (several syntax or resolution errors in one pass) is a
deliberate non-goal for now: parsing is fail-fast and evaluation is
fail-fast. The renderers already accept sequences, so collecting later is a
raise-site change only, not a reporting change.
