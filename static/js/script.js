document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
        });
    });
});

function validateImageUpload(input) {
    const file = input.files[0];
    const maxSize = 16 * 1024 * 1024;
    
    if (file && file.size > maxSize) {
        alert('File size must be less than 16MB');
        input.value = '';
        return false;
    }
    
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    if (file && !allowedTypes.includes(file.type)) {
        alert('Only PNG, JPG, JPEG, and GIF files are allowed');
        input.value = '';
        return false;
    }
    
    return true;
}

const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
imageInputs.forEach(input => {
    input.addEventListener('change', function() {
        validateImageUpload(this);
    });
});
