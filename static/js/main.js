// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add loading state to form submission
    const planForm = document.querySelector('form[action="/generate_plan"]');
    if (planForm) {
        planForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Generating Plan...';
            submitButton.disabled = true;
        });
    }
    
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Parse markdown-like content in the plan
function formatPlanContent() {
    const planContainer = document.querySelector('.plan-container');
    if (planContainer) {
        let content = planContainer.innerHTML;
        
        // Convert headers
        content = content.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        content = content.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        content = content.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        
        // Convert bold
        content = content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Convert lists
        content = content.replace(/^\* (.+)$/gm, '<li>$1</li>');
        content = content.replace(/(<li>.+<\/li>\n)+/g, '<ul>$&</ul>');
        
        planContainer.innerHTML = content;
    }
}

// Call the formatter when the page loads
window.onload = function() {
    formatPlanContent();
};