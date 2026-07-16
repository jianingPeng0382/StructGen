# StructGen Project Page Content and Layout Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the StructGen project page content hierarchy, figure composition, author metadata, resource controls, and emphasis styles.

**Architecture:** Keep the dependency-light static site and update its existing HTML/CSS/image pipeline. Extend the current standard-library tests to assert the requested content and layout contracts before making production changes.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Python standard-library tests, Poppler/Pillow image conversion.

## Global Constraints

- Keep Paper and arXiv non-interactive and marked `Coming Soon`; keep Code and Dataset active.
- Use Figure 4 beside Figure 2 in the data-curation section instead of duplicating Figure 3.
- Preserve existing section explanatory paragraphs while changing the first two headings and images.
- Keep all internal resources relative and retain ProbeX/template attribution and CC BY-SA 4.0.
- Do not publish or push before user approval of the refreshed local preview.

---

### Task 1: Add failing refresh contract tests

**Files:**
- Modify: `tests/test_page.py`

- [ ] Add tests for abstract trimming, hero ordering, compact affiliations, section headings and figures, Results Figure 7, button geometry, and benchmark contrast.
- [ ] Run `python3 -m unittest discover -s tests -v` and confirm the new assertions fail against the current page.

### Task 2: Implement content, figures, and styles

**Files:**
- Modify: `index.html`
- Modify: `static/css/site.css`
- Modify: `scripts/build_images.py`
- Create: `static/images/dataset-comparison.webp`
- Create: `static/images/text-generation.webp`

- [ ] Render Figure 4 and Figure 7 as web images through the existing image pipeline.
- [ ] Update hero order and affiliations, section headings and image composition, Results content, abstract, and benchmark emphasis.
- [ ] Match the large dark ProbeX-style resource controls while preserving disabled semantics.
- [ ] Run the complete test suite until all tests pass.

### Task 3: Browser verification

**Files:**
- Modify: `docs/superpowers/plans/2026-07-16-project-page-content-layout-refresh.md`

- [ ] Reload the local page and inspect desktop and 390px mobile layouts.
- [ ] Confirm the two-image row, stacked mobile fallback, no overflow, no console errors, and correct figure ordering.
- [ ] Commit the refreshed page while keeping the branch local.
