const header = document.getElementById("site-header");
const mobileToggle = document.querySelector(".mobile-toggle");
const siteNavigation = document.getElementById("site-navigation");
const siteLoader = document.getElementById("site-loader");
const filterButtons = document.querySelectorAll(".filter-button");
const filterTargets = document.querySelectorAll(".filter-targets [data-category]");
const revealItems = document.querySelectorAll(".reveal");
const counters = document.querySelectorAll(".counter[data-target]");

if (siteLoader) {
  window.addEventListener("load", () => {
    siteLoader.classList.add("is-hidden");
    window.setTimeout(() => {
      siteLoader.remove();
    }, 360);
  });
}

if (header) {
  const setHeaderState = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };

  setHeaderState();
  window.addEventListener("scroll", setHeaderState, { passive: true });
}

if (mobileToggle && siteNavigation) {
  mobileToggle.addEventListener("click", () => {
    const isExpanded = mobileToggle.getAttribute("aria-expanded") === "true";
    mobileToggle.setAttribute("aria-expanded", String(!isExpanded));
    siteNavigation.classList.toggle("is-open", !isExpanded);
  });
}

if (filterButtons.length && filterTargets.length) {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const { filter } = button.dataset;

      filterButtons.forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");

      filterTargets.forEach((target) => {
        const matches = filter === "all" || target.dataset.category === filter;
        target.classList.toggle("is-hidden", !matches);
      });
    });
  });
}

if (revealItems.length) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.18 }
  );

  revealItems.forEach((item) => revealObserver.observe(item));
}

if (counters.length) {
  const countObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const counter = entry.target;
        const targetValue = Number(counter.dataset.target);
        const originalText = counter.textContent.trim();

        if (Number.isNaN(targetValue) || targetValue <= 0) {
          countObserver.unobserve(counter);
          return;
        }

        let current = 0;
        const step = Math.max(1, Math.ceil(targetValue / 36));
        const suffix = originalText.replace(/[0-9.,]/g, "");

        const interval = window.setInterval(() => {
          current += step;
          if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
          }
          counter.textContent = `${current.toLocaleString()}${suffix}`;
        }, 30);

        countObserver.unobserve(counter);
      });
    },
    { threshold: 0.45 }
  );

  counters.forEach((counter) => countObserver.observe(counter));
}
