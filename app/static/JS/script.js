// Fetch patient information from the server or database
const patientName = document.getElementById('patient-name');
const patientDob = document.getElementById('patient-dob');

// Simulating fetching patient information
patientName.textContent = 'John Doe';
patientDob.textContent = '01/01/1990';

// Add event listeners to navigation links
const navLinks = document.querySelectorAll('nav ul li a');
const sections = document.querySelectorAll('main section');

navLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    const targetSectionId = event.target.getAttribute('href').substring(1);
    showSection(targetSectionId);
  });
});

function showSection(sectionId) {
  sections.forEach(section => {
    section.style.display = 'none';
    section.classList.remove('animate__animated', 'animate__fadeIn', 'animate__fadeInUp');
  });

  const targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.style.display = 'block';
    targetSection.classList.add('animate__animated', 'animate__fadeIn');
    const contentElements = targetSection.querySelectorAll('h2, p, ul, table');
    contentElements.forEach((element, index) => {
      element.classList.add('animate__animated', 'animate__fadeInUp');
      element.style.animationDelay = `${(index + 1) * 0.1}s`;
    });
  }

  // Update active navigation link
  navLinks.forEach(link => {
    link.classList.remove('active');
  });
  const activeLink = document.querySelector(`nav ul li a[href="#${sectionId}"]`);
  if (activeLink) {
    activeLink.classList.add('active');
  }
}

// Show the patient summary section by default
showSection('patient-summary');