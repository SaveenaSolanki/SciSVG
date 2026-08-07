const OWNER = "SaveenaSolanki";
const REPO = "SciSVG";
const BRANCH = "main";
const RAW_BASE = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/`;
const REPO_URL = `https://github.com/${OWNER}/${REPO}`;
const CITATION = `SciSVG \u2014 Saveena Solanki, CC BY 4.0, ${REPO_URL}`;

const grid = document.getElementById("grid");
const empty = document.getElementById("empty");
const search = document.getElementById("search");
const category = document.getElementById("category");
const chips = document.getElementById("chips");
const count = document.getElementById("count");
const modal = document.getElementById("modal");

let assets = [];
let fuse = null;

const FUSE_OPTIONS = {
  keys: ["name", "description", "tags", "category", "subcategory", "contributor"],
  threshold: 0.35,
  ignoreLocation: true,
  minMatchCharLength: 2,
};

function rawUrl(path) {
  return RAW_BASE + path.split("/").map(encodeURIComponent).join("/");
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
}

function flash(button, label) {
  const old = button.textContent;
  button.textContent = label;
  setTimeout(() => (button.textContent = old), 1200);
}

function metaLine(asset) {
  return [asset.category, asset.subcategory].filter(Boolean).join(" \u00b7 ");
}

function card(asset) {
  const url = rawUrl(asset.path);
  const article = document.createElement("article");
  article.className = "card";

  const preview = document.createElement("div");
  preview.className = "preview";
  const img = document.createElement("img");
  img.src = url;
  img.alt = asset.name;
  img.loading = "lazy";
  preview.appendChild(img);

  const body = document.createElement("div");
  body.className = "card-body";

  const title = document.createElement("h2");
  title.textContent = asset.name;

  const meta = document.createElement("p");
  meta.className = "meta";
  meta.textContent = metaLine(asset);
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

  const details = document.createElement("button");
  details.className = "button";
  details.textContent = "Details";
  details.addEventListener("click", () => openModal(asset));

  const cite = document.createElement("button");
  cite.className = "button";
  cite.textContent = "Copy citation";
  cite.addEventListener("click", async () => {
    await copyText(CITATION);
    flash(cite, "Copied");
  });

  actions.append(download, details, cite);
  body.append(title, meta, desc, actions);
  article.append(preview, body);
  return article;
}

function openModal(asset) {
  const url = rawUrl(asset.path);
  modal.querySelector("#modal-img").src = url;
  modal.querySelector("#modal-img").alt = asset.name;
  modal.querySelector("#modal-title").textContent = asset.name;
  modal.querySelector("#modal-meta").textContent = metaLine(asset);
  modal.querySelector("#modal-desc").textContent = asset.description || "";
  modal.querySelector("#modal-contributor").textContent =
    asset.contributor + (asset.orcid ? ` (ORCID ${asset.orcid})` : "");
  modal.querySelector("#modal-version").textContent = asset.version || "1.0.0";
  modal.querySelector("#modal-category").textContent =
    metaLine(asset) || asset.category;
  const review = asset.scientifically_reviewed
    ? "Scientifically reviewed"
    : "Technical review passed; scientific review pending";
  modal.querySelector("#modal-review").textContent = review;

  const dl = modal.querySelector("#btn-download");
  dl.onclick = async () => {
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
  };

  const cs = modal.querySelector("#btn-copy-svg");
  cs.onclick = async () => {
    const response = await fetch(url);
    const text = await response.text();
    await copyText(text);
    flash(cs, "Copied");
  };

  const ct = modal.querySelector("#btn-cite");
  ct.onclick = async () => {
    await copyText(CITATION);
    flash(ct, "Copied");
  };

  modal.querySelector("#btn-source").href = url;
  modal.hidden = false;
  document.body.classList.add("modal-open");
}

function closeModal() {
  modal.hidden = true;
  document.body.classList.remove("modal-open");
}

function render() {
  const q = search.value.trim().toLowerCase();
  const cat = category.value;
  let filtered = assets;
  if (q) {
    filtered = fuse ? fuse.search(q).map((r) => r.item) : assets.filter((a) =>
      [a.name, a.category, a.subcategory, a.filename, a.description, ...(a.tags || [])]
        .join(" ")
        .toLowerCase()
        .includes(q)
    );
  }
  if (cat !== "all") {
    filtered = filtered.filter((a) => a.category === cat);
  }

  grid.replaceChildren(...filtered.map(card));
  count.textContent = `${filtered.length} asset${filtered.length === 1 ? "" : "s"}`;
  empty.hidden = filtered.length !== 0;
}

function buildChips() {
  const cats = [...new Set(assets.map((a) => a.category))].sort();
  cats.forEach((c) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = c.replaceAll("-", " ");
    chip.addEventListener("click", () => {
      category.value = category.value === c ? "all" : c;
      [...chips.children].forEach((el) => el.classList.toggle("active", el === chip));
      render();
    });
    chips.appendChild(chip);
  });
}

fetch("catalog.json")
  .then((r) => r.json())
  .then((data) => {
    assets = data.assets || [];
    fuse = typeof Fuse !== "undefined" ? new Fuse(assets, FUSE_OPTIONS) : null;
    [...new Set(assets.map((a) => a.category))].sort().forEach((cat) => {
      const opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = cat.replaceAll("-", " ");
      category.appendChild(opt);
    });
    buildChips();
    render();
  })
  .catch(() => {
    assets = [];
    render();
  });

search.addEventListener("input", render);
category.addEventListener("change", () => {
  const cat = category.value;
  [...chips.children].forEach((el) =>
    el.classList.toggle("active", el.textContent === cat.replaceAll("-", " "))
  );
  render();
});

modal.querySelectorAll("[data-close]").forEach((el) =>
  el.addEventListener("click", closeModal)
);
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});
