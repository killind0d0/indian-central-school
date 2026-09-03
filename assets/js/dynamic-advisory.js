// Dynamic Advisory Committee Loader - Indian Central School
(function () {
  const grid = document.getElementById('advisory-cards-grid');
  if (!grid) return;

  async function loadAdvisory() {
    try {
      const res = await fetch('data/advisory.json?_t=' + Date.now());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const list = await res.json();
      if (!Array.isArray(list) || list.length === 0) return;

      grid.innerHTML = list.map(a => `
        <div class="group bg-white rounded-2xl p-6 sm:p-7 border border-[#E6DFC9] hover:border-amber-400 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 relative flex flex-col justify-between">
          <div>
            <div class="flex items-start gap-4 mb-4">
              <div class="w-16 h-16 sm:w-18 sm:h-18 rounded-2xl overflow-hidden shrink-0 border border-[#E6DFC9] bg-gradient-to-br from-brand-navy to-brand-blue flex items-center justify-center text-amber-300 font-serif font-black text-xl shadow-inner group-hover:scale-105 transition relative">
                ${a.image ? `<img src="${escapeHtml(a.image)}" alt="${escapeHtml(a.name)}" class="w-full h-full object-cover hidden" onload="this.classList.remove('hidden');" onerror="this.remove();" />` : ''}
                <span>${escapeHtml(a.initials || a.name.substring(0, 2).toUpperCase())}</span>
              </div>
              <div class="space-y-1 min-w-0">
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10.5px] font-extrabold bg-purple-50 text-purple-900 border border-purple-200">
                  <i data-lucide="award" class="w-3 h-3 text-purple-700"></i> ${escapeHtml(a.badge || 'Advisory')}
                </span>
                <h3 class="font-serif text-lg sm:text-xl font-bold text-brand-navy group-hover:text-brand-blue transition truncate">
                  ${escapeHtml(a.name)}
                </h3>
                <p class="text-xs font-semibold text-slate-500">
                  ${escapeHtml(a.institution || '')}
                </p>
              </div>
            </div>
            <p class="text-xs sm:text-[13px] text-slate-600 leading-relaxed border-t border-[#F0EAE1] pt-3">
              ${escapeHtml(a.bio || '')}
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-dashed border-[#EFE8DC] flex items-center justify-between text-[11px] text-slate-500">
            <span class="font-semibold text-brand-navy">Role</span>
            <span class="text-slate-600 font-medium">${escapeHtml(a.role || 'Advisor')}</span>
          </div>
        </div>
      `).join('');

      if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
      }
    } catch (e) {
      console.warn('Could not load dynamic advisory.json:', e);
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  loadAdvisory();
})();
