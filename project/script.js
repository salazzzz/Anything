const sliderCards = Array.from(document.querySelectorAll(".slide-card"));
const sliderPrev = document.getElementById("slider-prev");
const sliderNext = document.getElementById("slider-next");

let currentCenterIndex = 0;

function renderSliderPositions() {
  const total = sliderCards.length;

  sliderCards.forEach((card, index) => {
    card.classList.remove("left", "center", "right", "hidden-left", "hidden-right");

    if (index === currentCenterIndex) {
      card.classList.add("center");
    } 
    else if (index === (currentCenterIndex - 1 + total) % total) {
      card.classList.add("left");
    } 
    else if (index === (currentCenterIndex + 1) % total) {
      card.classList.add("right");
    } 
    else if (index < currentCenterIndex) {
      card.classList.add("hidden-left");
    } 
    else {
      card.classList.add("hidden-right");
    }
  });
}

function moveSliderNext() {
  currentCenterIndex = (currentCenterIndex + 1) % sliderCards.length;
  renderSliderPositions();
}

function moveSliderPrev() {
  currentCenterIndex = (currentCenterIndex - 1 + sliderCards.length) % sliderCards.length;
  renderSliderPositions();
}

if (sliderNext) sliderNext.addEventListener("click", moveSliderNext);
if (sliderPrev) sliderPrev.addEventListener("click", moveSliderPrev);

renderSliderPositions();

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
  // Initialize at 50
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

  // Keep the range input working for keyboard / a11y
  if (comparisonSlider) {
    comparisonSlider.addEventListener("input", (e) => updateComparison(e.target.value));
  }
}

/* ---------- Footer year ---------- */
const footerYear = document.getElementById("footer-year");
if (footerYear) footerYear.textContent = new Date().getFullYear();

/* ---------- Vehicle size selector (service detail pages) ---------- */
document.querySelectorAll(".tier-card").forEach((card) => {
  const buttons = card.querySelectorAll(".size-option");
  const priceEl = card.querySelector(".tier-price-value");
  const timeEl = card.querySelector(".tier-time-value");
  const bookBtn = card.querySelector(".tier-book-btn");
  const maintBtn = card.querySelector(".tier-maint-btn");

  let currentSize = "sedan";
  let maintenanceMode = false;

  // Decorate the price element with a strike-through original + save chip wrapper
  // (only relevant for cards that support maintenance, but harmless otherwise)
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
      // force reflow so animation restarts
      void priceEl.offsetWidth;
      priceEl.classList.add("is-flipping");

      // Swap text at midpoint of flip
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
      if (bookBtn && bookBtn.dataset["link" + capitalize(size)]) {
        bookBtn.setAttribute("href", bookBtn.dataset["link" + capitalize(size)]);
      }
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
    });
  }

  // Initialize
  applyPrice(false);
});

function capitalize(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}
