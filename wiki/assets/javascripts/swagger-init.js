// Render Swagger UI on any page with <div id="swagger-ui" data-spec="...">.
// Replaces the MkDocs-only swagger-ui-tag plugin (specs/zensical-migration.md AC-003).
(function () {
  function render() {
    var el = document.getElementById("swagger-ui");
    if (!el || el.dataset.rendered || typeof SwaggerUIBundle === "undefined") return;
    el.dataset.rendered = "true";
    SwaggerUIBundle({
      url: new URL(el.dataset.spec, window.location.href).href,
      domNode: el,
      deepLinking: true,
      persistAuthorization: false,
    });
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(render); // instant navigation re-renders pages
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
