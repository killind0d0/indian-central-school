// Dynamic Notices Loader for Indian Central School
// Backed by Git-hosted data/notices.json
(function () {
  let allNotices = [];
  let currentCategory = 'all';

  // Badge styling helpers to match Tailwind design
  const categoryStyles = {
    olympiad: {
      badgeBg: 'bg-amber-50',
      badgeText: 'text-amber-800',
      badgeBorder: 'border-amber-200',
      icon: 'award',
      iconColor: 'text-amber-600',
      tagText: 'Olympiad',
      overlayBadgeBg: 'bg-amber-500 text-slate-950'
    },
    academic: {
      badgeBg: 'bg-blue-50',
      badgeText: 'text-blue-800',
      badgeBorder: 'border-blue-200',
      icon: 'calendar',
      iconColor: 'text-blue-600',
      tagText: 'Academic',
      overlayBadgeBg: 'bg-blue-600 text-white'
    },
    parents: {
      badgeBg: 'bg-emerald-50',
      badgeText: 'text-emerald-800',
      badgeBorder: 'border-emerald-200',
      icon: 'users',
      iconColor: 'text-emerald-600',
      tagText: 'Parent Advisory',
      overlayBadgeBg: 'bg-emerald-600 text-white'
    },
    press: {
      badgeBg: 'bg-purple-50',
      badgeText: 'text-purple-800',
      badgeBorder: 'border-purple-200',
      icon: 'newspaper',
      iconColor: 'text-purple-600',
      tagText: 'Media Press',
      overlayBadgeBg: 'bg-purple-600 text-white'
    },
    default: {
      badgeBg: 'bg-slate-50',
      badgeText: 'text-slate-800',
      badgeBorder: 'border-slate-200',
      icon: 'bell',
      iconColor: 'text-slate-600',
      tagText: 'Notice',
      overlayBadgeBg: 'bg-brand-navy text-amber-300'
    }
  };

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Load notices from data/notices.json
  async function fetchNotices() {
    try {
      const res = await fetch(`data/notices.json?_t=${Date.now()}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const data = await res.json();
      allNotices = Array.isArray(data) ? data : [];
    } catch (err) {
      console.warn('Failed to load local data/notices.json:', err);
      // Fallback: check localStorage cache
      const cached = localStorage.getItem('ics_cached_notices');
      if (cached) {
        try { allNotices = JSON.parse(cached); } catch (e) {}
      }
    }

    if (allNotices.length > 0) {
      localStorage.setItem('ics_cached_notices', JSON.stringify(allNotices));
    }

    renderNoticesPage();
    renderHomePageSpotlight();
  }

  // --------------------------------------------------------------------------
  // RENDER FOR notices.html
  // --------------------------------------------------------------------------
  function renderNoticesPage() {
    const grid = document.getElementById('notice-cards-grid');
    if (!grid) return; // not on notices.html

    updateFilterCounts();

    const filtered = currentCategory === 'all'
      ? allNotices
      : allNotices.filter(n => (n.category || '').toLowerCase() === currentCategory.toLowerCase());

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div class="col-span-full py-16 text-center bg-white rounded-2xl border border-[#E6DFC9] p-8">
          <i data-lucide="inbox" class="w-12 h-12 text-slate-300 mx-auto mb-3"></i>
          <h3 class="font-serif text-lg font-bold text-brand-navy">No Notices Found</h3>
          <p class="text-xs text-slate-500 mt-1">There are currently no circulars in this category.</p>
        </div>
      `;
      if (window.lucide) lucide.createIcons();
      return;
    }

    grid.innerHTML = filtered.map(item => {
      const cat = (item.category || 'default').toLowerCase();
      const style = categoryStyles[cat] || categoryStyles.default;
      const iconName = item.badgeIcon || style.icon;
      const badgeText = item.badge || style.tagText;
      const sessionText = item.session || item.date || 'Recent';

      return `
        <div class="notice-card group bg-white rounded-2xl overflow-hidden border border-[#E6DFC9] hover:border-amber-400 hover:shadow-xl transition-all duration-300 flex flex-col justify-between" data-notice-cat="${escapeHtml(cat)}">
          <div class="relative h-60 bg-slate-100 overflow-hidden cursor-pointer lightbox-trigger" data-img-src="${escapeHtml(item.image || 'assets/logo.png')}" data-caption="${escapeHtml(item.caption || item.title)}">
            <img src="${escapeHtml(item.image || 'assets/logo.png')}" alt="${escapeHtml(item.title)}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-500" onerror="this.src='assets/logo.png'" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end justify-between p-4 text-white">
              <span class="text-xs font-semibold flex items-center gap-1.5"><i data-lucide="zoom-in" class="w-4 h-4"></i> Click to Enlarge</span>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded ${style.overlayBadgeBg}">${escapeHtml(badgeText)}</span>
            </div>
            ${item.urgent ? '<div class="absolute top-3 left-3 bg-red-600 text-white text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded shadow">Urgent</div>' : ''}
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="inline-flex items-center gap-1 text-[11px] font-bold ${style.badgeText} ${style.badgeBg} px-2.5 py-0.5 rounded-full border ${style.badgeBorder}">
                  <i data-lucide="${escapeHtml(iconName)}" class="w-3 h-3 ${style.iconColor}"></i> ${escapeHtml(badgeText)}
                </span>
                <span class="text-[11px] text-slate-400 font-medium">${escapeHtml(sessionText)}</span>
              </div>
              <h3 class="font-serif text-base font-bold text-brand-navy group-hover:text-brand-blue transition leading-snug">
                ${escapeHtml(item.title)}
              </h3>
              <p class="text-xs text-slate-600 mt-1.5 line-clamp-2">
                ${escapeHtml(item.description || item.content || '')}
              </p>
            </div>
            <div class="border-t border-[#F0EAE1] pt-3 flex items-center justify-between">
              <button class="lightbox-trigger text-xs font-bold text-brand-navy hover:text-amber-600 flex items-center gap-1 transition" data-img-src="${escapeHtml(item.image || 'assets/logo.png')}" data-caption="${escapeHtml(item.caption || item.title)}">
                <i data-lucide="eye" class="w-3.5 h-3.5"></i> View Circular
              </button>
              <span class="text-[11px] text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded">Verified</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Re-bind lightbox triggers
    bindLightboxEvents();

    if (window.lucide) lucide.createIcons();
  }

  function updateFilterCounts() {
    const pills = document.querySelectorAll('.notice-pill');
    if (!pills || pills.length === 0) return;

    const counts = {
      all: allNotices.length,
      olympiad: allNotices.filter(n => (n.category || '').toLowerCase() === 'olympiad').length,
      academic: allNotices.filter(n => (n.category || '').toLowerCase() === 'academic').length,
      parents: allNotices.filter(n => (n.category || '').toLowerCase() === 'parents').length,
      press: allNotices.filter(n => (n.category || '').toLowerCase() === 'press').length
    };

    const labelMap = {
      all: `All Circulars (${counts.all})`,
      olympiad: `Indian Talent Olympiad (${counts.olympiad})`,
      academic: `Exams & Rules (${counts.academic})`,
      parents: `Parent Advisory (${counts.parents})`,
      press: `Media & Press (${counts.press})`
    };

    pills.forEach(pill => {
      const cat = pill.getAttribute('data-notice-cat');
      if (labelMap[cat]) {
        pill.textContent = labelMap[cat];
      }
    });
  }

  // --------------------------------------------------------------------------
  // RENDER FOR index.html (Homepage Spotlight)
  // --------------------------------------------------------------------------
  function renderHomePageSpotlight() {
    const container = document.getElementById('home-notices-spotlight');
    const viewAllLink = document.getElementById('home-notices-view-all');

    if (viewAllLink) {
      viewAllLink.innerHTML = `<span>View All ${allNotices.length} Circulars &amp; Press</span> <i data-lucide="arrow-right" class="w-4 h-4"></i>`;
    }

    if (!container) return; // not on homepage

    const topNotices = allNotices.slice(0, 3);

    container.innerHTML = topNotices.map(item => {
      const cat = (item.category || 'default').toLowerCase();
      const style = categoryStyles[cat] || categoryStyles.default;
      const badgeText = item.badge || style.tagText;

      return `
        <div class="group bg-white rounded-2xl overflow-hidden border border-[#E6DFC9] hover:border-amber-400 hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
          <div class="relative h-52 bg-slate-100 overflow-hidden cursor-pointer lightbox-trigger" data-img-src="${escapeHtml(item.image || 'assets/logo.png')}" data-caption="${escapeHtml(item.caption || item.title)}">
            <img src="${escapeHtml(item.image || 'assets/logo.png')}" alt="${escapeHtml(item.title)}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-500" onerror="this.src='assets/logo.png'" />
            <div class="absolute top-3 right-3 ${style.overlayBadgeBg} text-[10px] font-extrabold px-2 py-0.5 rounded shadow">
              ${item.urgent ? '🚨 Urgent' : 'Active'}
            </div>
          </div>
          <div class="p-4 space-y-2">
            <span class="text-[10px] font-extrabold uppercase ${style.badgeText} ${style.badgeBg} px-2 py-0.5 rounded">
              ${escapeHtml(badgeText)}
            </span>
            <h4 class="font-serif font-bold text-sm text-brand-navy group-hover:text-brand-blue transition">
              ${escapeHtml(item.title)}
            </h4>
            <p class="text-[11.5px] text-slate-500 line-clamp-2">
              ${escapeHtml(item.description || item.content || '')}
            </p>
            <div class="pt-2 border-t border-[#F0EAE1] flex items-center justify-between">
              <a href="notices.html" class="text-xs font-bold text-brand-navy hover:text-amber-600">Read Circular &rarr;</a>
              <span class="text-[11px] text-slate-400">${escapeHtml(item.session || item.date || 'Active')}</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    bindLightboxEvents();
    if (window.lucide) lucide.createIcons();
  }

  // --------------------------------------------------------------------------
  // Lightbox and Pill Event Handlers
  // --------------------------------------------------------------------------
  function bindLightboxEvents() {
    document.querySelectorAll('.lightbox-trigger').forEach(el => {
      // Remove old listeners to avoid duplicates
      el.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const src = el.getAttribute('data-img-src');
        const caption = el.getAttribute('data-caption');
        if (typeof window.openLightbox === 'function') {
          window.openLightbox(src, caption);
        }
      };
    });
  }

  function setupFilterPills() {
    const pills = document.querySelectorAll('.notice-pill');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => {
          p.classList.remove('active', 'bg-brand-navy', 'text-amber-300', 'border-brand-navy', 'shadow-xs');
          p.classList.add('bg-[#FAF8F5]', 'text-slate-700', 'border-[#E6DFC9]');
        });
        pill.classList.add('active', 'bg-brand-navy', 'text-amber-300', 'border-brand-navy', 'shadow-xs');
        pill.classList.remove('bg-[#FAF8F5]', 'text-slate-700', 'border-[#E6DFC9]');

        currentCategory = pill.getAttribute('data-notice-cat') || 'all';
        renderNoticesPage();
      });
    });
  }

  // Initial Boot
  document.addEventListener('DOMContentLoaded', () => {
    setupFilterPills();
    fetchNotices();
  });
})();
