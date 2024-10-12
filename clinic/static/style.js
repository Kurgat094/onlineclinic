document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    dropdown.addEventListener('click', function () {
        dropdownContent.classList.toggle('show');
    });
    
    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', function (event) {
        if (!event.target.matches('.dropbtn')) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    });
});


