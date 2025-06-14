// JavaScript for adding the highlight effect on scroll
window.addEventListener('scroll', () => {
    // Get all sections
    const sections = document.querySelectorAll('section');
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        
        if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
            section.classList.add('highlight'); // Add the highlight class
            
            // Optional: Remove the highlight after a brief delay (0.5s) to reset for the next section
            setTimeout(() => {
                section.classList.remove('highlight');
            }, 500); // 500ms to match the animation duration
        }
    });
});
