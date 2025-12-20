/**
 * Valyxo GitHub Stats Fetcher (JavaScript Fallback)
 * Ports the statistics fetching from Rust WASM to pure JS.
 */

const REPO = "SandwichEater577/Valyxo";
const COLORS = {
  Rust: "#dea584",
  JavaScript: "#f1e05a",
  TypeScript: "#3178c6",
  Python: "#3572A5",
  HTML: "#e34c26",
  CSS: "#563d7c",
  Go: "#00ADD8",
  Makefile: "#427819",
};

export async function updateStats() {
  const starCount = document.getElementById("star-count");
  const forkCount = document.getElementById("fork-count");
  const issueCount = document.getElementById("issue-count");

  if (starCount) starCount.textContent = "Loading...";

  try {
    const response = await fetch(`https://api.github.com/repos/${REPO}`);
    if (!response.ok) throw new Error("GitHub API Error");
    const data = await response.json();

    if (starCount) starCount.textContent = `${data.stargazers_count} stars`;
    if (forkCount) forkCount.textContent = `${data.forks_count} forks`;
    if (issueCount) issueCount.textContent = `${data.open_issues_count} issues`;
  } catch (e) {
    console.error("Failed to fetch stats:", e);
  }
}

export async function updateContributors() {
  const container = document.getElementById("contributors-list");
  if (!container) return;

  try {
    const response = await fetch(
      `https://api.github.com/repos/${REPO}/contributors`
    );
    if (!response.ok) throw new Error("GitHub API Error");
    const contributors = await response.json();

    // Filter out specific users if requested in original Rust (skipped for simplicity here unless found)
    const list = contributors.filter(
      (c) => c.login.toLowerCase() !== "michalmazur"
    );

    container.innerHTML = "";
    for (const c of list) {
      const a = document.createElement("a");
      a.href = c.html_url;
      a.target = "_blank";
      a.className = "contributor";

      const img = document.createElement("img");
      img.src = c.avatar_url;
      img.className = "contributor-avatar-img";

      const name = document.createElement("span");
      name.textContent = c.login;

      const commits = document.createElement("span");
      commits.className = "contributor-commits";
      commits.textContent = `${c.contributions} commits`;

      a.appendChild(img);
      a.appendChild(name);
      a.appendChild(commits);
      container.appendChild(a);
    }
  } catch (e) {
    console.error("Failed to fetch contributors:", e);
  }
}

export async function updateLanguages() {
  const bar = document.getElementById("language-bar");
  const list = document.getElementById("language-list");
  if (!bar || !list) return;

  try {
    const response = await fetch(
      `https://api.github.com/repos/${REPO}/languages`
    );
    if (!response.ok) throw new Error("GitHub API Error");
    const languages = await response.json();
    const total = Object.values(languages).reduce((a, b) => a + b, 0);

    bar.innerHTML = "";
    list.innerHTML = "";

    const sorted = Object.entries(languages).sort((a, b) => b[1] - a[1]);

    for (const [lang, bytes] of sorted) {
      const percent = (bytes / total) * 100;
      if (percent < 0.5) continue;

      const color = COLORS[lang] || "#ccc";

      // Bar segment
      const segment = document.createElement("div");
      segment.className = "lang-segment";
      segment.style.width = `${percent}%`;
      segment.style.background = color;
      segment.title = `${lang}: ${percent.toFixed(1)}%`;
      bar.appendChild(segment);

      // List item
      const item = document.createElement("div");
      item.className = "lang-item";
      item.innerHTML = `
                <span class="lang-dot" style="background: ${color}"></span>
                ${lang}
                <span class="lang-percent">${percent.toFixed(1)}%</span>
            `;
      list.appendChild(item);
    }
  } catch (e) {
    console.error("Failed to fetch languages:", e);
  }
}
