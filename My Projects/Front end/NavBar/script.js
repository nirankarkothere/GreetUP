    // Optional: Add scroll effect to header (enhancement)
    window.addEventListener('scroll', () => {
      const header = document.getElementById('header');
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });

    // Close mobile menu when clicking on a link (optional)
    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => {
        document.getElementById('nav-toggle').checked = false;
      });
    });

    // Active link highlighting based on current page (demo)
    const currentLocation = window.location.pathname;
    const menuLinks = document.querySelectorAll('.nav-menu a');
    menuLinks.forEach(link => {
      if (link.getAttribute('href') === '#') {
        // For demo, first link is active
        if (link.classList.contains('active')) return;
      }
    });