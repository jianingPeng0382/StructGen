# StructGen Project Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and locally verify a faithful ProbeX-style static project page for StructGen.

**Architecture:** A dependency-light static site uses one HTML document, one CSS file, one JavaScript file, and relative image assets. It is designed for GitHub Pages subdirectory hosting without a build step.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Python standard-library tests, Poppler image conversion.

## Global Constraints

- Use the latest `Jianing_ACMMM26_arxiv_cvpr` Overleaf project as the source of truth for title, authors, affiliations, abstract, and citation metadata.
- Match ProbeX typography, palette, button treatment, section rhythm, responsive behavior, loading animation, scroll-to-top behavior, and BibTeX copy feedback.
- Keep all assets on relative paths and do not add React, a backend, a build tool, analytics, carousel, video, or MathJax.
- Code and Dataset are active links; Paper and arXiv are non-interactive `Coming Soon` controls.
- Do not publish or create a remote repository before user approval of the local preview.

---

### Task 1: Static page contract and source synchronization

- [x] Write failing structure, content, asset, accessibility, and attribution tests.
- [ ] Run tests and record the expected missing-page failure.
- [ ] Synchronize exact paper metadata from Overleaf.

### Task 2: Page implementation and image pipeline

- [ ] Implement the hero, navigation buttons, content sections, results, BibTeX, and footer.
- [ ] Convert the five paper figures into web-optimized high-resolution images.
- [ ] Add OG art, favicon, responsive styles, load animation, copy feedback, and scroll-to-top behavior.
- [ ] Run the tests until all pass.

### Task 3: Local browser verification

- [ ] Serve the page over local HTTP and verify resources and public links.
- [ ] Inspect desktop, tablet, and mobile layouts for overflow, readability, and section fidelity.
- [ ] Verify keyboard semantics, copy behavior, console cleanliness, and back-to-top behavior.
- [ ] Deliver the local preview without publishing it.
