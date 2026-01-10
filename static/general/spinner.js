// static/js/pinner.js

(function () {
  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (!form.classList.contains('pinner-form')) return;

    const button = form.querySelector('button[type="submit"]');
    if (!button || button.dataset.pinned === 'true') return;

    e.preventDefault();

    // Read config
    const spinnerText = button.dataset.spinnerText || 'Loading...';
    const spinnerClass = button.dataset.spinnerClass;

    // Save state
    button.dataset.originalHtml = button.innerHTML;
    button.dataset.pinned = 'true';

    // Disable
    button.disabled = true;

    // Change Bootstrap color if provided
    if (spinnerClass) {
      button.className = `btn ${spinnerClass}`;
    }

    // Bootstrap spinner
    button.innerHTML = `
      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
      ${spinnerText}
    `;

    // Let Django handle submission
    form.submit();
  });
})();
