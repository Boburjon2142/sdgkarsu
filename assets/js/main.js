const header = document.getElementById("site-header");
const mobileToggle = document.querySelector(".mobile-toggle");
const siteNavigation = document.getElementById("site-navigation");
const languageDropdown = document.querySelector(".language-dropdown");
const languageDropdownToggle = document.querySelector(".language-dropdown__toggle");
const siteLoader = document.getElementById("site-loader");
const filterButtons = document.querySelectorAll(".filter-button");
const filterTargets = document.querySelectorAll(".filter-targets [data-category]");
const revealItems = document.querySelectorAll(".reveal");
const countupItems = document.querySelectorAll("[data-countup]");
const tiltTargets = document.querySelectorAll(
  ".stat-card, .content-card:not(.governance-detail-card), .priority-card, .metric-card, .report-card, .news-card, .partner-card, .list-card, .sdg-news-card, .sdg-goal-card, .sdg-work-card"
);
const heroParallax = document.querySelectorAll(".hero-portrait-card, .hero-rankings-strip, .hero-author");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const typewriterTargets = document.querySelectorAll("[data-typewriter]");

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

  const revealItem = (item) => {
    if (item.classList.contains("is-visible")) {
      return;
    }

    item.classList.add("is-visible");
  };

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          revealItem(entry.target);
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.18 }
  );

  revealItems.forEach((item) => {
    const rect = item.getBoundingClientRect();
    const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

    if (isVisible) {
      revealItem(item);
      return;
    }

    revealObserver.observe(item);
  });
}

if (countupItems.length) {
  const formatCountupValue = (value, prefix = "", suffix = "") => {
    return `${prefix}${Math.round(value).toLocaleString("en-US")}${suffix}`;
  };

  const runCountup = (element) => {
    if (element.dataset.countupReady === "true") {
      return;
    }

    const targetValue = Number(element.dataset.target);
    const duration = Number(element.dataset.duration || 1800);
    const prefix = element.dataset.prefix || "";
    const suffix = element.dataset.suffix || "";

    if (Number.isNaN(targetValue) || targetValue <= 0) {
      element.textContent = formatCountupValue(0, prefix, suffix);
      element.dataset.countupReady = "true";
      return;
    }

    element.dataset.countupReady = "true";

    if (prefersReducedMotion.matches) {
      element.textContent = formatCountupValue(targetValue, prefix, suffix);
      return;
    }

    const startedAt = performance.now();
    const easeOutCubic = (progress) => 1 - ((1 - progress) ** 3);

    element.textContent = formatCountupValue(0, prefix, suffix);

    const tick = (now) => {
      const elapsed = now - startedAt;
      const progress = Math.min(elapsed / duration, 1);
      const currentValue = targetValue * easeOutCubic(progress);

      element.textContent = formatCountupValue(currentValue, prefix, suffix);

      if (progress < 1) {
        window.requestAnimationFrame(tick);
      } else {
        element.textContent = formatCountupValue(targetValue, prefix, suffix);
      }
    };

    window.requestAnimationFrame(tick);
  };

  const countupObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        runCountup(entry.target);
        countupObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.35,
      rootMargin: "0px 0px -5% 0px",
    }
  );

  countupItems.forEach((item) => {
    const rect = item.getBoundingClientRect();
    const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

    if (isVisible) {
      runCountup(item);
      return;
    }

    countupObserver.observe(item);
  });
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
    element.classList.remove("typewriter-pending");
    element.style.minHeight = `${element.getBoundingClientRect().height || element.offsetHeight}px`;

    if (prefersReducedMotion.matches) {
      element.textContent = originalText;
      element.classList.add("is-complete");
      element.classList.remove("typewriter-pending");
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
        element.style.minHeight = "";
      }
    };

    window.setTimeout(step, 120);
  };

  const startTypewriters = () => {
    typewriterTargets.forEach((target) => {
      runTypewriter(target);
    });
  };

  if (document.readyState === "complete") {
    window.setTimeout(startTypewriters, 180);
  } else {
    window.addEventListener("load", () => {
      window.setTimeout(startTypewriters, 180);
    });
  }

  if (prefersReducedMotion.matches) {
    typewriterTargets.forEach((target) => {
      target.classList.remove("typewriter-pending");
    });
  } else {
    window.setTimeout(() => {
      typewriterTargets.forEach((target) => {
        if (target.dataset.typewriterReady !== "true") {
          target.classList.remove("typewriter-pending");
        }
      });
    }, 2000);
  }
}
