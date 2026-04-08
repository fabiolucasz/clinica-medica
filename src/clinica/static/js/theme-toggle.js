/**
 * Theme Toggle functionality for Light/Dark mode
 * Saves preference to localStorage
 */

(function() {
    'use strict';

    // Theme management
    const ThemeManager = {
        // Initialize
        init() {
            this.loadTheme();
            this.setupToggleButton();
            this.setupSystemPreferenceListener();
        },

        // Load saved theme or detect system preference
        loadTheme() {
            const savedTheme = localStorage.getItem('clinica-theme');
            
            if (savedTheme) {
                this.setTheme(savedTheme);
            } else {
                // Check system preference
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                this.setTheme(prefersDark ? 'dark' : 'light');
            }
        },

        // Set theme
        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('clinica-theme', theme);
            
            // Update toggle button icon
            this.updateToggleIcon(theme);
            
            // Dispatch custom event
            window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
        },

        // Toggle between light and dark
        toggle() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            this.setTheme(newTheme);
        },

        // Update toggle button icon
        updateToggleIcon(theme) {
            const toggleBtn = document.querySelector('.theme-toggle');
            if (toggleBtn) {
                const icon = toggleBtn.querySelector('.theme-toggle-icon');
                if (icon) {
                    if (theme === 'dark') {
                        icon.innerHTML = '🌙';
                        icon.style.transform = 'translateX(22px)';
                    } else {
                        icon.innerHTML = '☀️';
                        icon.style.transform = 'translateX(0)';
                    }
                }
            }
        },

        // Setup toggle button
        setupToggleButton() {
            // Create toggle button if it doesn't exist
            let toggleBtn = document.querySelector('.theme-toggle');
            
            if (!toggleBtn) {
                toggleBtn = this.createToggleButton();
                
                // Add to navbar
                const navbar = document.querySelector('.navbar-modern .navbar-nav, .navbar .navbar-nav, .navbar .container-fluid');
                if (navbar) {
                    const li = document.createElement('li');
                    li.className = 'nav-item d-flex align-items-center ms-3';
                    li.appendChild(toggleBtn);
                    navbar.appendChild(li);
                }
            }

            // Add click event
            toggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggle();
            });

            // Set initial icon
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            this.updateToggleIcon(currentTheme);
        },

        // Create toggle button element
        createToggleButton() {
            const button = document.createElement('button');
            button.className = 'theme-toggle';
            button.setAttribute('aria-label', 'Alternar tema claro/escuro');
            button.setAttribute('title', 'Alternar tema');
            
            const icon = document.createElement('span');
            icon.className = 'theme-toggle-icon';
            icon.innerHTML = '☀️';
            
            button.appendChild(icon);
            return button;
        },

        // Listen for system preference changes
        setupSystemPreferenceListener() {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                // Only auto-switch if user hasn't manually set a preference
                if (!localStorage.getItem('clinica-theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        },

        // Get current theme
        getCurrentTheme() {
            return document.documentElement.getAttribute('data-theme') || 'light';
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => ThemeManager.init());
    } else {
        ThemeManager.init();
    }

    // Expose to global scope for debugging
    window.ThemeManager = ThemeManager;

})();
