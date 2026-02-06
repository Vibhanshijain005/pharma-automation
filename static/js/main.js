/*
  ====== PHARMACY MANAGEMENT SYSTEM - INTERACTIVE FEATURES ======
  Modern animations, interactions, and UI enhancements
*/

document.addEventListener('DOMContentLoaded', function() {
  
  // ====== SMOOTH NAVIGATION LINKS ======
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('mouseenter', function() {
      this.style.paddingLeft = '25px';
    });
    link.addEventListener('mouseleave', function() {
      this.style.paddingLeft = '20px';
    });
  });

  // ====== TOOLTIP INITIALIZATION ======
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // ====== CARD HOVER ANIMATION ======
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px)';
      this.style.transition = 'all 0.3s ease';
    });
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // ====== TABLE ROW INTERACTIONS ======
  const tableRows = document.querySelectorAll('.table tbody tr');
  tableRows.forEach((row, index) => {
    row.style.animationDelay = `${index * 0.05}s`;
    row.addEventListener('mouseenter', function() {
      this.style.boxShadow = '0 2px 8px rgba(44, 120, 115, 0.15)';
      this.style.transition = 'all 0.3s ease';
    });
    row.addEventListener('mouseleave', function() {
      this.style.boxShadow = 'none';
    });
  });

  // ====== ALERT AUTO-DISMISS ======
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(function() {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // ====== BUTTON RIPPLE EFFECT ======
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // ====== FORM INPUT FOCUS EFFECTS ======
  const formInputs = document.querySelectorAll('.form-control, .form-select');
  formInputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.style.borderColor = '#2c7873';
      this.style.boxShadow = '0 0 0 0.2rem rgba(44, 120, 115, 0.25)';
      this.style.transform = 'scale(1.02)';
      this.style.transition = 'all 0.2s ease';
    });
    input.addEventListener('blur', function() {
      this.style.borderColor = '#e0d5c7';
      this.style.boxShadow = 'none';
      this.style.transform = 'scale(1)';
    });
  });

  // ====== SEARCH FUNCTIONALITY WITH ANIMATION ======
  const searchInput = document.querySelector('input[name="q"]');
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      this.parentElement.style.boxShadow = '0 4px 12px rgba(44, 120, 115, 0.2)';
    });
    searchInput.addEventListener('blur', function() {
      this.parentElement.style.boxShadow = 'none';
    });
  }

  // ====== DELETE CONFIRMATION WITH STYLE ======
  const deleteButtons = document.querySelectorAll('.btn-danger');
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      if (!confirm('Are you sure? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  // ====== QUANTITY INPUT HANDLER (FOR BILLING) ======
  const quantityInputs = document.querySelectorAll('.quantity-input');
  quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
      const qty = parseInt(this.value) || 0;
      const maxQty = parseInt(this.max) || 0;
      
      if (qty > maxQty) {
        this.value = maxQty;
        showNotification('Not enough inventory!', 'warning');
      }
    });
    
    input.addEventListener('input', function() {
      this.style.borderColor = this.value > 0 ? '#27ae60' : '#e74c3c';
    });
  });

  // ====== NOTIFICATION SYSTEM ======
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed`;
    notification.style.top = '80px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
      <i class="fas fa-info-circle me-2"></i>${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 4000);
  }
  // expose to global so templates can call it after load
  window.showNotification = showNotification;

  // ====== LOADING STATE FOR BUTTONS ======
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
      }
    });
  });

  // ====== DARK MODE TOGGLE (OPTIONAL) ======
  const darkModeBtn = document.getElementById('darkModeToggle');
  if (darkModeBtn) {
    darkModeBtn.addEventListener('click', function() {
      document.body.classList.toggle('dark');
      localStorage.setItem('darkMode', document.body.classList.contains('dark'));
    });
    
    // Load saved preference
    if (localStorage.getItem('darkMode') === 'true') {
      document.body.classList.add('dark');
    }
  }

  // ====== SCROLL ANIMATIONS ======
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all cards for scroll animation
  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
  });

  // ====== KEYBOARD SHORTCUTS ======
  document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K = Focus Search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault();
      searchInput?.focus();
    }
    
    // Escape = Close dropdowns
    if (event.key === 'Escape') {
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        menu.classList.remove('show');
      });
    }
  });

  // ====== RESPONSIVE TABLE BEHAVIOR ======
  const tables = document.querySelectorAll('.table');
  tables.forEach(table => {
    if (window.innerWidth < 768) {
      table.classList.add('table-sm');
    }
  });

  // ====== LIVE INVOICE CALCULATOR ======
  const invoiceTotal = document.getElementById('invoice-total');
  if (invoiceTotal) {
    const quantityFields = document.querySelectorAll('.quantity-input');
    quantityFields.forEach(field => {
      field.addEventListener('change', calculateTotal);
      field.addEventListener('input', calculateTotal);
    });
  }

  function calculateTotal() {
    let total = 0;
    document.querySelectorAll('.total-price').forEach(cell => {
      total += parseFloat(cell.textContent) || 0;
    });
    
    if (invoiceTotal) {
      invoiceTotal.textContent = total.toFixed(2);
      
      // Animate the change
      invoiceTotal.style.animation = 'none';
      setTimeout(() => {
        invoiceTotal.style.animation = 'pulse 0.5s ease';
      }, 0);
    }
  }

  // ====== ADD CSS ANIMATIONS ======
  if (!document.querySelector('style[data-animations]')) {
    const style = document.createElement('style');
    style.setAttribute('data-animations', 'true');
    style.innerHTML = `
      @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
      }

      @keyframes slideInUp {
        from {
          opacity: 0;
          transform: translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
      }

      @keyframes ripple-animation {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }

      /* Smooth transitions */
      * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
      }

      /* Text color utility for teal */
      .text-teal {
        color: #2c7873 !important;
      }

      /* Background color utility */
      .bg-teal {
        background-color: #2c7873 !important;
      }

      .bg-light-teal {
        background-color: #f0f8f7 !important;
      }
    `;
    document.head.appendChild(style);
  }

  console.log('✅ PharmaCare UI Initialized');
});

/* ====== UTILITY FUNCTIONS ====== */

// Format currency
function formatCurrency(value) {
  return new Intl.NumberFormat('en-PK', {
    style: 'currency',
    currency: 'PKR'
  }).format(value);
}

// Format date
function formatDate(date) {
  return new Date(date).toLocaleDateString('en-PK', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Dark mode toggle function
function toggleDarkMode() {
  document.body.classList.toggle('dark');
  localStorage.setItem('darkMode', document.body.classList.contains('dark'));
}
