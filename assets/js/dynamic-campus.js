// Dynamic Campus Gallery Loader - Indian Central School
(function () {
  const grid = document.getElementById('campus-gallery-grid');
  if (!grid) return;

  async function loadCampus() {
    try {
      const res = await fetch('data/campus.json?_t=' + Date.now());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const items = await res.json();
      if (!Array.isArray(items) || items.length === 0) return;

      grid.innerHTML = items.map((c, idx) => `
        <div class="group relative rounded-2xl overflow-hidden border border-[#E6DFC9] bg-white shadow-xs hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 ${idx === 0 ? 'sm:col-span-2 lg:col-span-1' : ''}">
          <div class="h-64 overflow-hidden cursor-pointer lightbox-trigger" data-img-src="${escapeHtml(c.image)}" data-caption="${escapeHtml(c.title)}">
            <img src="${escapeHtml(c.image)}" alt="${escapeHtml(c.title)}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" onerror="this.src='assets/logo.png'" />
          </div>
          <div class="p-4 bg-white border-t border-[#F0EAE1]">
            <span class="text-[10px] font-extrabold uppercase tracking-wider text-amber-700 bg-amber-50 px-2 py-0.5 rounded">${escapeHtml(c.category || 'Campus')}</span>
            <h4 class="font-serif font-bold text-sm text-brand-navy mt-1">${escapeHtml(c.title)}</h4>
            <p class="text-[11.5px] text-slate-500 mt-0.5">${escapeHtml(c.description || '')}</p>
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.warn('Could not load dynamic campus.json:', e);
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  loadCampus();
})();
