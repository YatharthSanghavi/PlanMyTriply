// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();
    
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
    
    // Initialize destination autocomplete
    initDestinationAutocomplete();
    
    // Add lazy loading for images
    lazyLoadImages();
    
    // Initialize smooth scroll for hash links
    initSmoothScroll();
});

// Theme Management
function initTheme() {
    // Create theme toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'theme-toggle';
    themeToggle.setAttribute('aria-label', 'Toggle dark mode');
    themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
    document.body.appendChild(themeToggle);
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    // Toggle theme on button click
    themeToggle.addEventListener('click', function() {
        let theme = document.documentElement.getAttribute('data-theme');
        let newTheme = theme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Add transition effect
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    });
}

function updateThemeIcon(theme) {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'light' 
            ? '<i class="bi bi-moon-fill"></i>' 
            : '<i class="bi bi-sun-fill"></i>';
    }
}

// Destination Autocomplete
function initDestinationAutocomplete() {
    const destinationInput = document.getElementById('destination');
    if (!destinationInput) return;
    
    let autocompleteContainer = document.createElement('div');
    autocompleteContainer.className = 'autocomplete-suggestions';
    autocompleteContainer.style.cssText = `
        position: absolute;
        background: var(--background);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-lg);
        max-height: 300px;
        overflow-y: auto;
        z-index: 1000;
        display: none;
        width: 100%;
    `;
    destinationInput.parentElement.style.position = 'relative';
    destinationInput.parentElement.appendChild(autocompleteContainer);
    
    let debounceTimer;
    destinationInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();
        
        if (query.length < 2) {
            autocompleteContainer.style.display = 'none';
            return;
        }
        
        debounceTimer = setTimeout(() => {
            fetchPopularDestinations(query, autocompleteContainer);
        }, 300);
    });
    
    // Close autocomplete when clicking outside
    document.addEventListener('click', function(e) {
        if (!destinationInput.contains(e.target)) {
            autocompleteContainer.style.display = 'none';
        }
    });
}

function fetchPopularDestinations(query, container) {
    fetch('/api/popular-destinations')
        .then(response => response.json())
        .then(destinations => {
            const filtered = destinations.filter(d => 
                d.name.toLowerCase().includes(query.toLowerCase())
            );
            
            if (filtered.length > 0) {
                container.innerHTML = filtered.map(dest => `
                    <div class="autocomplete-item" style="padding: 0.75rem; cursor: pointer; transition: background 0.2s;" 
                         onmouseover="this.style.background='var(--border)'" 
                         onmouseout="this.style.background='transparent'"
                         onclick="selectDestination('${dest.name}')">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 1.5rem;">${dest.icon}</span>
                            <div>
                                <div style="font-weight: 600; color: var(--text);">${dest.name}</div>
                                <div style="font-size: 0.75rem; color: var(--text-light);">
                                    ${dest.tags.join(' • ')}
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
                container.style.display = 'block';
            } else {
                container.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching destinations:', error);
        });
}

function selectDestination(destination) {
    const destinationInput = document.getElementById('destination');
    if (destinationInput) {
        destinationInput.value = destination;
        document.querySelector('.autocomplete-suggestions').style.display = 'none';
        
        // Show success feedback
        showToast('Destination selected!', 'success');
    }
}

// Toast Notifications
function showToast(message, type = 'success') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-check-circle me-2"></i>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Lazy Loading Images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src || img.src;
            img.classList.add('loaded');
        });
    }
}

// Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

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