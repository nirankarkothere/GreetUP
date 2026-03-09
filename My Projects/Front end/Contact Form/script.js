    (function() {
      // DOM elements
      const form = document.getElementById('contactForm');
      const nameInput = document.getElementById('name');
      const emailInput = document.getElementById('email');
      const messageInput = document.getElementById('message');
      const submitBtn = document.getElementById('submitBtn');
      const btnText = document.getElementById('btnText');
      const btnIcon = document.getElementById('btnIcon');
      const resetBtn = document.getElementById('resetBtn');
      const successMsg = document.getElementById('successMessage');
      
      // Error message elements
      const nameError = document.getElementById('nameError');
      const emailError = document.getElementById('emailError');
      const messageError = document.getElementById('messageError');
      const charCounter = document.getElementById('charCounter');

      // Validation state
      let isValid = {
        name: false,
        email: false,
        message: false
      };

      // ===== VALIDATION FUNCTIONS =====
      
      // Validate name (not empty, at least 2 chars, letters only)
      function validateName(value) {
        const trimmed = value.trim();
        
        if (trimmed.length === 0) {
          nameError.innerHTML = '<i class="fas fa-exclamation-circle"></i> name is required';
          nameError.className = 'validation-message error';
          nameInput.classList.add('invalid');
          nameInput.classList.remove('valid');
          return false;
        }
        
        if (trimmed.length < 2) {
          nameError.innerHTML = '<i class="fas fa-exclamation-circle"></i> name must be at least 2 characters';
          nameError.className = 'validation-message error';
          nameInput.classList.add('invalid');
          nameInput.classList.remove('valid');
          return false;
        }
        
        if (!/^[a-zA-Z\s]+$/.test(trimmed)) {
          nameError.innerHTML = '<i class="fas fa-exclamation-circle"></i> only letters and spaces allowed';
          nameError.className = 'validation-message error';
          nameInput.classList.add('invalid');
          nameInput.classList.remove('valid');
          return false;
        }
        
        nameError.innerHTML = '<i class="fas fa-check-circle"></i> looks good!';
        nameError.className = 'validation-message success';
        nameInput.classList.add('valid');
        nameInput.classList.remove('invalid');
        return true;
      }

      // Validate email (format + not empty)
      function validateEmail(value) {
        const trimmed = value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (trimmed.length === 0) {
          emailError.innerHTML = '<i class="fas fa-exclamation-circle"></i> email is required';
          emailError.className = 'validation-message error';
          emailInput.classList.add('invalid');
          emailInput.classList.remove('valid');
          return false;
        }
        
        if (!emailRegex.test(trimmed)) {
          emailError.innerHTML = '<i class="fas fa-exclamation-circle"></i> please enter a valid email address';
          emailError.className = 'validation-message error';
          emailInput.classList.add('invalid');
          emailInput.classList.remove('valid');
          return false;
        }
        
        emailError.innerHTML = '<i class="fas fa-check-circle"></i> valid email format';
        emailError.className = 'validation-message success';
        emailInput.classList.add('valid');
        emailInput.classList.remove('invalid');
        return true;
      }

      // Validate message (not empty, min 10 chars, max 500)
      function validateMessage(value) {
        const trimmed = value.trim();
        const length = trimmed.length;
        
        // Update character counter
        charCounter.textContent = `${length}/500 characters`;
        
        if (length > 450) {
          charCounter.classList.add('warning');
        } else {
          charCounter.classList.remove('warning');
        }
        
        if (length > 480) {
          charCounter.classList.add('danger');
        } else {
          charCounter.classList.remove('danger');
        }
        
        if (length === 0) {
          messageError.innerHTML = '<i class="fas fa-exclamation-circle"></i> message cannot be empty';
          messageError.className = 'validation-message error';
          messageInput.classList.add('invalid');
          messageInput.classList.remove('valid');
          return false;
        }
        
        if (length < 10) {
          messageError.innerHTML = '<i class="fas fa-exclamation-circle"></i> message must be at least 10 characters';
          messageError.className = 'validation-message error';
          messageInput.classList.add('invalid');
          messageInput.classList.remove('valid');
          return false;
        }
        
        if (length > 500) {
          messageError.innerHTML = '<i class="fas fa-exclamation-circle"></i> message cannot exceed 500 characters';
          messageError.className = 'validation-message error';
          messageInput.classList.add('invalid');
          messageInput.classList.remove('valid');
          return false;
        }
        
        messageError.innerHTML = '<i class="fas fa-check-circle"></i> message length OK';
        messageError.className = 'validation-message success';
        messageInput.classList.add('valid');
        messageInput.classList.remove('invalid');
        return true;
      }

      // ===== EVENT LISTENERS =====
      
      // Real-time validation
      nameInput.addEventListener('input', function(e) {
        isValid.name = validateName(e.target.value);
        updateSubmitButton();
      });

      emailInput.addEventListener('input', function(e) {
        isValid.email = validateEmail(e.target.value);
        updateSubmitButton();
      });

      messageInput.addEventListener('input', function(e) {
        isValid.message = validateMessage(e.target.value);
        updateSubmitButton();
      });

      // Blur events (to validate empty fields when leaving)
      nameInput.addEventListener('blur', function(e) {
        validateName(e.target.value);
      });

      emailInput.addEventListener('blur', function(e) {
        validateEmail(e.target.value);
      });

      messageInput.addEventListener('blur', function(e) {
        validateMessage(e.target.value);
      });

      // Update submit button state
      function updateSubmitButton() {
        if (isValid.name && isValid.email && isValid.message) {
          submitBtn.disabled = false;
          submitBtn.style.opacity = '1';
        } else {
          submitBtn.disabled = true;
          submitBtn.style.opacity = '0.6';
        }
      }

      // Form submission
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Final validation
        isValid.name = validateName(nameInput.value);
        isValid.email = validateEmail(emailInput.value);
        isValid.message = validateMessage(messageInput.value);
        
        if (isValid.name && isValid.email && isValid.message) {
          // Show loading state
          btnText.textContent = 'sending...';
          btnIcon.innerHTML = '<span class="spinner"></span>';
          submitBtn.disabled = true;
          
          // Simulate API call (replace with actual fetch)
          setTimeout(() => {
            // Hide form, show success message
            form.style.display = 'none';
            successMsg.style.display = 'block';
            
            // Reset button state (for next time)
            btnText.textContent = 'send message';
            btnIcon.innerHTML = '<i class="fas fa-arrow-right"></i>';
            
            console.log('Form data:', {
              name: nameInput.value.trim(),
              email: emailInput.value.trim(),
              message: messageInput.value.trim()
            });
          }, 1500);
        }
      });

      // Reset form
      resetBtn.addEventListener('click', function() {
        // Clear inputs
        nameInput.value = '';
        emailInput.value = '';
        messageInput.value = '';
        
        // Reset validation states
        isValid = { name: false, email: false, message: false };
        
        // Remove validation classes
        [nameInput, emailInput, messageInput].forEach(input => {
          input.classList.remove('valid', 'invalid');
        });
        
        // Clear error messages
        nameError.innerHTML = '';
        emailError.innerHTML = '';
        messageError.innerHTML = '';
        
        // Reset character counter
        charCounter.textContent = '0/500 characters';
        charCounter.classList.remove('warning', 'danger');
        
        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.6';
        
        // If success message is showing, hide it and show form
        if (successMsg.style.display === 'block') {
          successMsg.style.display = 'none';
          form.style.display = 'block';
        }
      });

      // Initial state - disable submit button
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.6';
      
      // Optional: Add some demo data for testing
      // nameInput.value = 'John Doe';
      // emailInput.value = 'john@example.com';
      // messageInput.value = 'This is a test message';
      // validateName('John Doe');
      // validateEmail('john@example.com');
      // validateMessage('This is a test message');
    })();