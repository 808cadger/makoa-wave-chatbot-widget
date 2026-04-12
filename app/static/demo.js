document.addEventListener("DOMContentLoaded", function () {
  const presetButtons = Array.from(document.querySelectorAll("[data-preset]"));
  const contextField = document.querySelector("#context-field");
  const placeholderField = document.querySelector("#placeholder-field");
  const titleField = document.querySelector("#title-field");
  const openButton = document.querySelector("#open-widget");
  const fillButtons = Array.from(document.querySelectorAll("[data-fill]"));

  const presets = {
    tours: {
      title: "Book with Makoa~Wave",
      placeholder: "Ask about tours, pricing, or availability...",
      context:
        "Business name: Makoa~Wave\nVertical: Hawaii tour operator\nOffers: snorkel tour $89 adult, sunset cruise $129 adult, private charter from $499\nCTA: Book at makoawave.demo/book\nEscalation: text 808-555-0144",
    },
    salon: {
      title: "Spa Concierge",
      placeholder: "Ask about facials, timings, or packages...",
      context:
        "Business name: Makoa~Wave Glow Studio\nVertical: spa and skincare studio\nOffers: express facial $65, glow facial $110, membership from $79 monthly\nCTA: Reserve at makoawave.demo/glow\nEscalation: hello@makoawave.demo",
    },
    retail: {
      title: "Store Support",
      placeholder: "Ask about shipping, bundles, or returns...",
      context:
        "Business name: Makoa~Wave Market\nVertical: ecommerce store\nOffers: reef-safe sunscreen $24, after-sun bundle $42, free shipping over $75\nCTA: Shop at makoawave.demo/shop\nEscalation: support@makoawave.demo",
    },
  };

  function applyPreset(key) {
    const preset = presets[key];
    if (!preset) return;

    titleField.value = preset.title;
    placeholderField.value = preset.placeholder;
    contextField.value = preset.context;

    if (window.MakoaWaveWidget) {
      window.MakoaWaveWidget.setTitle(preset.title);
      window.MakoaWaveWidget.setPlaceholder(preset.placeholder);
      window.MakoaWaveWidget.setContext(preset.context);
    }

    presetButtons.forEach(function (button) {
      button.classList.toggle("is-active", button.dataset.preset === key);
    });
  }

  presetButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      applyPreset(button.dataset.preset);
    });
  });

  contextField.addEventListener("input", function () {
    if (window.MakoaWaveWidget) {
      window.MakoaWaveWidget.setContext(contextField.value);
    }
  });

  placeholderField.addEventListener("input", function () {
    if (window.MakoaWaveWidget) {
      window.MakoaWaveWidget.setPlaceholder(placeholderField.value);
    }
  });

  titleField.addEventListener("input", function () {
    if (window.MakoaWaveWidget) {
      window.MakoaWaveWidget.setTitle(titleField.value);
    }
  });

  openButton.addEventListener("click", function () {
    if (window.MakoaWaveWidget) {
      window.MakoaWaveWidget.open();
    }
  });

  fillButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      if (window.MakoaWaveWidget) {
        window.MakoaWaveWidget.open();
        window.MakoaWaveWidget.fillInput(button.dataset.fill);
      }
    });
  });

  applyPreset("tours");
});
