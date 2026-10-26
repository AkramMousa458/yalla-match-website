(function () {
  var config = window.YALLA_MATCH_SUPPORT || {};
  var langKey = "yalla-match-lang";

  document.querySelectorAll("[data-lang-link]").forEach(function (link) {
    link.addEventListener("click", function () {
      try {
        localStorage.setItem(langKey, link.getAttribute("data-lang-link"));
      } catch (error) {
        return;
      }
    });
  });

  var yearNode = document.getElementById("copyright-year");
  if (yearNode) {
    yearNode.textContent = String(new Date().getFullYear());
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      if (isOpen) {
        var firstLink = nav.querySelector("a");
        if (firstLink) firstLink.focus();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  document.querySelectorAll(".faq-item button").forEach(function (button) {
    button.addEventListener("click", function () {
      var item = button.closest(".faq-item");
      var isOpen = item.classList.contains("is-open");
      item.classList.toggle("is-open", !isOpen);
      button.setAttribute("aria-expanded", isOpen ? "false" : "true");
    });
  });

  var filterButtons = document.querySelectorAll(".filter-chip");
  filterButtons.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var category = chip.getAttribute("data-filter");
      filterButtons.forEach(function (other) {
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });
      document.querySelectorAll(".faq-item").forEach(function (item) {
        var matches = category === "all" || item.getAttribute("data-category") === category;
        item.hidden = !matches;
      });
    });
  });

  var form = document.getElementById("support-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var errorBox = document.getElementById("form-error");
      var statusBox = document.getElementById("form-status");
      if (errorBox) {
        errorBox.hidden = true;
        errorBox.textContent = "";
      }
      if (statusBox) {
        statusBox.hidden = true;
        statusBox.textContent = "";
      }

      var email = form.email.value.trim();
      var category = form.category.value;
      var subject = form.subject.value.trim();
      var message = form.message.value.trim();
      var name = form.name.value.trim();
      var invalidMessage = "";
      var invalidField = null;

      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        invalidMessage = form.getAttribute("data-error-email");
        invalidField = form.email;
      } else if (!category) {
        invalidMessage = form.getAttribute("data-error-category");
        invalidField = form.category;
      } else if (!subject) {
        invalidMessage = form.getAttribute("data-error-subject");
        invalidField = form.subject;
      } else if (message.length < 10) {
        invalidMessage = form.getAttribute("data-error-message");
        invalidField = form.message;
      }

      if (invalidMessage) {
        if (errorBox) {
          errorBox.hidden = false;
          errorBox.textContent = invalidMessage;
        }
        if (invalidField) invalidField.focus();
        return;
      }

      var categoryLabel = form.category.options[form.category.selectedIndex].text;
      var lines = [
        form.getAttribute("data-intro"),
        "",
        form.getAttribute("data-label-name") + ": " + (name || "-"),
        form.getAttribute("data-label-email") + ": " + email,
        form.getAttribute("data-label-category") + ": " + categoryLabel,
        form.getAttribute("data-label-subject") + ": " + subject,
        "",
        message,
        "",
        form.getAttribute("data-footer")
      ];
      var mailSubject = form.getAttribute("data-subject-prefix") + " - " + subject;
      var href = "mailto:" + form.getAttribute("data-support-email") +
        "?subject=" + encodeURIComponent(mailSubject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      if (statusBox) {
        statusBox.hidden = false;
        statusBox.textContent = form.getAttribute("data-status-ready");
      }
    });
  }

  var appStoreSlot = document.getElementById("app-store-slot");
  var appStoreUrl = typeof config.appStoreUrl === "string" ? config.appStoreUrl.trim() : "";
  if (appStoreSlot && /^https:\/\/apps\.apple\.com\//.test(appStoreUrl)) {
    var badge = appStoreSlot.querySelector(".store-badge");
    if (badge) {
      var link = document.createElement("a");
      link.className = "store-badge";
      link.href = appStoreUrl;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.innerHTML = badge.innerHTML;
      var hint = link.querySelector("small");
      if (hint) hint.textContent = appStoreSlot.getAttribute("data-hint") || hint.textContent;
      badge.replaceWith(link);
    }
  }

  var origin = typeof config.siteOrigin === "string" ? config.siteOrigin.replace(/\/$/, "") : "";
  if (origin && /^https:\/\//.test(origin)) {
    ["canonical", "alternate"].forEach(function (rel) {
      document.querySelectorAll('link[rel="' + rel + '"]').forEach(function (node) {
        var href = node.getAttribute("href");
        if (!href || href.indexOf("http") === 0) return;
        var resolved = new URL(href, window.location.href);
        node.setAttribute("href", origin + resolved.pathname + resolved.search);
      });
    });
    var ogUrl = document.querySelector('meta[property="og:url"]');
    if (ogUrl) ogUrl.setAttribute("content", origin + window.location.pathname);
    var ogImage = document.querySelector('meta[property="og:image"]');
    if (ogImage) {
      var imageHref = ogImage.getAttribute("content");
      if (imageHref && imageHref.indexOf("http") !== 0) {
        ogImage.setAttribute("content", new URL(imageHref, window.location.href).href.replace(window.location.origin, origin));
      }
    }
  }
})();
