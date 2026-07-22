document.addEventListener('DOMContentLoaded', function () {

  // Auto-hide alerts after 4 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 4000);
  });

  // Confirm before delete
  const deleteLinks = document.querySelectorAll('[data-confirm]');
  deleteLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // Active nav highlight fallback
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(function (item) {
    if (item.href === window.location.href) {
      item.classList.add('active');
    }
  });

});