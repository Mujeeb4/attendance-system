/**
 * Smart Attendance System - Attendance App JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Image preview functionality
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const previewElement = document.getElementById('imagePreviewElement');
                const previewContainer = document.getElementById('imagePreview');
                
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
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-important)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Attendance confirmation page - Select/Deselect All functionality
    const selectAllCheckbox = document.getElementById('select-all-students');
    if (selectAllCheckbox) {
        const studentCheckboxes = document.querySelectorAll('input[name="student_ids"]');
        
        selectAllCheckbox.addEventListener('change', function() {
            studentCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
        
        // Update "Select All" if all individual checkboxes are checked
        studentCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = [...studentCheckboxes].every(cb => cb.checked);
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = !allChecked && [...studentCheckboxes].some(cb => cb.checked);
            });
        });
    }
    
    // Attendance calendar initialization if calendar element exists
    const calendarEl = document.getElementById('calendar');
    if (calendarEl && typeof FullCalendar !== 'undefined') {
        // Calendar initialization is in the respective template
        // This is just a placeholder for additional calendar customization
        
        // Example: Add print button to calendar toolbar
        document.querySelector('.fc-toolbar-chunk:last-child')?.insertAdjacentHTML(
            'beforeend',
            '<button class="fc-button fc-button-primary ms-2" id="print-calendar"><i class="fas fa-print"></i></button>'
        );
        
        // Print calendar functionality
        document.getElementById('print-calendar')?.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Edit attendance page - Quick selection buttons
    const quickButtons = document.querySelectorAll('.quick-status-btn');
    quickButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const status = this.dataset.status;
            const selectElements = document.querySelectorAll('select[name^="status_"]');
            
            selectElements.forEach(select => {
                select.value = status;
            });
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
});

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

// Function for confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Search functionality for tables
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip header
        let showRow = false;
        const cells = rows[i].getElementsByTagName('td');
        
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    showRow = true;
                    break;
                }
            }
        }
        
        rows[i].style.display = showRow ? '' : 'none';
    }
}
