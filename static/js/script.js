document.addEventListener('DOMContentLoaded', () => {
    // Scroll animations using Intersection Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                entry.target.classList.add('appear');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Elements to observe for section reveal
    const hiddenElements = document.querySelectorAll('.hidden');
    hiddenElements.forEach(el => observer.observe(el));

    // Elements to observe for staggered fade-in animations
    const fadeInElements = document.querySelectorAll('.hero .fade-in');
    fadeInElements.forEach((el, index) => {
        // adding staggered delay based on index
        el.style.transitionDelay = `${index * 0.15}s`;
        // Trigger appear manually since they are above fold, or let observer do it
        setTimeout(() => {
             el.classList.add('appear');
        }, 100);
    });

    // Smooth scroll for Navigation links and CTA buttons
    document.querySelectorAll('.nav-links a, .cta-group a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;
            
            const targetSection = document.querySelector(targetId);
            if(targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Backend form submission
    const form = document.querySelector('.contact-form');
    if(form) {
        const statusEl = document.getElementById('contactStatus');

        if (statusEl) {
            const initialStatus = statusEl.dataset.status;
            if (initialStatus === 'success') {
                statusEl.style.color = '#10b981';
            } else if (initialStatus === 'error') {
                statusEl.style.color = '#ef4444';
            }
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('.submit-btn');
            const originalText = btn.textContent;

            if (statusEl) {
                statusEl.textContent = '';
                statusEl.style.color = 'var(--text-secondary)';
            }
            
            btn.textContent = 'Sending...';
            btn.style.opacity = '0.8';
            btn.style.pointerEvents = 'none';

            const payload = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value,
                website: document.getElementById('website') ? document.getElementById('website').value : ''
            };
            
            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    btn.textContent = 'Message Sent Successfully!';
                    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    btn.style.boxShadow = '0 10px 20px rgba(16, 185, 129, 0.2)';
                    btn.style.opacity = '1';
                    if (statusEl) {
                        statusEl.textContent = data.message || 'Your message has been sent.';
                        statusEl.style.color = '#10b981';
                    }
                    form.reset();
                } else {
                    btn.textContent = 'Error sending message';
                    btn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                    btn.style.opacity = '1';
                    if (statusEl) {
                        statusEl.textContent = (data && data.message) || 'Failed to send message.';
                        statusEl.style.color = '#ef4444';
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                btn.textContent = 'Error sending message';
                btn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                btn.style.opacity = '1';
                if (statusEl) {
                    statusEl.textContent = 'Network error. Please try again.';
                    statusEl.style.color = '#ef4444';
                }
            }
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = ''; 
                btn.style.boxShadow = '';
                btn.style.opacity = '1';
                btn.style.pointerEvents = 'auto';
            }, 3000);
        });
    }

    // Add navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if(window.scrollY > 50) {
            navbar.style.padding = '15px 5%';
            navbar.style.background = 'rgba(5, 5, 5, 0.85)';
            navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
        } else {
            navbar.style.padding = '20px 5%';
            navbar.style.background = 'rgba(5, 5, 5, 0.6)';
            navbar.style.boxShadow = 'none';
        }
    });
});
