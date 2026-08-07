const OWNER = "SaveenaSolanki";
const REPO = "SciSVG";
const BRANCH = "main";
const RAW_BASE = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/`;
const CITATION = `SciSVG \u2014 Saveena Solanki, CC BY 4.0, https://github.com/${OWNER}/${REPO}`;

const grid = document.getElementById("grid");
const empty = document.getElementById("empty");
const search = document.getElementById("search");
const category = document.getElementById("category");
const count = document.getElementById("count");

let assets = [];

function rawUrl(path) {
  return RAW_BASE + path.split("/").map(encodeURIComponent).join("/");
}

function card(asset) {
  const url = rawUrl(asset.path);
  const article = document.createElement("article");
  article.className = "card";

  const preview = document.createElement("div");
  preview.className = "preview";
  const img = document.createElement("img");
  img.src = url;
  img.alt = asset.title;
  img.loading = "lazy";
  preview.appendChild(img);

  const body = document.createElement("div");
  body.className = "card-body";

  const title = document.createElement("h2");
  title.textContent = asset.title;

  const meta = document.createElement("p");
  meta.className = "meta";
  meta.textContent = (asset.category || "").replaceAll("/", " \u00b7 ");
  const badge = document.createElement("span");
  badge.className = "badge";
  badge.textContent = asset.license || "CC BY 4.0";
  meta.appendChild(badge);

  const desc = document.createElement("p");
  desc.className = "desc";
  desc.textContent = asset.description || "";

  const actions = document.createElement("div");
  actions.className = "actions";

  const download = document.createElement("button");
  download.className = "button primary";
  download.textContent = "Download SVG";
  download.addEventListener("click", async () => {
    const response = await fetch(url);
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = objectUrl;
    a.download = asset.filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(objectUrl);
  });

  const cite = document.createElement("button");
  cite.className = "button";
  cite.textContent = "Copy citation";
  cite.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(CITATION);
    } catch (err) {
      const ta = document.createElement("textarea");
      ta.value = CITATION;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    }
    const old = cite.textContent;
    cite.textContent = "Copied";
    setTimeout(() => (cite.textContent = old), 1200);
  });

  actions.append(download, cite);
  body.append(title, meta, desc, actions);
  article.append(preview, body);
  return article;
}

function render() {
  const q = search.value.trim().toLowerCase();
  const cat = category.value;
  const filtered = assets.filter((a) => {
    const haystack = [
      a.title,
      a.category,
      a.filename,
      a.description,
      ...(a.tags || []),
    ]
      .join(" ")
      .toLowerCase();
    return (cat === "all" || a.category === cat) && (!q || haystack.includes(q));
  });

  grid.replaceChildren(...filtered.map(card));
  count.textContent = `${filtered.length} asset${filtered.length === 1 ? "" : "s"}`;
  empty.hidden = filtered.length !== 0;
}

fetch("catalog.json")
  .then((r) => r.json())
  .then((data) => {
    assets = data.assets || [];
    [...new Set(assets.map((a) => a.category))].sort().forEach((cat) => {
      const opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = cat.replaceAll("/", " \u00b7 ");
      category.appendChild(opt);
    });
    render();
  })
  .catch(() => {
    assets = [];
    render();
  });

search.addEventListener("input", render);
category.addEventListener("change", render);
