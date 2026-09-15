document.addEventListener("DOMContentLoaded", function () {
  // phone menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.classList.toggle("is-open", isOpen);
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  // counter down offers
  var countdown = document.querySelector(".countdown");
  if (countdown) {
    var persianDigits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    var toPersianDigits = function (n) {
      return String(n)
        .split("")
        .map(function (ch) {
          return /\d/.test(ch) ? persianDigits[ch] : ch;
        })
        .join("");
    };

    // set time offer
    var endOfDay = new Date();
    endOfDay.setFullYear(2026,8,20);//set date TODO:set in admin panel
    endOfDay.setHours(24, 0, 0, 0);

    var hoursEl = countdown.querySelector(".countdown-unit:nth-child(5) .countdown-value");
    var minutesEl = countdown.querySelector(".countdown-unit:nth-child(3) .countdown-value");
    var secondsEl = countdown.querySelector(".countdown-unit:nth-child(1) .countdown-value");

    function tick() {
      var diff = Math.max(0, endOfDay - new Date());
      var h = Math.floor(diff / 3600000);
      var m = Math.floor((diff % 3600000) / 60000);
      var s = Math.floor((diff % 60000) / 1000);

      if (hoursEl) hoursEl.textContent = toPersianDigits(String(h).padStart(2, "0"));
      if (minutesEl) minutesEl.textContent = toPersianDigits(String(m).padStart(2, "0"));
      if (secondsEl) secondsEl.textContent = toPersianDigits(String(s).padStart(2, "0"));
    }

    tick();
    setInterval(tick, 1000);
  }
});
