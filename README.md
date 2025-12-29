Below is a **clean, recruiter-grade README** you can paste directly.
No hype. No fluff. Scope is frozen. Ownership is clear.

---

# Protocol Compiler

**Protocol Compiler** is a system that converts vague human intent into **structured, executable action protocols**.

It does not generate motivational advice or life roadmaps.
It enforces structure, validates intent, and outputs machine-readable execution plans.

---

## Philosophy

> **Vague intent is not executable. Structure is.**

Most “planning” tools fail because they accept under-specified goals and respond with generic roadmaps.
Protocol Compiler takes the opposite approach:

* It **refuses vague inputs**
* It **forces clarification**
* It outputs **inspectable structure**, not prose

The goal is not usefulness at scale — the goal is **correct transformation**.

---

## What This Project Is (and Is Not)

### ✅ This project **does**

* Transform raw intent into a **canonical intent frame**
* Validate whether an intent is **actionable**
* Convert valid intent into a **structured execution protocol**
* Output results as **strict JSON schemas**

### ❌ This project does **not**

* Track execution or progress
* Provide dashboards or UI
* Generate content-heavy roadmaps
* Solve open-ended life goals

If an intent cannot be bounded, decomposed, and executed, the system rejects it.

---

## Core Idea

The system performs the following transformation:

```
Unstructured Intent (text)
        ↓
Intent Validation & Normalization
        ↓
Intent Frame (structured)
        ↓
Protocol Plan (executable steps)
```

The key contribution is **not** the steps themselves, but the **structural discipline** enforced before steps exist.

---

## Valid vs Invalid Intent

Protocol Compiler operates only on **task-shaped intent**.

### ❌ Invalid (rejected)

* “I want to become a millionaire”
* “I want to be healthy”
* “I want to improve my life”

These lack bounds, constraints, or executability.

### ✅ Valid

* “Prepare for a Codeforces contest in 14 days”
* “Understand eigenvalues well enough to solve tutorial problems this week”
* “Build running stamina to reach 10km in 4 weeks”

---

## Intent Frame (Internal Representation)

All valid intents are normalized into a canonical **Intent Frame**:

```json
{
  "objective": "string",
  "domain": "string",
  "time_horizon_days": number,
  "starting_state": "string",
  "constraints": ["string"],
  "success_definition": "string"
}
```

This abstraction allows the system to remain domain-agnostic while still enforcing rigor.

---

## Protocol Output Schema

The output is a **machine-readable execution protocol**, not free text.

Example (simplified):

```json
{
  "day": 3,
  "focus": "Two pointers",
  "tasks": [
    { "type": "conceptual_pass", "duration_min": 60 },
    { "type": "practice", "count": 8 },
    { "type": "review", "duration_min": 30 }
  ]
}
```

Tasks are intentionally abstract (learn / practice / review / execute).
The system provides **structure**, not content.

---

## Architecture Overview

* **Intent Parser**

  * Parses raw text
  * Extracts candidate objectives and constraints
* **Validator**

  * Rejects under-specified or non-executable intents
  * Requests clarification when needed
* **Protocol Planner**

  * Decomposes intent into ordered phases and task types
  * Enforces workload and sequencing constraints
* **Output Layer**

  * CLI output
  * JSON persistence

---

## Design Principles

* Determinism over creativity
* Structure over advice
* Validation before execution
* Schema before features

---

## Project Status

This repository intentionally implements **only the compiler core**.

All expansion ideas (execution tracking, personalization, UI, agents) are explicitly deferred and documented in `FUTURE.md`.

This is a finished, scoped artifact — not a growing product.

---

## Why This Exists

This project demonstrates:

* Ability to freeze scope
* System design thinking
* Schema-first engineering
* Constraint-driven planning logic

It is meant to be **understandable, explainable, and complete**.

---

## Example Usage (Planned)

```bash
protocol compile "Prepare for a Codeforces contest in 14 days"
```

Output:

* Validated intent frame
* Executable protocol (JSON)

---
