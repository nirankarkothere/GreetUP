    // Card data
    const cards = [
      { title: "ocean whispers", author: "alex chen", time: "2 days", price: 129, likes: 234, category: "nature", image: "img-1" },
      { title: "neon vortex", author: "samira khan", time: "5 hours", price: 89, likes: 567, category: "technology", image: "img-2" },
      { title: "forest floor", author: "marcus lee", time: "1 week", price: 149, likes: 128, category: "nature", image: "img-3" },
      { title: "sunset gradient", author: "tara wilson", time: "3 days", price: 79, likes: 892, category: "abstract", image: "img-4" },
      { title: "purple haze", author: "jordan p.", time: "8 hours", price: 199, likes: 421, category: "abstract", image: "img-5" },
      { title: "pixel dreams", author: "casey kim", time: "2 hours", price: 59, likes: 673, category: "technology", image: "img-6" },
      { title: "cherry bloom", author: "riley w.", time: "4 days", price: 109, likes: 345, category: "nature", image: "img-7" },
      { title: "tropical tide", author: "alex chen", time: "6 days", price: 139, likes: 234, category: "nature", image: "img-8" },
      { title: "ember glow", author: "tara wilson", time: "12 hours", price: 169, likes: 756, category: "abstract", image: "img-9" },
      { title: "midnight", author: "marcus lee", time: "1 day", price: 199, likes: 189, category: "minimal", image: "img-10" },
      { title: "mint frost", author: "samira khan", time: "3 hours", price: 89, likes: 432, category: "minimal", image: "img-11" },
      { title: "sunburst", author: "casey kim", time: "2 days", price: 119, likes: 621, category: "abstract", image: "img-12" }
    ];

    // DOM elements
    const grid = document.getElementById('dynamicGrid');
    const patternBtns = document.querySelectorAll('.pattern-btn');
    const chips = document.querySelectorAll('.chip');
    const viewBtns = document.querySelectorAll('.view-btn');
    const bps = document.querySelectorAll('.bp');

    // Render cards
    function renderCards(layout = 'standard', filter = 'all') {
      const filtered = filter === 'all' ? cards : cards.filter(c => c.category === filter);
      
      let html = '';
      filtered.forEach(card => {
        html += `
          <div class="grid-card" data-category="${card.category}">
            <div class="card-image ${card.image}">
              <span class="card-badge"><i class="far fa-heart"></i> ${card.likes}</span>
            </div>
            <div class="card-content">
              <h3 class="card-title">${card.title}</h3>
              <div class="card-meta">
                <span><i class="far fa-user"></i> ${card.author}</span>
                <span><i class="far fa-clock"></i> ${card.time}</span>
              </div>
              <p class="card-description">Beautiful gradient artwork with vibrant colors and smooth transitions.</p>
              <div class="card-footer">
                <span class="card-price">$${card.price}</span>
                <button class="card-btn"><i class="fas fa-arrow-right"></i></button>
              </div>
            </div>
          </div>
        `;
      });

      grid.innerHTML = html;
      grid.className = `card-grid grid-${layout}`;
    }

    // Update viewport info
    function updateViewport() {
      const width = window.innerWidth;
      document.getElementById('viewportWidth').textContent = width;
      
      let cols = 1;
      if (width >= 1280) cols = 4;
      else if (width >= 1024) cols = 3;
      else if (width >= 640) cols = 2;
      document.getElementById('colCount').textContent = cols;

      // Update breakpoint indicators
      bps.forEach(bp => {
        bp.classList.remove('active');
        if (width < 640 && bp.dataset.bp === 'mobile') bp.classList.add('active');
        else if (width >= 640 && width < 1024 && bp.dataset.bp === 'tablet') bp.classList.add('active');
        else if (width >= 1024 && width < 1280 && bp.dataset.bp === 'desktop') bp.classList.add('active');
        else if (width >= 1280 && bp.dataset.bp === 'wide') bp.classList.add('active');
      });
    }

    // Pattern button clicks
    patternBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        patternBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const layout = this.dataset.layout;
        const activeFilter = document.querySelector('.chip.active')?.dataset.filter || 'all';
        renderCards(layout, activeFilter);
      });
    });

    // Filter chips
    chips.forEach(chip => {
      chip.addEventListener('click', function() {
        chips.forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        
        const filter = this.dataset.filter;
        const activeLayout = document.querySelector('.pattern-btn.active')?.dataset.layout || 'standard';
        renderCards(activeLayout, filter);
      });
    });

    // View toggle (gap adjustment)
    viewBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        viewBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        if (this.id === 'gridView') grid.style.gap = '1.5rem';
        else if (this.id === 'listView') grid.style.gap = '1rem';
        else if (this.id === 'compactView') grid.style.gap = '0.8rem';
      });
    });

    // Initialize
    renderCards('standard', 'all');
    updateViewport();
    window.addEventListener('resize', updateViewport);
