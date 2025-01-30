//images scrolling horizontally


        document.addEventListener("DOMContentLoaded", function () {
      const scrollImages = document.querySelector(".scroll-images");
      const scrollLength = scrollImages.scrollWidth - scrollImages.clientWidth;
      const leftButton = document.querySelector(".left");
      const rightButton = document.querySelector(".right");

      function checkScroll() {
        const currentScroll = scrollImages.scrollLeft;
        if (currentScroll === 0) {
          leftButton.setAttribute("disabled", "true");
          rightButton.removeAttribute("disabled");
        } else if (currentScroll === scrollLength) {
          rightButton.setAttribute("disabled", "true");
          leftButton.removeAttribute("disabled");
        } else {
          leftButton.removeAttribute("disabled");
          rightButton.removeAttribute("disabled");
        }
      }

      scrollImages.addEventListener("scroll", checkScroll);
      window.addEventListener("resize", checkScroll);
      checkScroll();

      function leftScroll() {
        scrollImages.scrollBy({
          left: -200,
          behavior: "smooth"
        });
      }

      function rightScroll() {
        scrollImages.scrollBy({
          left: 200,
          behavior: "smooth"
        });
      }

      leftButton.addEventListener("click", leftScroll);
      rightButton.addEventListener("click", rightScroll);
    });


// For side bar menu

       var sidmue = document.getElementById("sidemenue");

       function openmenue(){
        sidmue.style.right="0";
       }
       function closemenue(){
        sidmue.style.right="-150px";
       }



// For content in about us


    // Get all the accordion items
const accordionItems = document.querySelectorAll('.accordion-item');

// Add click event listener to each accordion title
accordionItems.forEach(item => {
  const title = item.querySelector('.accordion-title');
  const content = item.querySelector('.accordion-content');

  title.addEventListener('click', () => {
    // Toggle the active class on the clicked item
    item.classList.toggle('active');


  // Toggle the rotation of the arrow icon
  const arrowIcon = title.querySelector('.arrow-icon');
  arrowIcon.classList.toggle('rotate-up');


    // Toggle the display of the content
    if (content.style.display === 'block') {
      content.style.display = 'none';
    } else {
      // First, close all other accordion items
      accordionItems.forEach(otherItem => {
        if (otherItem !== item && otherItem.classList.contains('active')) {
          otherItem.classList.remove('active');
          otherItem.querySelector('.accordion-content').style.display = 'none';
          otherItem.querySelector('.arrow-icon').classList.remove('rotate-up');
        }
      });

      // Then, open the clicked item
      content.style.display = 'block';
    }
  });
});
