const environmentData = {
  shop: {
    title: "Shop",
    counter: "01 / 04",
    description: "Search, compare, and purchase under a budget while keeping product evidence and constraints available over a long interaction.",
    native: "browse + buy",
    memory: "preferences, evidence",
    file: ".agent_memory/preferences.md",
    footer: "A task-native world, one shared memory substrate."
  },
  coding: {
    title: "Coding",
    counter: "02 / 04",
    description: "Reproduce a failure, inspect a codebase, patch the right file, and verify the result after the task has outgrown the active context.",
    native: "shell + patch",
    memory: "tests, decisions",
    file: ".agent_memory/CONTINUATION.md",
    footer: "The agent writes the evidence trail it will need later."
  },
  research: {
    title: "DeepResearch",
    counter: "03 / 04",
    description: "Gather and synthesize evidence over many searches, keeping sources, claims, and unfinished lines of inquiry available across turns.",
    native: "search + synthesize",
    memory: "sources, claims",
    file: ".agent_memory/source_map.md",
    footer: "Research state stays editable, searchable, and grounded."
  },
  auto: {
    title: "AutoResearch",
    counter: "04 / 04",
    description: "Iterate on a data-science task by writing experiments, inspecting outputs, and reusing the growing record of what worked.",
    native: "run + evaluate",
    memory: "experiments, results",
    file: ".agent_memory/experiment_log.md",
    footer: "A durable lab notebook emerges from ordinary file operations."
  }
};

function initIcons() {
  if (window.lucide) window.lucide.createIcons();
}

function initEnvironmentTabs() {
  const tabs = [...document.querySelectorAll(".env-tab")];
  const next = document.querySelector("#env-next");
  const title = document.querySelector("#env-title");
  const counter = document.querySelector("#env-counter");
  const description = document.querySelector("#env-description");
  const native = document.querySelector("#env-native");
  const memory = document.querySelector("#env-memory");
  const file = document.querySelector("#env-file");
  const footer = document.querySelector("#env-footer-copy");
  let activeIndex = 0;

  function selectEnvironment(key) {
    const data = environmentData[key];
    activeIndex = tabs.findIndex((tab) => tab.dataset.env === key);
    tabs.forEach((tab) => {
      const selected = tab.dataset.env === key;
      tab.classList.toggle("is-active", selected);
      tab.setAttribute("aria-selected", String(selected));
    });
    title.textContent = data.title;
    counter.textContent = data.counter;
    description.textContent = data.description;
    native.textContent = data.native;
    memory.textContent = data.memory;
    file.textContent = data.file;
    footer.textContent = data.footer;
  }

  tabs.forEach((tab) => tab.addEventListener("click", () => selectEnvironment(tab.dataset.env)));
  next?.addEventListener("click", () => selectEnvironment(tabs[(activeIndex + 1) % tabs.length].dataset.env));
}

function initChart() {
  const buttons = [...document.querySelectorAll(".legend-button")];
  const valueMap = {
    camg: ["97.1%", "26.6%", "55.5%", "38.3%"],
    compact: ["97.5%", "19.5%", "50.8%", "24.2%"],
    base: ["11.6%", "10.9%", "36.7%", "10.2%"]
  };
  buttons.forEach((button) => button.addEventListener("click", () => {
    const series = button.dataset.series;
    buttons.forEach((item) => item.classList.toggle("is-active", item === button));
    document.querySelectorAll(".chart-row").forEach((row, index) => {
      row.querySelectorAll(".bar").forEach((bar) => bar.classList.toggle("is-hidden", !bar.classList.contains(`bar-${series}`)));
      row.querySelector(".bar-value").textContent = valueMap[series][index];
    });
  }));
}

function initReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach((item) => item.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver((entries, io) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -34px" });
  items.forEach((item) => observer.observe(item));
}

function initCitation() {
  const button = document.querySelector("#copy-citation");
  const original = button?.querySelector("span")?.textContent || "Copy citation";
  const citation = "Luo, Lirui; Mao, Kelong; Xia, Heming; Li, Rongqing; Yang, Xinwei; Chen, Luyu; Wong, Kieran; Guo, Yudong; Wang, Xinrui; Zhu, Jiayin; Gu, Simiu; Xu, Sulong; Fang, Cong. Coding Agent Memory Post-training: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via Reinforcement Learning. arXiv:2609.34422, 2026.";
  button?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(citation);
      button.querySelector("span").textContent = "Citation copied";
      setTimeout(() => { button.querySelector("span").textContent = original; }, 1800);
    } catch {
      button.querySelector("span").textContent = "Select from paper PDF";
      setTimeout(() => { button.querySelector("span").textContent = original; }, 1800);
    }
  });
}

initEnvironmentTabs();
initChart();
initReveal();
initCitation();
initIcons();
