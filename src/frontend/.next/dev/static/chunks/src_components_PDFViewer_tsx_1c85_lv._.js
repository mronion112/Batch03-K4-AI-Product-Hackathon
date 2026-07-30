(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/src/components/PDFViewer.tsx [app-client] (ecmascript, next/dynamic entry, async loader)", ((__turbopack_context__) => {

__turbopack_context__.v((parentImport) => {
    return Promise.all([
  "static/chunks/node_modules_1-hwjic._.js",
  "static/chunks/src_components_PDFViewer_tsx_0fwg2p8._.js",
  {
    "path": "static/chunks/node_modules_react-pdf_dist_Page_0vn2xto._.css",
    "included": [
      "[project]/node_modules/react-pdf/dist/Page/AnnotationLayer.css [app-client] (css)",
      "[project]/node_modules/react-pdf/dist/Page/TextLayer.css [app-client] (css)"
    ],
    "moduleChunks": [
      "static/chunks/node_modules_react-pdf_dist_Page_AnnotationLayer_css_1igg3k2._.single.css",
      "static/chunks/node_modules_react-pdf_dist_Page_TextLayer_css_1igg3k2._.single.css"
    ]
  },
  "static/chunks/src_components_PDFViewer_tsx_0sjcrc2._.js"
].map((chunk) => __turbopack_context__.l(chunk))).then(() => {
        return parentImport("[project]/src/components/PDFViewer.tsx [app-client] (ecmascript, next/dynamic entry)");
    });
});
}),
]);