// Enhanced Scroll Indicator
window.addEventListener("scroll", () => {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrollPercent = (scrollTop / scrollHeight) * 100;
  document.getElementById("scrollIndicator").style.width = scrollPercent + "%";
});

// Navigation and Section Management
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-link");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const id = entry.target.getAttribute("id");
    const navLink = document.querySelector(`.nav-link[href="#${id}"]`);

    if (entry.isIntersecting) {
      navLinks.forEach(link => link.classList.remove("active"));
      sections.forEach(sec => sec.classList.remove("active"));

      navLink.classList.add("active");
      entry.target.classList.add("active");

      // Create floating particles effect
      createParticles(entry.target);
    }
  });
}, {
  threshold: 0.6
});

sections.forEach(section => observer.observe(section));

navLinks.forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute("href"));
    target.scrollIntoView({ behavior: "smooth" });
  });
});

// Floating particles effect
function createParticles(section) {
  const particlesContainer = section.querySelector('.particles');
  if (!particlesContainer) return;

  // Clear existing particles
  particlesContainer.innerHTML = '';

  // Create new particles
  for (let i = 0; i < 15; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.width = Math.random() * 10 + 5 + 'px';
    particle.style.height = particle.style.width;
    particle.style.animationDelay = Math.random() * 6 + 's';
    particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
    particlesContainer.appendChild(particle);
  }
}

// Initialize particles for the active section
document.addEventListener('DOMContentLoaded', () => {
  createParticles(document.querySelector('section.active'));
});

// Add smooth hover effects to navigation
navLinks.forEach(link => {
  link.addEventListener('mouseenter', () => {
    link.style.transform = 'translateY(-3px) scale(1.05)';
  });
  
  link.addEventListener('mouseleave', () => {
    if (!link.classList.contains('active')) {
      link.style.transform = 'translateY(0) scale(1)';
    }
  });
});