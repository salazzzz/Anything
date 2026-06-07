/* ---------- Before / After comparison slider ---------- */
const comparisonSlider = document.getElementById("comparisonSlider");
const comparisonWrapper = document.getElementById("comparisonWrapper");
const afterWrapper = document.getElementById("afterWrapper");
const comparisonLine = document.getElementById("comparisonLine");
const comparisonHandle = document.getElementById("comparisonHandle");

function updateComparison(pct) {
  pct = Math.max(0, Math.min(100, Number(pct)));
  if (afterWrapper) afterWrapper.style.width = pct + "%";
  if (comparisonLine) comparisonLine.style.left = pct + "%";
  if (comparisonHandle) comparisonHandle.style.left = pct + "%";
  if (comparisonSlider) comparisonSlider.value = pct;
}

if (comparisonWrapper) {
  updateComparison(50);

  let dragging = false;

  const pctFromEvent = (e) => {
    const rect = comparisonWrapper.getBoundingClientRect();
    const x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
    return (x / rect.width) * 100;
  };

  const startDrag = (e) => {
    dragging = true;
    comparisonWrapper.classList.add("is-dragging");
    updateComparison(pctFromEvent(e));
    e.preventDefault();
  };

  const onMove = (e) => {
    if (!dragging) return;
    updateComparison(pctFromEvent(e));
  };

  const endDrag = () => {
    dragging = false;
    comparisonWrapper.classList.remove("is-dragging");
  };

  comparisonWrapper.addEventListener("mousedown", startDrag);
  window.addEventListener("mousemove", onMove);
  window.addEventListener("mouseup", endDrag);

  comparisonWrapper.addEventListener("touchstart", startDrag, { passive: false });
  window.addEventListener("touchmove", onMove, { passive: false });
  window.addEventListener("touchend", endDrag);

  if (comparisonSlider) {
    comparisonSlider.addEventListener("input", (e) => updateComparison(e.target.value));
  }
}

/* ---------- Footer year ---------- */
const footerYear = document.getElementById("footer-year");
if (footerYear) footerYear.textContent = new Date().getFullYear();

/* ---------- Email protection ---------- */
document.querySelectorAll(".js-email").forEach(function (el) {
  var addr = el.dataset.e + "@" + el.dataset.d;
  el.href = "mailto:" + addr;
  if (el.textContent === "Email Us" || el.textContent === "Email Euro Detailing") {
    el.textContent = addr;
  }
});

/* ---------- Vehicle size selector (service detail pages) ---------- */
document.querySelectorAll(".tier-card").forEach((card) => {
  const buttons = card.querySelectorAll(".size-option");
  const priceEl = card.querySelector(".tier-price-value");
  const timeEl = card.querySelector(".tier-time-value");
  const bookBtn = card.querySelector(".tier-book-btn");
  const maintBtn = card.querySelector(".tier-maint-btn");

  let currentSize = "sedan";
  let maintenanceMode = false;

  let originalEl = null;
  let saveChipEl = null;
  if (maintBtn && priceEl) {
    originalEl = document.createElement("span");
    originalEl.className = "tier-price-original";
    priceEl.parentNode.insertBefore(originalEl, priceEl);

    saveChipEl = document.createElement("span");
    saveChipEl.className = "tier-save-chip";
    saveChipEl.textContent = "Save $25";
    priceEl.parentNode.appendChild(saveChipEl);
  }

  function getRegularPrice(size) {
    return priceEl?.dataset["price" + capitalize(size)] || "";
  }
  function getMaintPrice(size) {
    return priceEl?.dataset["maint" + capitalize(size)] || "";
  }
  function getRegularLink(size) {
    return bookBtn?.dataset["link" + capitalize(size)] || "#";
  }
  function getMaintLink(size) {
    return bookBtn?.dataset["maintLink" + capitalize(size)] || getRegularLink(size);
  }
  function priceToNumber(p) {
    return Number(String(p).replace(/[^0-9.]/g, "")) || 0;
  }

  function applyPrice(animate) {
    if (!priceEl) return;
    const regular = getRegularPrice(currentSize);
    const maint = getMaintPrice(currentSize);
    const next = maintenanceMode && maint ? maint : regular;

    if (animate && priceEl.textContent !== next) {
      priceEl.classList.remove("is-flipping");
      void priceEl.offsetWidth;
      priceEl.classList.add("is-flipping");

      setTimeout(() => {
        priceEl.textContent = next;
      }, 200);
    } else {
      priceEl.textContent = next;
    }

    if (originalEl && regular) {
      originalEl.textContent = regular;
    }
    if (saveChipEl && regular && maint) {
      const diff = priceToNumber(regular) - priceToNumber(maint);
      saveChipEl.textContent = diff > 0 ? "Save $" + diff : "";
    }
  }

  function applyBookingLink() {
    if (!bookBtn) return;
    const link = maintenanceMode ? getMaintLink(currentSize) : getRegularLink(currentSize);
    bookBtn.setAttribute("href", link);
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const size = btn.dataset.size;
      currentSize = size;

      buttons.forEach((b) => {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-selected", b === btn ? "true" : "false");
      });

      applyPrice(true);

      if (timeEl && timeEl.dataset["time" + capitalize(size)]) {
        timeEl.textContent = timeEl.dataset["time" + capitalize(size)];
      }

      applyBookingLink();
    });
  });

  if (maintBtn) {
    maintBtn.addEventListener("click", () => {
      maintenanceMode = !maintenanceMode;
      maintBtn.setAttribute("aria-pressed", maintenanceMode ? "true" : "false");
      maintBtn.querySelector(".tier-maint-btn-label").textContent =
        maintenanceMode ? "Maintenance Active" : "Book as Maintenance";
      card.classList.toggle("is-maintenance", maintenanceMode);
      if (bookBtn) {
        bookBtn.textContent = maintenanceMode ? "Book Maintenance" : "Book Premium";
      }
      applyPrice(true);
      applyBookingLink();
    });
  }

  // Initialize
  applyPrice(false);
  applyBookingLink();
});

function capitalize(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}

/* ---------- Scroll reveal (Rise & Fade) ---------- */
(function () {
  var root = document.documentElement;
  // js-anim is set in <head> only when motion is allowed; bail otherwise.
  if (!root.classList.contains("js-anim")) return;

  var targets = document.querySelectorAll("[data-reveal], [data-reveal-group]");
  if (!targets.length) return;

  function revealEl(el) {
    if (el.hasAttribute("data-reveal-group")) {
      var kids = el.children;
      for (var i = 0; i < kids.length; i++) {
        kids[i].style.transitionDelay = Math.min(i * 80, 640) + "ms";
        kids[i].classList.add("is-visible");
      }
    } else {
      el.classList.add("is-visible");
    }
  }

  if (!("IntersectionObserver" in window)) {
    targets.forEach(revealEl);
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      revealEl(e.target);
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });

  targets.forEach(function (el) { io.observe(el); });
})();
