// Dynamic Achievements Loader - Indian Central School
(function () {
  const grid = document.getElementById('ach-cards-grid');
  const filterBtns = document.querySelectorAll('.ach-filter-btn');
  if (!grid) return;

  let allAchievements = [];
  let currentCategory = 'all';

  async function loadAchievements() {
    try {
      const res = await fetch('data/achievements.json?_t=' + Date.now());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      allAchievements = await res.json();
      render();
    } catch (e) {
      console.warn('Could not load dynamic achievements.json:', e);
    }
  }

  function render() {
    const filtered = allAchievements.filter(a => {
      if (currentCategory === 'all') return true;
      const cat = (a.category || '').toLowerCase().replace(/\s+/g, '');
      if (currentCategory === 'halloffame' && cat.includes('halloffame')) return true;
      if (currentCategory === 'principal-awards' && (cat.includes('leadership') || cat.includes('principal'))) return true;
      if (currentCategory === 'student-awards' && (cat.includes('student') || cat.includes('trophy'))) return true;
      return false;
    });

    if (filtered.length === 0) {
      grid.innerHTML = `<div class="col-span-full py-12 text-center text-slate-400 text-sm">No awards found in this category.</div>`;
      return;
    }

    grid.innerHTML = filtered.map(a => `
      <div class="achievement-card group bg-white rounded-2xl overflow-hidden border border-[#E6DFC9] hover:border-amber-400 hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
        <div class="relative h-64 bg-slate-100 overflow-hidden cursor-pointer lightbox-trigger" data-img-src="${escapeHtml(a.image)}" data-caption="${escapeHtml(a.title)}">
          <img src="${escapeHtml(a.image)}" alt="${escapeHtml(a.title)}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-500" onerror="this.src='assets/logo.png'" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end justify-between p-4 text-white">
            <span class="text-xs font-semibold flex items-center gap-1.5"><i data-lucide="zoom-in" class="w-4 h-4"></i> Click to Enlarge</span>
            <span class="text-[11px] bg-amber-500 text-slate-950 font-bold px-2 py-0.5 rounded">${escapeHtml(a.category || 'Award')}</span>
          </div>
        </div>
        <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="inline-flex items-center gap-1 text-[11px] font-bold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200">
                <i data-lucide="trophy" class="w-3 h-3 text-amber-600"></i> ${escapeHtml(a.category || 'Accolade')}
              </span>
              <span class="text-[11px] text-slate-400 font-medium">${escapeHtml(a.date || '2026')}</span>
            </div>
            <h3 class="font-serif text-base font-bold text-brand-navy group-hover:text-brand-blue transition leading-snug">
              ${escapeHtml(a.title)}
            </h3>
            <p class="text-xs text-slate-600 mt-1.5 line-clamp-2 leading-relaxed">
              ${escapeHtml(a.description || '')}
            </p>
          </div>
        </div>
      </div>
    `).join('');

    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active', 'bg-brand-navy', 'text-amber-300');
        b.classList.add('bg-white', 'text-slate-700');
      });
      btn.classList.add('active', 'bg-brand-navy', 'text-amber-300');
      btn.classList.remove('bg-white', 'text-slate-700');
      currentCategory = btn.dataset.achCat || 'all';
      render();
    });
  });

  loadAchievements();
})();
