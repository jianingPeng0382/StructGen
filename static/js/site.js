(() => {
  "use strict";

  const loader = document.querySelector(".page-loader");
  const copyButton = document.querySelector("#copy-bibtex");
  const bibtexCode = document.querySelector("#bibtex-code code");
  const backToTop = document.querySelector("#back-to-top");

  window.addEventListener("load", () => {
    window.setTimeout(() => loader?.classList.add("is-hidden"), 120);
  });

  copyButton?.addEventListener("click", async () => {
    const citation = bibtexCode?.textContent?.trim() ?? "";
    if (!citation) return;

    try {
      await navigator.clipboard.writeText(citation);
      const label = copyButton.querySelector("span");
      const original = label?.textContent ?? "Copy";
      if (label) label.textContent = "Copied!";
      copyButton.classList.add("is-copied");
      window.setTimeout(() => {
        if (label) label.textContent = original;
        copyButton.classList.remove("is-copied");
      }, 2000);
    } catch (error) {
      console.error("Unable to copy the BibTeX entry.", error);
    }
  });

  const updateBackToTop = () => {
    backToTop?.classList.toggle("is-visible", window.scrollY > 300);
  };

  window.addEventListener("scroll", updateBackToTop, { passive: true });
  updateBackToTop();

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();
