(function () {
  // Mobile menu
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("navLinks");
  toggle.addEventListener("click", function () {
    var open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  links.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  // Services dropdown (click/tap support)
  document.querySelectorAll(".dropdown").forEach(function (dd) {
    var btn = dd.querySelector(".dropdown__btn");
    btn.addEventListener("click", function () {
      var open = dd.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) {
      if (!dd.contains(e.target)) {
        dd.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  });

  // Scroll reveal
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Footer year
  document.getElementById("year").textContent = new Date().getFullYear();

  // Contact form -> pre-filled email (no backend required)
  var form = document.getElementById("contactForm");
  var note = document.getElementById("formNote");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = form.elements.name, phone = form.elements.phone;
    var ok = true;
    [name, phone].forEach(function (f) {
      var bad = !f.value.trim();
      f.classList.toggle("invalid", bad);
      if (bad) ok = false;
    });
    if (!ok) { note.textContent = "Please add your name and phone number."; return; }

    var interests = Array.prototype.map.call(
      form.querySelectorAll('input[name="interest"]:checked'), function (c) { return c.value; }
    ).join(", ") || "Not specified";
    var body =
      "Name: " + name.value + "\n" +
      "Phone: " + phone.value + "\n" +
      "Email: " + form.elements.email.value + "\n" +
      "City / ZIP: " + form.elements.city.value + "\n" +
      "Interested in: " + interests + "\n\n" +
      form.elements.message.value;
    window.location.href = "mailto:meddy@novaprohome.com?subject=" +
      encodeURIComponent("Free Assessment Request - " + name.value) +
      "&body=" + encodeURIComponent(body);
    note.textContent = "Thanks! Your email app should open now. Prefer to talk? Call (571) 241-9569.";
  });
})();
