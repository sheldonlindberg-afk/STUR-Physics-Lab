/* Service worker retired: unregister any worker left over from STUR v7. */
(function () {
  if (!('serviceWorker' in navigator)) return;
  navigator.serviceWorker.getRegistrations()
    .then(function (regs) { regs.forEach(function (r) { r.unregister(); }); })
    .catch(function () {});
})();
