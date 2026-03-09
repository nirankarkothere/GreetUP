    // header scroll effect
    window.addEventListener('scroll', () => {
      const header = document.getElementById('header');
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });

    // back to top button
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    });

    backToTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // search functionality (demo)
    const searchInput = document.querySelector('.search-box input');
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        alert('searching for: ' + searchInput.value);
      }
    });

    // newsletter subscription
    const subscribeBtn = document.querySelector('.subscribe-btn');
    subscribeBtn.addEventListener('click', () => {
      const email = document.querySelector('.newsletter-form input').value;
      if (email) {
        subscribeBtn.innerHTML = '<i class="fas fa-check"></i> subscribed!';
        setTimeout(() => {
          subscribeBtn.innerHTML = '<i class="fas fa-paper-plane"></i> subscribe';
        }, 2000);
      }
    });

    // smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
