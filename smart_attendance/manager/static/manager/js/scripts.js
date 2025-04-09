/**
 * Smart Attendance System - Manager App JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Mobile sidebar toggle
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(event) {
            if (sidebar.classList.contains('show') && 
                !sidebar.contains(event.target) &&
                !sidebarToggleBtn.contains(event.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-important)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Image preview functionality
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const previewId = this.getAttribute('data-preview') || 'imagePreviewElement';
                const containerId = this.getAttribute('data-container') || 'imagePreview';
                
                const previewElement = document.getElementById(previewId);
                const previewContainer = document.getElementById(containerId);
                
                if (previewElement && previewContainer) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewElement.src = e.target.result;
                        previewContainer.style.display = 'block';
                    };
                    reader.readAsDataURL(file);
                }
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Search functionality for tables
    const tableSearchInputs = document.querySelectorAll('.table-search');
    tableSearchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const tableId = this.getAttribute('data-table');
            filterManagerTable(this.value, tableId);
        });
    });
    
    // Select/Deselect All functionality for checkboxes
    const selectAllCheckboxes = document.querySelectorAll('.select-all-checkbox');
    selectAllCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const targetName = this.getAttribute('data-target');
            const targetCheckboxes = document.querySelectorAll(`input[name="${targetName}"]`);
            
            targetCheckboxes.forEach(targetCheckbox => {
                targetCheckbox.checked = this.checked;
            });
        });
    });
    
    // Password confirmation validation
    const passwordField = document.getElementById('id_password');
    const confirmPasswordField = document.getElementById('id_confirm_password');
    
    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (passwordField.value !== this.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Initialize any DataTables
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.datatable').DataTable({
            responsive: true,
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search...",
                paginate: {
                    previous: '<i class="fas fa-chevron-left"></i>',
                    next: '<i class="fas fa-chevron-right"></i>'
                }
            }
        });
    }
    
    // Initialize date pickers
    const datePickers = document.querySelectorAll('.datepicker');
    datePickers.forEach(picker => {
        if (typeof flatpickr !== 'undefined') {
            flatpickr(picker, {
                dateFormat: "Y-m-d"
            });
        }
    });
});

// Function to filter tables
function filterManagerTable(searchText, tableId) {
    const filter = searchText.toUpperCase();
    const table = document.getElementById(tableId);
    
    if (!table) return;
    
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip header
        let showRow = false;
        const cells = rows[i].getElementsByTagName('td');
        
        for (let j = 0; j < cells.length; j++) {
            const cellText = cells[j].textContent || cells[j].innerText;
            if (cellText.toUpperCase().indexOf(filter) > -1) {
                showRow = true;
                break;
            }
        }
        
        rows[i].style.display = showRow ? '' : 'none';
    }
}

// Function to toggle password visibility
function togglePasswordVisibility(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Function for action confirmation
function confirmAction(message, actionUrl) {
    if (confirm(message)) {
        window.location.href = actionUrl;
    }
}

// Function to handle bulk actions
function bulkAction(formId, actionType) {
    const form = document.getElementById(formId);
    
    if (!form) return;
    
    // Check if any item is selected
    const selectedItems = form.querySelectorAll('input[type="checkbox"]:checked');
    if (selectedItems.length === 0) {
        alert('Please select at least one item.');
        return;
    }
    
    // Set the action type
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action_type';
    actionInput.value = actionType;
    form.appendChild(actionInput);
    
    // Confirm and submit
    if (actionType === 'delete') {
        if (confirm('Are you sure you want to delete the selected items?')) {
            form.submit();
        }
    } else {
        form.submit();
    }
}
