// Simple initialization
document.addEventListener('DOMContentLoaded', function() {
    
    // Add smooth scrolling for any anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-6px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click effects for CTA buttons
    const ctaButtons = document.querySelectorAll('.cta-button, .learn-more-btn');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            console.log('Button clicked:', this.textContent);
        });
    });
    
    // Simple number counting animation for statistics
    const stats = document.querySelectorAll('.percentage');
    
    const animateCounter = (element, target) => {
        const increment = target / 50;
        let current = 0;
        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.ceil(current) + '%';
            if (current >= target) {
                clearInterval(timer);
                element.textContent = target + '%';
            }
        }, 30);
    };
    
    // Observer for stats animation
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.textContent);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, { threshold: 0.3 });
    
    stats.forEach(stat => {
        observer.observe(stat);
    });
    
});

// Simple loading state
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});