    // grid view toggle
    const viewBtns = document.querySelectorAll('.view-btn');
    const productGrid = document.getElementById('productGrid');

    viewBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        viewBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const cols = this.dataset.grid;
        productGrid.className = `product-grid grid-${cols}`;
      });
    });

    // wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.toggle('active');
        const icon = this.querySelector('i');
        if (this.classList.contains('active')) {
          icon.className = 'fas fa-heart';
        } else {
          icon.className = 'far fa-heart';
        }
      });
    });

    // color selection
    document.querySelectorAll('.color-option').forEach(option => {
      option.addEventListener('click', function(e) {
        e.stopPropagation();
        const container = this.closest('.color-selector');
        container.querySelectorAll('.color-option').forEach(c => {
          c.classList.remove('selected');
        });
        this.classList.add('selected');
      });
    });

    // size selection
    document.querySelectorAll('.size-option').forEach(option => {
      option.addEventListener('click', function(e) {
        e.stopPropagation();
        const container = this.closest('.size-selector');
        container.querySelectorAll('.size-option').forEach(s => {
          s.classList.remove('selected');
        });
        this.classList.add('selected');
      });
    });

    // quantity adjuster
    window.adjustQty = function(btn, delta) {
      const container = btn.closest('.quantity-selector');
      const input = container.querySelector('.qty-input');
      let val = parseInt(input.value) + delta;
      if (val < 1) val = 1;
      if (val > 10) val = 10;
      input.value = val;
    };

    // add to cart animation
    document.querySelectorAll('.add-to-cart').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        if (this.disabled) return;
        
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="fas fa-check"></i> added!';
        this.style.background = '#10b981';
        
        setTimeout(() => {
          this.innerHTML = originalText;
          this.style.background = '';
        }, 1500);
      });
    });

    // quick view modal
    window.showQuickView = function(id) {
      document.getElementById('quickViewModal').classList.add('active');
    };

    window.closeModal = function() {
      document.getElementById('quickViewModal').classList.remove('active');
    };

    // filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        if (this.textContent.includes('all')) {
          document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          this.classList.add('active');
        } else {
          this.classList.toggle('active');
        }
      });
    });

    // close modal on overlay click
    document.getElementById('quickViewModal').addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });