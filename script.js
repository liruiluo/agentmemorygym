/* Optional interaction only. Every result and case stage is present in the HTML. */
'use strict';
const caseButtons = [...document.querySelectorAll('[data-case]')];
caseButtons.forEach(button => button.addEventListener('click', () => {
  caseButtons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  document.querySelectorAll('.case-panel').forEach(panel => panel.classList.toggle('selected', panel.id === button.dataset.case));
  const panel = document.getElementById(button.dataset.case);
  if (window.matchMedia('(max-width: 760px)').matches) {
    panel.scrollIntoView({block: 'start', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  }
}));
const copy = document.getElementById('copy-citation');
if (copy) copy.addEventListener('click', async () => {
  const status = document.getElementById('copy-status');
  const content = document.getElementById('citation-text').textContent;
  try {
    if (!navigator.clipboard) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(content);
    status.textContent = 'BibTeX copied.';
  } catch (_) {
    const range = document.createRange();
    range.selectNodeContents(document.getElementById('citation-text'));
    const selection = window.getSelection();
    selection.removeAllRanges(); selection.addRange(range);
    status.textContent = 'Text selected. Use your system’s Copy command.';
  }
});
