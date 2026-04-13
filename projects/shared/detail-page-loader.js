(function () {
  var DETAIL_ASSET_VERSION = "20260413-encoding";
  var zoomDialog = null;

  function versionSvgAsset(img) {
    var rawSrc = img.getAttribute("src");

    if (!rawSrc) {
      return;
    }

    try {
      var url = new URL(rawSrc, window.location.href);

      if (url.pathname.slice(-4).toLowerCase() !== ".svg") {
        return;
      }

      url.searchParams.set("v", DETAIL_ASSET_VERSION);
      img.src = url.href;
    } catch (error) {
      console.error(error);
    }
  }

  function getZoomDialog() {
    if (zoomDialog) {
      return zoomDialog;
    }

    zoomDialog = document.createElement("dialog");
    zoomDialog.className = "doc-zoom-dialog";
    zoomDialog.innerHTML = [
      '<button class="doc-zoom-close" type="button" aria-label="Close enlarged diagram">Close</button>',
      '<div class="doc-zoom-frame">',
      '<img class="doc-zoom-image" alt="">',
      '<p class="doc-zoom-caption"></p>',
      "</div>",
    ].join("");

    zoomDialog.addEventListener("click", function (event) {
      if (event.target === zoomDialog) {
        zoomDialog.close();
      }
    });

    zoomDialog.querySelector(".doc-zoom-close").addEventListener("click", function () {
      zoomDialog.close();
    });

    document.body.appendChild(zoomDialog);
    return zoomDialog;
  }

  function openZoomedFigure(img) {
    var figure = img.closest(".doc-figure");
    var caption = figure ? figure.querySelector("figcaption") : null;
    var dialog = getZoomDialog();
    var zoomImage = dialog.querySelector(".doc-zoom-image");
    var zoomCaption = dialog.querySelector(".doc-zoom-caption");

    zoomImage.src = img.currentSrc || img.src;
    zoomImage.alt = img.alt || "";
    zoomCaption.textContent = caption ? caption.textContent.trim() : "";
    zoomCaption.hidden = !zoomCaption.textContent;

    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
  }

  function setupFigureZoom(scope) {
    var root = scope || document;
    var images = root.querySelectorAll(".doc-figure img");

    Array.prototype.forEach.call(images, function (img) {
      if (img.getAttribute("data-zoom-ready") === "true") {
        return;
      }

      versionSvgAsset(img);
      img.setAttribute("data-zoom-ready", "true");
      img.setAttribute("role", "button");
      img.setAttribute("tabindex", "0");
      img.setAttribute("aria-label", "Open enlarged diagram");

      img.addEventListener("click", function () {
        openZoomedFigure(img);
      });

      img.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openZoomedFigure(img);
        }
      });
    });
  }

  function renderDetailPage() {
    var body = document.body;
    var source = body ? body.dataset.detailSource : "";
    var root = document.getElementById("detail-page-root");
    var fallback = document.getElementById("detail-page-fallback");

    if (!source || !root) {
      setupFigureZoom(document);
      return;
    }

    fetch(source, { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Failed to load detail page: " + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        var parsed = new DOMParser().parseFromString(html, "text/html");

        if (parsed.title) {
          document.title = parsed.title;
        }

        if (parsed.body.className) {
          body.className = parsed.body.className;
        }

        root.innerHTML = parsed.body.innerHTML;
        root.hidden = false;
        setupFigureZoom(root);

        if (fallback) {
          fallback.remove();
        }
      })
      .catch(function (error) {
        if (fallback) {
          fallback.textContent = "Detail page failed to load.";
        }
        console.error(error);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderDetailPage, { once: true });
  } else {
    renderDetailPage();
  }
})();
