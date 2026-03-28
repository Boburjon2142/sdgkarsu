const header = document.getElementById("site-header");
const mobileToggle = document.querySelector(".mobile-toggle");
const siteNavigation = document.getElementById("site-navigation");
const languageDropdown = document.querySelector(".language-dropdown");
const languageDropdownToggle = document.querySelector(".language-dropdown__toggle");
const siteLoader = document.getElementById("site-loader");
const filterButtons = document.querySelectorAll(".filter-button");
const filterTargets = document.querySelectorAll(".filter-targets [data-category]");
const revealItems = document.querySelectorAll(".reveal");
const counters = document.querySelectorAll(".counter[data-target]");
const tiltTargets = document.querySelectorAll(
  ".stat-card, .content-card:not(.governance-detail-card), .priority-card, .metric-card, .report-card, .news-card, .partner-card, .list-card, .sdg-news-card, .sdg-goal-card, .sdg-work-card"
);
const heroParallax = document.querySelectorAll(".hero-portrait-card, .hero-rankings-strip, .hero-author");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const typewriterTargets = document.querySelectorAll(
  ".hero-copy h1, .page-intro h1, .section-heading h2, .lined-title span"
);

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
  const closeNavigation = () => {
    mobileToggle.setAttribute("aria-expanded", "false");
    siteNavigation.classList.remove("is-open");
  };

  mobileToggle.addEventListener("click", () => {
    const isExpanded = mobileToggle.getAttribute("aria-expanded") === "true";
    mobileToggle.setAttribute("aria-expanded", String(!isExpanded));
    siteNavigation.classList.toggle("is-open", !isExpanded);
  });

  siteNavigation.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      closeNavigation();
    });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 860) {
      closeNavigation();
    }
  });
}

if (languageDropdown && languageDropdownToggle) {
  const closeLanguageDropdown = () => {
    languageDropdown.classList.remove("is-open");
    languageDropdownToggle.setAttribute("aria-expanded", "false");
  };

  languageDropdownToggle.addEventListener("click", () => {
    const isExpanded = languageDropdownToggle.getAttribute("aria-expanded") === "true";
    languageDropdown.classList.toggle("is-open", !isExpanded);
    languageDropdownToggle.setAttribute("aria-expanded", String(!isExpanded));
  });

  document.addEventListener("click", (event) => {
    if (!languageDropdown.contains(event.target)) {
      closeLanguageDropdown();
    }
  });

  languageDropdown.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      closeLanguageDropdown();
    });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 580) {
      closeLanguageDropdown();
    }
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
  revealItems.forEach((item, index) => {
    item.style.setProperty("--reveal-delay", `${Math.min(index * 55, 420)}ms`);
  });

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

if (tiltTargets.length && !prefersReducedMotion.matches) {
  tiltTargets.forEach((card) => {
    card.classList.add("tilt-card");

    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const rotateX = ((y / rect.height) - 0.5) * -8;
      const rotateY = ((x / rect.width) - 0.5) * 8;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-6px)`;
    });

    card.addEventListener("pointerleave", () => {
      card.style.transform = "";
    });

    card.addEventListener("pointerup", () => {
      card.style.transform = "";
    });
  });
}

if (heroParallax.length && !prefersReducedMotion.matches) {
  const handleHeroParallax = () => {
    const offset = Math.min(window.scrollY * 0.08, 24);

    heroParallax.forEach((item, index) => {
      const multipliers = [1, 0.65, 0.45];
      const multiplier = multipliers[index] || 0.4;
      item.style.transform = `translateY(${offset * multiplier}px)`;
    });
  };

  handleHeroParallax();
  window.addEventListener("scroll", handleHeroParallax, { passive: true });
}

if (typewriterTargets.length) {
  const runTypewriter = (element) => {
    if (element.dataset.typewriterReady === "true") {
      return;
    }

    const originalText = element.textContent.trim();
    if (!originalText) {
      element.dataset.typewriterReady = "true";
      return;
    }

    element.dataset.typewriterReady = "true";
    element.classList.add("typewriter-target");

    if (prefersReducedMotion.matches) {
      element.textContent = originalText;
      element.classList.add("is-complete");
      return;
    }

    element.textContent = "";
    element.classList.add("is-typing");

    let index = 0;
    const step = () => {
      index += 1;
      element.textContent = originalText.slice(0, index);

      if (index < originalText.length) {
        window.setTimeout(step, originalText.length > 42 ? 20 : 34);
      } else {
        element.classList.remove("is-typing");
        element.classList.add("is-complete");
      }
    };

    window.setTimeout(step, 120);
  };

  const typeObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          runTypewriter(entry.target);
          typeObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.45 }
  );

  typewriterTargets.forEach((target) => typeObserver.observe(target));
}
