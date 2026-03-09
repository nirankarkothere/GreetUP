    // cart functionality
    const cartIcon = document.getElementById('cartIcon');
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    const closeCart = document.getElementById('closeCart');
    const cartCount = document.getElementById('cartCount');
    
    let cartItems = 3; // demo count
    
    function openCart() {
      cartSidebar.classList.add('open');
      cartOverlay.classList.add('open');
    }
    
    function closeCartSidebar() {
      cartSidebar.classList.remove('open');
      cartOverlay.classList.remove('open');
    }
    
    cartIcon.addEventListener('click', openCart);
    closeCart.addEventListener('click', closeCartSidebar);
    cartOverlay.addEventListener('click', closeCartSidebar);
    
    // add to cart function
    function addToCart(productName, price) {
      cartItems++;
      cartCount.textContent = cartItems;
      
      // show feedback
      alert(`${productName} added to cart! $${price}`);
      
      // demo: open cart after adding
      openCart();
    }
    
    // wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const icon = this.querySelector('i');
        if (icon.classList.contains('far')) {
          icon.classList.remove('far');
          icon.classList.add('fas');
          this.style.background = '#fee2e2';
          this.style.color = '#ef4444';
        } else {
          icon.classList.remove('fas');
          icon.classList.add('far');
          this.style.background = '';
          this.style.color = '';
        }
      });
    });
    
    // quick view
    document.querySelectorAll('.quick-view').forEach(view => {
      view.addEventListener('click', () => {
        alert('quick view - product details would appear here');
      });
    });
    
    // category tabs
    document.querySelectorAll('.category-tab').forEach(tab => {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
      });
    });
    
    // newsletter
    document.querySelector('.newsletter-form button').addEventListener('click', () => {
      const email = document.querySelector('.newsletter-form input').value;
      if (email) {
        alert(`subscribed with: ${email}`);
      } else {
        alert('please enter an email');
      }
    });
    
    // sort select
    document.querySelector('.sort-select').addEventListener('change', function() {
      alert(`sorting by: ${this.value}`);
    });
    
    // quantity buttons
    document.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const qtySpan = this.parentElement.querySelector('span');
        let qty = parseInt(qtySpan.textContent);
        
        if (this.textContent === '+') {
          qty++;
        } else if (this.textContent === '-' && qty > 1) {
          qty--;
        }
        
        qtySpan.textContent = qty;
      });
    });
