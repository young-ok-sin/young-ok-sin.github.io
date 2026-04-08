(function () {
  function renderDetailPage() {
    var body = document.body;
    var source = body ? body.dataset.detailSource : "";
    var root = document.getElementById("detail-page-root");
    var fallback = document.getElementById("detail-page-fallback");

    if (!source || !root) {
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
