/* Capture card actions — three buttons, one delegated handler.
 *
 * DELEGATION IS NOT OPTIONAL. The working page carries the post-mortem:
 * "the static cards carried no such class, so it bound to nothing, and the
 *  action was a bare anchor to #slug — navigating to the card the reader was
 *  already looking at. It appeared to do nothing because it did nothing."
 * render() hides and shows cards rather than rebuilding them, so a per-render
 * handler would be attached once and then own a DOM it no longer controls.
 * Bind to the container. Once.
 */
(function () {
  var caps = document.getElementById('captures');
  if (!caps) return;

  function flash(btn, msg) {
    var t = btn.textContent;
    btn.textContent = msg;
    btn.classList.add('ok');
    setTimeout(function () { btn.textContent = t; btn.classList.remove('ok'); }, 1600);
  }

  function copy(btn, text, okMsg) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { flash(btn, okMsg); },
        function () { flash(btn, text); }
      );
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'absolute';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); flash(btn, okMsg); }
    catch (e) { flash(btn, text); }
    document.body.removeChild(ta);
  }

  caps.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.cap-act');
    if (!b) return;
    ev.preventDefault();

    var url  = b.dataset.cite || '';
    var slug = url.split('#')[1] || '';

    /* Every action that has a URL also parks it in the address bar, so the
       reader's back button and their next copy agree with what they clicked. */
    if (slug) history.replaceState(null, '', '#' + slug);

    switch (b.dataset.act) {

      /* CITE — copies the CITATION, not the bare URL. A reader clicking cite
         wants something pasteable into a document, and the URL is inside it. */
      case 'cite':
        copy(b, b.dataset.citation || url, '¶ Copied');
        break;

      /* LINK — copies the bare permalink. Distinct from cite on purpose:
         sometimes the reader wants the address and nothing else. */
      case 'link':
        copy(b, url, '⛓ Copied');
        break;

      /* RERUN — opens the SAME SEMANTIC ADDRESS live, so the capture becomes a
         repeatable experiment and the reader can see the current state against
         this dated baseline.
         The URL is DATA, built by the pipeline and carried on the card. It is
         never assembled here: the query must be reproduced exactly, quotation
         marks included, because quoting is the decisive variable in this
         corpus — «operative semiotics» held 5/5 archive cards quoted and 1/8
         unquoted. A re-run that drops the quotes is not a re-run of this
         address. */
      case 'rerun':
        var target = b.dataset.rerun;
        if (!target) { flash(b, 'no target for this surface'); break; }
        window.open(target, '_blank', 'noopener');
        break;
    }
  });
})();
