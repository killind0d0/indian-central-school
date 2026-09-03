// Dynamic Faculty Loader - Indian Central School
(function () {
  const grid = document.getElementById('faculty-cards-grid');
  const countText = document.getElementById('faculty-count-text');
  const searchInput = document.getElementById('faculty-search-input');
  const filterBtns = document.querySelectorAll('.faculty-filter-btn');

  if (!grid) return;

  let allFaculty = [];
  let currentCategory = 'all';
  let currentQuery = '';

  async function loadFaculty() {
    try {
      const res = await fetch('data/faculty.json?_t=' + Date.now());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      allFaculty = await res.json();
      render();
    } catch (e) {
      console.warn('Could not load dynamic faculty.json:', e);
    }
  }

  function filterData() {
    return allFaculty.filter(f => {
      const matchesCat = (currentCategory === 'all') || (f.category === currentCategory);
      const text = `${f.name} ${f.subject} ${f.role} ${f.qualification}`.toLowerCase();
      const matchesSearch = !currentQuery || text.includes(currentQuery);
      return matchesCat && matchesSearch;
    });
  }

  function render() {
    const list = filterData();

    if (countText) {
      countText.textContent = `Showing ${list.length} Members`;
    }

    if (list.length === 0) {
      grid.innerHTML = `
        <div class="col-span-full py-16 text-center text-slate-500">
          <p class="font-serif text-lg text-brand-navy font-bold">No faculty members found</p>
          <p class="text-xs text-slate-400 mt-1">Try selecting another department or clearing your search.</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = list.map(f => `
      <div class="faculty-card group bg-white rounded-2xl p-5 border border-[#E6DFC9] hover:border-amber-400 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 flex flex-col justify-between" data-category="${f.category || 'senior'}" data-search="${escapeHtml(f.name + ' ' + f.subject + ' ' + f.role + ' ' + f.qualification).toLowerCase()}">
        <div>
          <div class="flex items-start gap-3.5 mb-3.5">
            <div class="w-13 h-13 sm:w-14 sm:h-14 rounded-xl overflow-hidden shrink-0 border border-[#E6DFC9] bg-gradient-to-br from-brand-navy to-brand-blue flex items-center justify-center text-amber-300 font-serif font-black text-lg shadow-inner group-hover:scale-105 transition relative">
              ${f.image ? `<img src="${escapeHtml(f.image)}" alt="${escapeHtml(f.name)}" class="w-full h-full object-cover hidden" onload="this.classList.remove('hidden');" onerror="this.remove();" />` : ''}
              <span>${escapeHtml(f.initials || f.name.substring(0, 2).toUpperCase())}</span>
            </div>
            <div class="min-w-0 flex-1 space-y-0.5">
              <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold border bg-emerald-50 text-emerald-800 border-emerald-200">
                <i data-lucide="book-open" class="w-2.5 h-2.5"></i> ${escapeHtml(f.subject || 'Faculty')}
              </span>
              <h3 class="font-serif text-[15px] sm:text-base font-bold text-brand-navy group-hover:text-brand-blue transition truncate">
                ${escapeHtml(f.name)}
              </h3>
              <p class="text-[11.5px] font-medium text-slate-600 line-clamp-1">
                ${escapeHtml(f.role || 'Teacher')}
              </p>
            </div>
          </div>
          <div class="border-t border-[#F0EAE1] pt-2.5 flex items-center justify-between text-[11px]">
            <span class="text-slate-400 font-medium">Qualification</span>
            <span class="font-semibold text-brand-navy text-right line-clamp-1" title="${escapeHtml(f.qualification || '')}">${escapeHtml(f.qualification || 'Certified')}</span>
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

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentQuery = e.target.value.toLowerCase().trim();
      render();
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active', 'bg-brand-navy', 'text-amber-300');
        b.classList.add('bg-white', 'text-slate-700');
      });
      btn.classList.add('active', 'bg-brand-navy', 'text-amber-300');
      btn.classList.remove('bg-white', 'text-slate-700');
      currentCategory = btn.dataset.category || 'all';
      render();
    });
  });

  loadFaculty();
})();
