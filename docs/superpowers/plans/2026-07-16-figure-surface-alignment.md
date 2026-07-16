# Figure Surface Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the Pipeline figures and remove the patch-like contrast around white-backed paper figures.

**Architecture:** Add an explicit white-section class to the two image-heavy sections. Normalize the paired Pipeline images through columns derived from their source aspect ratios and preserve natural image sizing.

**Tech Stack:** Static HTML, CSS, Python `unittest`.

## Global Constraints

- Do not crop or modify source images.
- Preserve the current mobile one-column layout.
- Keep neighboring section backgrounds unchanged.

---

### Task 1: Figure surface and alignment

**Files:**
- Modify: `index.html`
- Modify: `static/css/site.css`
- Test: `tests/test_page.py`

**Interfaces:**
- Consumes: existing `.paired-figures`, `.paired-figure-item`, and `.section-muted` layout rules.
- Produces: `.section-figure-white` section surface and aspect-ratio-aligned paired image dimensions.

- [ ] **Step 1: Write failing tests**

Assert that both target sections use `section-figure-white`, paired columns use the source aspect-ratio relationship, and images retain automatic height.

- [ ] **Step 2: Run tests to verify failure**

Run: `python3 -m unittest discover -s tests -v`

Expected: the new figure-surface test fails.

- [ ] **Step 3: Implement minimal HTML and CSS changes**

Add `section-figure-white` to `#structgen` and `#results`, define the white surface, and size the paired columns at `1fr 2.37fr` with natural image height.

- [ ] **Step 4: Verify tests and browser layout**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass. In the browser, Pipeline image top and bottom coordinates match and both target section backgrounds compute to white.

- [ ] **Step 5: Commit**

Commit the implementation and test changes together.
