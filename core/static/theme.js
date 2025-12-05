// core/static/theme.js
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("theme-toggle");
  if (!toggle) return;

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
    toggle.textContent = "Modo claro";
  }

  toggle.addEventListener("click", function () {
    const isDark = document.body.classList.toggle("dark");

    if (isDark) {
      localStorage.setItem("theme", "dark");
      toggle.textContent = "Modo claro";
    } else {
      localStorage.setItem("theme", "light");
      toggle.textContent = "Modo escuro";
    }
  });
});
