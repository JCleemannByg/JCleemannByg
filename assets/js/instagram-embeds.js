/**
 * Instagram post embeds — click to load.
 *
 * Nothing from Instagram (no script, no cookie) is loaded until the visitor
 * activates a post tile. The official embed script is then injected once and
 * the clicked post is rendered with Instagram's own markup.
 */
(() => {
  const panel = document.querySelector('[data-ig-panel]');
  if (!panel) return;

  const slot = panel.querySelector('[data-ig-slot]');
  const openLink = panel.querySelector('[data-ig-open]');
  const closeButton = panel.querySelector('[data-ig-close]');
  const tiles = Array.from(document.querySelectorAll('[data-ig-post]'));
  let scriptLoaded = false;
  let lastTrigger = null;

  const showEmbed = (url) => {
    slot.replaceChildren();
    const quote = document.createElement('blockquote');
    quote.className = 'instagram-media';
    quote.setAttribute('data-instgrm-permalink', url);
    quote.setAttribute('data-instgrm-version', '14');
    quote.style.maxWidth = '540px';
    quote.style.margin = '0 auto';
    quote.style.border = '0';
    slot.append(quote);

    if (window.instgrm && window.instgrm.Embeds) {
      window.instgrm.Embeds.process();
      return;
    }
    if (scriptLoaded) return;
    scriptLoaded = true;
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.instagram.com/embed.js';
    script.addEventListener('load', () => {
      if (window.instgrm && window.instgrm.Embeds) window.instgrm.Embeds.process();
    });
    document.body.append(script);
  };

  const close = () => {
    if (panel.hidden) return;
    panel.hidden = true;
    slot.replaceChildren();
    tiles.forEach((tile) => tile.setAttribute('aria-expanded', 'false'));
    if (lastTrigger) lastTrigger.focus();
  };

  tiles.forEach((tile) => {
    tile.addEventListener('click', () => {
      const url = tile.getAttribute('data-ig-post');
      if (!url) return;
      if (!panel.hidden && openLink.dataset.url === url) {
        close();
        return;
      }
      openLink.href = url;
      openLink.dataset.url = url;
      showEmbed(url);
      panel.hidden = false;
      tiles.forEach((t) => t.setAttribute('aria-expanded', String(t === tile)));
      lastTrigger = tile;
      panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      closeButton.focus({ preventScroll: true });
    });
  });

  closeButton.addEventListener('click', close);
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });
})();
