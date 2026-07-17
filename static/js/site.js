(() => {
  "use strict";

  document.documentElement.classList.add("is-loading");

  const loader = document.querySelector(".page-loader");
  const backToTop = document.querySelector("#back-to-top");

  const hideLoader = () => {
    loader?.classList.add("is-hidden");
    document.documentElement.classList.remove("is-loading");
  };

  window.addEventListener("load", () => window.setTimeout(hideLoader, 120));
  window.setTimeout(hideLoader, 3000);

  const updateBackToTop = () => {
    backToTop?.classList.toggle("is-visible", window.scrollY > 300);
  };

  window.addEventListener("scroll", updateBackToTop, { passive: true });
  updateBackToTop();

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();
