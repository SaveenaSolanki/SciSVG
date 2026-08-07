module.exports = {
  multipass: true,
  js2svg: {
    pretty: true,
    indent: 2,
  },
  plugins: [
    {
      name: "preset-default",
      params: {
        overrides: {
          // Keep the viewBox: assets are standardized on 0 0 512 512.
          removeViewBox: false,
          // Keep meaningful IDs (named layers/groups).
          cleanupIds: false,
          // Keep SciSVG attribution comments; strip the rest.
          removeComments: {
            preservePatterns: ["CC BY 4.0", "SciSVG", "Saveena Solanki"],
          },
          // Keep accessibility metadata.
          removeTitle: false,
          removeDesc: false,
          // Editability first: keep named groups as real layers, keep
          // rects/circles/ellipses as shapes, and do not merge separate
          // paths (users must be able to recolor individual elements).
          collapseGroups: false,
          moveGroupAttrsToElems: false,
          mergePaths: false,
          convertShapeToPath: false,
        },
      },
    },
  ],
};
