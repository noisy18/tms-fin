document.addEventListener('DOMContentLoaded', function() {
    const addTaskButton = document.querySelector('.add-task');
    const dropdown = document.getElementById('dropdownList');

    addTaskButton.addEventListener('click', function() {
        dropdown.classList.toggle('show');
    });

    // Закрыть выпадающий список, если кликнуть вне его
    window.onclick = function(event) {
        if (!event.target.matches('.add-task') && !dropdown.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    };
});