# Project Philosophy (Python / Solo / Cursor)

## 0) Priorities (in order)
1. Correctness
2. **Clear modular design**
3. Simplicity and readability
4. Fast iteration (easy to build, change, and delete)
5. Performance (only when measured or clearly necessary)

Default choice: the simplest modular solution that is easy to extend or remove.

---

## 1) Design & Modularity Principles (Core)
- Prefer **composition over inheritance**
- Modules should do **one thing** and expose a **small, explicit interface**
- Dependencies flow **in one direction** (no circular knowledge)
- Build systems from **replaceable parts**
- Avoid deep hierarchies; keep the structure flat where possible

A good module:
- Can be explained in one sentence
- Has few reasons to change
- Can be tested in isolation

---

## 2) Efficient Building & Iteration
- Optimize for **fast construction and feedback**
- Start concrete, abstract only when repetition appears
- Prefer small, working increments over large designs
- Write code that is easy to throw away

Rule of thumb:
> If a change touches many files, the design is probably wrong.

---

## 3) Documentation Policy (No Doc Bloat)
### Allowed docs (keep these, keep them short)
- **README.md**: what the project does + how to run it
- **ARCHITECTURE.md**: the one true high-level view (required, always current)
- **CHANGELOG.md** (optional): only if releases matter

### Not allowed
- Summary, notes, or history markdown files that grow over time
- Duplicated explanations across multiple docs

### Rule
Explain things in this order:
1) Code (clear structure and naming)
2) Local comments (why, not what)
3) **ARCHITECTURE.md** (system view)

---

## 4) Architecture Must Be Stable and Visible
### The contract
- **ARCHITECTURE.md is mandatory and authoritative**
- If architecture changes, update it in the same change
- Remove abandoned approaches immediately

### ARCHITECTURE.md must fit on one screen and include:
- One-paragraph system overview
- Simple dataflow diagram (ASCII)
- Module map with responsibilities
- Key invariants (3–7 bullets)
- Main entrypoints and how they connect

No deep dives, no historical context.

---

## 5) Code Organization
- Prefer **explicit boundaries** between modules
- Pass dependencies explicitly (no hidden globals)
- Centralize orchestration; keep logic at the edges
- Keep I/O, business logic, and coordination separate

Suggested default layout:
- `src/` or top-level package: core logic
- `tests/`: tests
- `scripts/`: thin wrappers / entrypoints (optional)

---

## 6) Change Policy (Prevent Fleeting Architecture)
- Improve designs incrementally, not via rewrites
- Large refactors require:
  - a clear simplification
  - fewer or cleaner dependencies
  - ARCHITECTURE.md updated in the same change
- Old paths are removed quickly; no long-lived dead code

---

## 7) Dependency Policy
- Default: no new dependencies
- Add dependencies only if they **reduce overall complexity**
- Prefer standard library
- Each dependency must earn its place

---

## 8) Secrets & Configuration (Stable and Explicit)
- Never commit secrets
- Never replace real config with “INSERT KEY HERE”
- Config keys are stable and validated at startup

Standard pattern:
- `.env` (local, ignored)
- `.env.example` (committed, real variable names)
- `config.py` that loads and validates config

Missing config should fail fast with clear errors.

---

## 9) Testing & Validation
- Test modules in isolation
- Focus tests on logic, not wiring
- Regression tests for fixed bugs when reasonable
- Small scripts must have at least a documented smoke run

---

## 10) Error Handling & Observability
- Fail fast on invalid state
- Errors must include context
- Logging should reflect system structure (module-level, not noisy)

---

## 11) Cursor / AI Rules
- Follow existing structure and naming
- Prefer minimal diffs
- Do not introduce new abstractions without need
- Ask before:
  - adding dependencies
  - changing module boundaries
  - restructuring folders
- Architecture changes require ARCHITECTURE.md updates

Output preference:
- Propose a plan first when scope is unclear
- Keep explanations short and actionable

---

## 12) Quality Bar
- Modules over functions, functions over cleverness
- Readability beats elegance
- If it’s hard to change, it’s not modular enough

## Execution Constraints (Strict)

This document defines intent, not documentation requirements.

When implementing changes, agents must follow these rules:

### 1. Scope Discipline
- Implement **only what is explicitly requested**
- Do NOT update unrelated files
- Do NOT create new markdown, documentation, or explanation files unless explicitly asked

If the request is a visual change:
→ Only CSS / HTML / templates may be touched.

---

### 2. No Meta-Documentation by Default
- Do NOT create system explanation files (e.g. UI_SYSTEM.md, CHANGES.md)
- Do NOT narrate or justify changes in long-form text
- Do NOT restate philosophy in new documents

Silence is preferred over explanation.

---

### 3. Minimal Response Contract
Default response format:
- Short confirmation
- List of files changed
- One-line summary per file (optional)

No essays. No summaries. No retrospectives.

---

### 4. Design ≠ Documentation
A design rule only exists if it is **encoded in the system itself**
(CSS variables, layout structure, templates).

If a rule cannot be enforced structurally, it should not be documented.

---

### 5. Prefer Deletion Over Addition
- Fewer files > more files
- Fewer concepts > more concepts
- Fewer words > more words

Adding a new file requires explicit approval.

---

### 6. Stop Condition
Once the requested change is implemented:
- STOP
- Do NOT look for adjacent improvements
- Do NOT “complete the system”