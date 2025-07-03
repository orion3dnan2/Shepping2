            </main>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    <script>
        // Auto-hide alerts after 5 seconds
        document.addEventListener('DOMContentLoaded', function() {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(function(alert) {
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.style.opacity = '0';
                        setTimeout(function() {
                            if (alert.parentNode) {
                                alert.parentNode.removeChild(alert);
                            }
                        }, 300);
                    }
                }, 5000);
            });
        });
        
        // Confirm delete actions
        function confirmDelete(message = 'هل أنت متأكد من الحذف؟') {
            return confirm(message);
        }
        
        // Format currency input
        function formatCurrency(input) {
            let value = input.value.replace(/[^\d.]/g, '');
            if (value) {
                input.value = parseFloat(value).toFixed(3);
            }
        }
        
        // Copy to clipboard
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                showToast('تم النسخ بنجاح', 'success');
            });
        }
        
        // Show toast notification
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast show position-fixed top-0 end-0 m-3`;
            toast.innerHTML = `
                <div class="toast-header">
                    <strong class="me-auto">${type === 'success' ? 'نجح' : 'إشعار'}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">${message}</div>
            `;
            
            document.body.appendChild(toast);
            
            setTimeout(function() {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 3000);
        }
        
        // Print function
        function printElement(elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                const printWindow = window.open('', '_blank');
                printWindow.document.write(`
                    <html>
                    <head>
                        <title>طباعة</title>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
                        <style>
                            body { font-family: 'Tajawal', Arial, sans-serif; }
                            @media print {
                                .no-print { display: none !important; }
                            }
                        </style>
                    </head>
                    <body>
                        ${element.innerHTML}
                    </body>
                    </html>
                `);
                printWindow.document.close();
                printWindow.print();
            }
        }
        
        // Mobile sidebar toggle
        document.addEventListener('DOMContentLoaded', function() {
            const toggler = document.querySelector('.navbar-toggler');
            const sidebar = document.getElementById('sidebar');
            
            if (toggler && sidebar) {
                toggler.addEventListener('click', function() {
                    sidebar.classList.toggle('show');
                });
                
                // Close sidebar when clicking outside on mobile
                document.addEventListener('click', function(event) {
                    if (window.innerWidth <= 768) {
                        if (!sidebar.contains(event.target) && !toggler.contains(event.target)) {
                            sidebar.classList.remove('show');
                        }
                    }
                });
            }
        });
        
        // Real-time search
        function searchTable(inputId, tableId) {
            const input = document.getElementById(inputId);
            const table = document.getElementById(tableId);
            
            if (input && table) {
                input.addEventListener('keyup', function() {
                    const filter = this.value.toLowerCase();
                    const rows = table.getElementsByTagName('tr');
                    
                    for (let i = 1; i < rows.length; i++) {
                        const row = rows[i];
                        const text = row.textContent || row.innerText;
                        
                        if (text.toLowerCase().indexOf(filter) > -1) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    }
                });
            }
        }
        
        // Form validation
        function validateForm(formId) {
            const form = document.getElementById(formId);
            if (!form) return true;
            
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Email validation
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(function(field) {
                if (field.value && !isValidEmail(field.value)) {
                    field.classList.add('is-invalid');
                    isValid = false;
                }
            });
            
            return isValid;
        }
        
        function isValidEmail(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        }
        
        // Auto-calculate remaining amount
        function calculateRemaining(priceInput, paidInput, remainingInput) {
            const price = parseFloat(priceInput.value) || 0;
            const paid = parseFloat(paidInput.value) || 0;
            const remaining = Math.max(0, price - paid);
            remainingInput.value = remaining.toFixed(3);
        }
    </script>
    
    <!-- Page-specific scripts -->
    <?php if (isset($pageScripts)): ?>
        <?= $pageScripts ?>
    <?php endif; ?>
</body>
</html>