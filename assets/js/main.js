document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".mobile-toggle");
  var dropdownItems = document.querySelectorAll(".nav-item--dropdown");
  var currentPage = document.body.getAttribute("data-page");
  var navLinks = document.querySelectorAll("[data-nav]");
  var filterButtons = document.querySelectorAll("[data-filter]");
  var filterItems = document.querySelectorAll("[data-category]");

  function setScrolledState() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }

  function closeMobileNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    dropdownItems.forEach(function (item) {
      item.classList.remove("is-open");
      var trigger = item.querySelector(".nav-link--dropdown");
      if (trigger) {
        trigger.setAttribute("aria-expanded", "false");
      }
    });
  }

  setScrolledState();
  window.addEventListener("scroll", setScrolledState);

  navLinks.forEach(function (link) {
    if (link.getAttribute("data-nav") === currentPage) {
      link.classList.add("is-active");
      link.setAttribute("aria-current", "page");
    }
  });

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("is-open");
    });
  }

  dropdownItems.forEach(function (item) {
    var trigger = item.querySelector(".nav-link--dropdown");
    if (!trigger) return;

    trigger.addEventListener("click", function (event) {
      if (window.innerWidth > 960) return;
      event.preventDefault();

      var isOpen = item.classList.contains("is-open");
      dropdownItems.forEach(function (dropdownItem) {
        dropdownItem.classList.remove("is-open");
        var dropdownTrigger = dropdownItem.querySelector(".nav-link--dropdown");
        if (dropdownTrigger) {
          dropdownTrigger.setAttribute("aria-expanded", "false");
        }
      });

      if (!isOpen) {
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (event) {
      var targetId = anchor.getAttribute("href");
      if (!targetId || targetId === "#") return;
      var target = document.querySelector(targetId);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      closeMobileNav();
    });
  });

  if (filterButtons.length && filterItems.length) {
    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var category = button.getAttribute("data-filter");
        filterButtons.forEach(function (item) {
          item.classList.remove("is-active");
        });
        button.classList.add("is-active");

        filterItems.forEach(function (card) {
          var matches = category === "all" || card.getAttribute("data-category") === category;
          card.classList.toggle("is-hidden", !matches);
        });
      });
    });
  }

  window.addEventListener("resize", function () {
    if (window.innerWidth > 960) {
      closeMobileNav();
    }
  });
});
