# StructGen Project Page Content and Layout Refresh

## Approved design

The hero keeps the existing ProbeX-inspired structure but moves `ACM MM 2026` directly below the paper title. Author affiliations are shortened by removing cities and countries, then grouped into three compact visual lines without changing author–affiliation numbering. The four resource controls retain their existing active/disabled behavior while adopting the reference page's large dark pill geometry and white icon treatment.

The post-abstract content is reorganized without swapping the explanatory paragraphs. The first section is titled `StructGen: a multi-reference image generation framework with structured context modeling mechanism.` and displays `method.pdf`. The second is titled `Structured Data Curation Pipeline` and presents `intro_v2.pdf` beside `dataset_compare.pdf`; Figure 4 is used instead of repeating `method.pdf`, which is Figure 3 in the paper. The Results section keeps the current qualitative comparison and adds Figure 7 (`text_generation.pdf`) below it with an accompanying explanation of text-only references.

The abstract removes only its final code-availability sentence. Benchmark emphasis for `400 cases` and `8 subsets` uses the primary dark text color. Desktop, tablet, and mobile layouts must remain free of horizontal overflow, with the two-image data row stacking on narrow screens.

## Validation

Automated tests cover content removal, section titles/order, new image assets, hero order, compact affiliations, button geometry, and benchmark emphasis. Browser verification covers desktop and mobile layout, the side-by-side image row, results additions, console errors, and horizontal overflow.
