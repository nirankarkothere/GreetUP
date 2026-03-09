    // unit toggle
    const unitBtns = document.querySelectorAll('.unit-btn');
    unitBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        unitBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // demo: update temperatures (just for show)
        const temps = document.querySelectorAll('.temp-value, .hour-temp, .temp-high, .temp-low, .city-temp');
        const isCelsius = this.textContent === '°C';
        
        temps.forEach(temp => {
          if (temp.classList.contains('temp-low')) return; // skip for demo
          
          const currentText = temp.textContent;
          const value = parseInt(currentText);
          if (!isNaN(value)) {
            if (isCelsius) {
              // convert from F to C (demo)
              temp.textContent = Math.round((value - 32) * 5/9) + '°';
            } else {
              // convert from C to F (demo)
              temp.textContent = Math.round((value * 9/5) + 32) + '°';
            }
          }
        });
      });
    });

    // search button
    const searchBtn = document.querySelector('.location-search button');
    searchBtn.addEventListener('click', () => {
      const input = document.querySelector('.location-search input');
      alert(`searching weather for: ${input.value}`);
    });

    // city cards click
    document.querySelectorAll('.city-card').forEach(card => {
      card.addEventListener('click', function() {
        const city = this.querySelector('h4').textContent;
        alert(`loading weather for: ${city}`);
      });
    });

    // enter key in search
    document.querySelector('.location-search input').addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        searchBtn.click();
      }
    });
