# StructGen Project Page

Static project page for **StructGen: Disambiguating Multi-Reference Image Generation via Structured Context Modeling**.

## Local preview

```bash
python3 -m http.server 18766
```

Then open <http://127.0.0.1:18766/>.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Image assets

The web images are generated from the selected paper figures:

```bash
python3 scripts/build_images.py
```

This repository contains only the project-page implementation. The page license does not alter the licenses of the associated paper, code, or dataset.
