// Theme Management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.themeToggle = document.getElementById('themeToggle');
        this.init();
    }

    init() {
        this.applyTheme();
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        const icon = this.themeToggle.querySelector('.theme-icon');
        icon.textContent = this.theme === 'dark' ? '☀️' : '🌙';
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
    }
}

// Menu Management
class MenuManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.menuToggle = document.getElementById('menuToggle');
        this.isCollapsed = localStorage.getItem('menuCollapsed') === 'true';
        this.init();
    }

    init() {
        if (this.isCollapsed) {
            this.sidebar.classList.add('collapsed');
        }
        this.menuToggle.addEventListener('click', () => this.toggleMenu());
        
        // Mobile menu handling
        if (window.innerWidth <= 768) {
            this.sidebar.classList.remove('collapsed');
            this.menuToggle.addEventListener('click', () => this.toggleMobileMenu());
        }
    }

    toggleMenu() {
        this.isCollapsed = !this.isCollapsed;
        this.sidebar.classList.toggle('collapsed');
        localStorage.setItem('menuCollapsed', this.isCollapsed);
    }

    toggleMobileMenu() {
        this.sidebar.classList.toggle('open');
    }
}

// Resize Panel Management
class ResizeManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.resizeHandle = document.getElementById('resizeHandle');
        this.isResizing = false;
        this.startX = 0;
        this.startWidth = 0;
        this.minWidth = 200;
        this.maxWidth = 600;
        this.init();
    }

    init() {
        // Load saved width
        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth) {
            this.sidebar.style.width = savedWidth + 'px';
            document.documentElement.style.setProperty('--sidebar-width', savedWidth + 'px');
        }

        this.resizeHandle.addEventListener('mousedown', (e) => this.startResize(e));
        document.addEventListener('mousemove', (e) => this.resize(e));
        document.addEventListener('mouseup', () => this.stopResize());
    }

    startResize(e) {
        this.isResizing = true;
        this.startX = e.clientX;
        this.startWidth = this.sidebar.offsetWidth;
        this.resizeHandle.classList.add('resizing');
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    }

    resize(e) {
        if (!this.isResizing) return;

        const delta = e.clientX - this.startX;
        let newWidth = this.startWidth + delta;

        // Constrain width
        newWidth = Math.max(this.minWidth, Math.min(this.maxWidth, newWidth));

        this.sidebar.style.width = newWidth + 'px';
        document.documentElement.style.setProperty('--sidebar-width', newWidth + 'px');
    }

    stopResize() {
        if (!this.isResizing) return;

        this.isResizing = false;
        this.resizeHandle.classList.remove('resizing');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';

        // Save width
        const width = this.sidebar.offsetWidth;
        localStorage.setItem('sidebarWidth', width);
    }
}

// Smooth Scrolling for Anchor Links
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// Code Copy Button
class CodeCopyManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('pre code').forEach(block => {
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.textContent = 'Copy';
            button.addEventListener('click', () => this.copyCode(block, button));
            
            const pre = block.parentElement;
            pre.style.position = 'relative';
            pre.appendChild(button);
        });
    }

    async copyCode(block, button) {
        const code = block.textContent;
        try {
            await navigator.clipboard.writeText(code);
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
            button.textContent = 'Failed';
        }
    }
}

// Table of Contents Generator
class TOCGenerator {
    constructor() {
        this.init();
    }

    init() {
        const content = document.querySelector('.doc-body');
        if (!content) return;

        const headings = content.querySelectorAll('h2, h3');
        if (headings.length < 3) return; // Only show TOC if there are enough headings

        const toc = this.generateTOC(headings);
        if (toc) {
            content.insertBefore(toc, content.firstChild);
        }
    }

    generateTOC(headings) {
        const nav = document.createElement('nav');
        nav.className = 'table-of-contents';
        
        const title = document.createElement('h2');
        title.textContent = 'Table of Contents';
        nav.appendChild(title);

        const list = document.createElement('ul');
        
        headings.forEach((heading, index) => {
            // Add ID if not present
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }

            const li = document.createElement('li');
            li.className = `toc-${heading.tagName.toLowerCase()}`;
            
            const a = document.createElement('a');
            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;
            
            li.appendChild(a);
            list.appendChild(li);
        });

        nav.appendChild(list);
        return nav;
    }
}

// Initialize all managers when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new MenuManager();
    new ResizeManager();
    new SmoothScroll();
    new CodeCopyManager();
    new TOCGenerator();

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        const sidebar = document.getElementById('sidebar');
        const menuToggle = document.getElementById('menuToggle');
        
        if (window.innerWidth <= 768 && 
            !sidebar.contains(e.target) && 
            !menuToggle.contains(e.target) &&
            sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    });
});

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Reinitialize menu manager on resize
        if (window.innerWidth > 768) {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.remove('open');
        }
    }, 250);
});
