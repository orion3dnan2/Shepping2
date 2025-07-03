/**
 * Mobile navigation and responsive functionality
 */

// Mobile sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
    // Create mobile toggle button if it doesn't exist
    if (!document.querySelector('.mobile-toggle')) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'mobile-toggle btn btn-outline-light d-lg-none';
            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            toggleBtn.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 1050; display: none;';
            
            // Add toggle functionality
            toggleBtn.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
            
            document.body.appendChild(toggleBtn);
        }
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        const sidebar = document.querySelector('.sidebar');
        const toggleBtn = document.querySelector('.mobile-toggle');
        
        if (sidebar && sidebar.classList.contains('show') && 
            !sidebar.contains(e.target) && 
            !toggleBtn.contains(e.target)) {
            sidebar.classList.remove('show');
        }
    });
    
    // Responsive table enhancements
    enhanceResponsiveTables();
    
    // Auto-resize on window resize
    window.addEventListener('resize', function() {
        enhanceResponsiveTables();
    });
});

function enhanceResponsiveTables() {
    const tables = document.querySelectorAll('.unified-table');
    
    tables.forEach(table => {
        const container = table.closest('.unified-table-container');
        if (!container) return;
        
        // Add scroll indicator for mobile
        if (window.innerWidth <= 768) {
            if (!container.querySelector('.scroll-indicator')) {
                const indicator = document.createElement('div');
                indicator.className = 'scroll-indicator';
                indicator.innerHTML = '<small class="text-muted"><i class="fas fa-arrow-left"></i> اسحب لليسار لرؤية المزيد</small>';
                indicator.style.cssText = 'text-align: center; padding: 5px; font-size: 11px; background: #f8f9fa; border-radius: 0 0 8px 8px;';
                container.appendChild(indicator);
                
                // Hide indicator after scroll
                container.addEventListener('scroll', function() {
                    if (this.scrollLeft > 20) {
                        indicator.style.display = 'none';
                    }
                });
            }
        } else {
            // Remove indicator on larger screens
            const indicator = container.querySelector('.scroll-indicator');
            if (indicator) {
                indicator.remove();
            }
        }
    });
}

// Touch-friendly interactions for mobile
if ('ontouchstart' in window) {
    document.addEventListener('DOMContentLoaded', function() {
        // Add touch feedback to buttons
        const buttons = document.querySelectorAll('.btn-action, .btn');
        buttons.forEach(btn => {
            btn.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            btn.addEventListener('touchend', function() {
                this.style.transform = 'scale(1)';
            });
        });
    });
}

// Optimize form inputs for mobile
function optimizeMobileInputs() {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        // Add better mobile keyboard types
        if (input.type === 'text') {
            if (input.name && input.name.includes('phone')) {
                input.type = 'tel';
            } else if (input.name && input.name.includes('email')) {
                input.type = 'email';
            } else if (input.name && input.name.includes('weight')) {
                input.type = 'number';
                input.step = '0.1';
            }
        }
        
        // Prevent zoom on focus for iOS
        if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
            input.addEventListener('focus', function() {
                this.style.fontSize = '16px';
            });
            
            input.addEventListener('blur', function() {
                this.style.fontSize = '';
            });
        }
    });
}

// Initialize mobile optimizations
document.addEventListener('DOMContentLoaded', function() {
    optimizeMobileInputs();
});