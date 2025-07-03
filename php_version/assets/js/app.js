/**
 * Main JavaScript for PHP Shipping Management System
 */

// Global variables
let currentLanguage = 'ar';

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize search functionality
    initializeSearch();
    
    // Initialize form validations
    initializeFormValidation();
    
    // Initialize print functionality
    initializePrintFunctions();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Initialize responsive tables
    initializeResponsiveTables();
}

// Search Functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    });
}

function performSearch(query) {
    if (query.trim() === '') {
        return;
    }
    
    // Show loading state
    showLoading();
    
    // Redirect to tracking page if it looks like a tracking number
    if (query.match(/^SHIP-\d{8}-\d{3}$/)) {
        window.location.href = `tracking.php?number=${encodeURIComponent(query)}`;
        return;
    }
    
    // Otherwise redirect to shipments page with search
    window.location.href = `shipments.php?search=${encodeURIComponent(query)}`;
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Find first invalid field and focus on it
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Print Functions
function initializePrintFunctions() {
    // Add print button event listeners
    document.querySelectorAll('.print-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            if (target) {
                printElement(target);
            }
        });
    });
}

function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error('Print element not found:', elementId);
        return;
    }
    
    const printWindow = window.open('', '_blank');
    const elementHtml = element.outerHTML;
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>طباعة</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Tajawal', Arial, sans-serif; margin: 20px; }
                .no-print { display: none !important; }
                @media print {
                    body { margin: 0; }
                    .container, .container-fluid { padding: 0; }
                }
            </style>
        </head>
        <body>
            ${elementHtml}
            <script>
                window.onload = function() {
                    window.print();
                    window.onafterprint = function() {
                        window.close();
                    };
                };
            </script>
        </body>
        </html>
    `);
    
    printWindow.document.close();
}

// Auto-hide alerts
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert.auto-hide');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Responsive Tables
function initializeResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive');
    
    tables.forEach(tableContainer => {
        const table = tableContainer.querySelector('table');
        if (table) {
            // Add scroll indicators for mobile
            if (window.innerWidth <= 768) {
                addScrollIndicators(tableContainer);
            }
        }
    });
}

function addScrollIndicators(container) {
    const indicator = document.createElement('div');
    indicator.className = 'table-scroll-indicator';
    indicator.innerHTML = '<i class="fas fa-arrow-left me-2"></i>مرر للجانب لرؤية المزيد';
    indicator.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 10;
        display: none;
    `;
    
    container.style.position = 'relative';
    container.appendChild(indicator);
    
    container.addEventListener('scroll', function() {
        if (this.scrollLeft > 10) {
            indicator.style.display = 'none';
        } else {
            indicator.style.display = 'block';
        }
    });
    
    // Show indicator initially
    setTimeout(() => {
        indicator.style.display = 'block';
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 3000);
    }, 1000);
}

// Loading States
function showLoading(element = null) {
    if (element) {
        element.innerHTML = '<div class="spinner-border spinner-border-sm me-2" role="status"></div>جاري التحميل...';
        element.disabled = true;
    } else {
        // Show global loading
        const loader = document.createElement('div');
        loader.id = 'globalLoader';
        loader.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
        loader.style.cssText = 'background: rgba(0,0,0,0.5); z-index: 9999;';
        loader.innerHTML = `
            <div class="bg-white p-4 rounded text-center">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <div>جاري التحميل...</div>
            </div>
        `;
        document.body.appendChild(loader);
    }
}

function hideLoading(element = null) {
    if (element) {
        element.disabled = false;
    } else {
        const loader = document.getElementById('globalLoader');
        if (loader) {
            loader.remove();
        }
    }
}

// Confirmation Dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Flash Messages
function showFlashMessage(type, message) {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show auto-hide`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Form Utilities
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
    }
}

function serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (data[key]) {
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

// Currency Formatting
function formatCurrency(amount) {
    const num = parseFloat(amount) || 0;
    return num.toFixed(3) + ' د.ك';
}

// Date Formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Number Formatting
function formatNumber(num, decimals = 3) {
    const number = parseFloat(num) || 0;
    return number.toFixed(decimals);
}

// URL Utilities
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function updateUrlParameter(key, value) {
    const url = new URL(window.location);
    url.searchParams.set(key, value);
    window.history.pushState({}, '', url);
}

// Local Storage Utilities
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

function loadFromStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Error loading from localStorage:', e);
        return null;
    }
}

// AJAX Utilities
function makeRequest(url, options = {}) {
    const defaults = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };
    
    const config = { ...defaults, ...options };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Request failed:', error);
            throw error;
        });
}

// Input Validation
function validateTrackingNumber(trackingNumber) {
    const pattern = /^SHIP-\d{8}-\d{3}$/;
    return pattern.test(trackingNumber);
}

function validateEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

function validatePhone(phone) {
    const pattern = /^[\+]?[0-9\s\-\(\)]{8,15}$/;
    return pattern.test(phone.replace(/\s/g, ''));
}

// Animation Utilities
function animateElement(element, animation = 'fadeIn') {
    element.classList.add('animate__animated', `animate__${animation}`);
    
    element.addEventListener('animationend', function() {
        element.classList.remove('animate__animated', `animate__${animation}`);
    }, { once: true });
}

// Copy to Clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showFlashMessage('success', 'تم نسخ النص بنجاح');
        }).catch(function(err) {
            console.error('Error copying text: ', err);
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showFlashMessage('success', 'تم نسخ النص بنجاح');
    } catch (err) {
        console.error('Fallback: Could not copy text: ', err);
        showFlashMessage('error', 'فشل في نسخ النص');
    }
    
    document.body.removeChild(textArea);
}

// Export Functions
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) {
        console.error('Table not found:', tableId);
        return;
    }
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            // Skip action columns
            if (cols[j].classList.contains('no-print') || cols[j].querySelector('.no-print')) {
                continue;
            }
            
            let cellText = cols[j].innerText.replace(/"/g, '""');
            row.push('"' + cellText + '"');
        }
        
        csv.push(row.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csvContent, filename) {
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Mobile Detection
function isMobile() {
    return window.innerWidth <= 768;
}

// Touch Support Detection
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Initialize touch-friendly features for mobile
if (isMobile() && isTouchDevice()) {
    document.addEventListener('DOMContentLoaded', function() {
        // Add touch-friendly classes
        document.body.classList.add('touch-device');
        
        // Increase button sizes on mobile
        const buttons = document.querySelectorAll('.btn-sm');
        buttons.forEach(btn => {
            btn.classList.remove('btn-sm');
            btn.classList.add('btn-touch');
        });
    });
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], .search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) {
                modal.hide();
            }
        }
    }
});

// Global Error Handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // You can add error reporting here if needed
});

// Service Worker Registration (if needed)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment if you want to add PWA support
        // navigator.serviceWorker.register('/sw.js');
    });
}