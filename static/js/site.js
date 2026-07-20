(() => {
  "use strict";

  document.documentElement.classList.add("is-loading");

  const loader = document.querySelector(".page-loader");
  const copyButton = document.querySelector("#copy-citation");
  const citationCode = document.querySelector("#citation-code code");
  const backToTop = document.querySelector("#back-to-top");

  const hideLoader = () => {
    loader?.classList.add("is-hidden");
    document.documentElement.classList.remove("is-loading");
  };

  window.addEventListener("load", () => window.setTimeout(hideLoader, 120));
  window.setTimeout(hideLoader, 3000);

  copyButton?.addEventListener("click", async () => {
    const citation = citationCode?.textContent?.trim() ?? "";
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
      console.error("Unable to copy the citation.", error);
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
