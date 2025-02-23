// Выпадающий список
document.addEventListener('DOMContentLoaded', function() {
    const editEmployee = document.querySelector('.edit-employee-profile');
    const dropdown = document.getElementById('dropdownList');

    editEmployee.addEventListener('click', function() {
        dropdown.classList.toggle('show');
    });
});

// Появление и скрытие формы изменения профиля
document.addEventListener("DOMContentLoaded", function () {
    const showEditFormButton = document.getElementById("show-edit-form");
    const editForm = document.getElementById("edit-form");

    let isFormVisible = false;

    if (showEditFormButton) {
        showEditFormButton.addEventListener("click", function (event) {
            event.preventDefault();
            isFormVisible = !isFormVisible;
            editForm.style.display = isFormVisible ? "block" : "none";
        });
    }

    // Скрывать форму при клике вне формы
    window.onclick = function(event) {
        if (!editForm.contains(event.target) && !showEditFormButton.contains(event.target) && isFormVisible) {
            isFormVisible = false;
            editForm.style.display = "none";
        }
    };
});

// Появление и скрытие формы добавления сотрудника
document.addEventListener("DOMContentLoaded", function () {
    const showAddFormButton = document.getElementById("show-add-form");
    const addForm = document.getElementById("add-form");

    let isFormVisible = false;

    if (showAddFormButton) {
        showAddFormButton.addEventListener("click", function (event) {
            event.preventDefault();
            isFormVisible = !isFormVisible;
            addForm.style.display = isFormVisible ? "block" : "none";
        });
    }

    // Скрывать форму при клике вне формы
    document.addEventListener("click", function(event) {
        if (!addForm.contains(event.target) && !showAddFormButton.contains(event.target) && isFormVisible) {
            isFormVisible = false;
            addForm.style.display = "none";
        }
    });
});

// СКРИПТ для кнопок выбора роли сотрудника
// Получение контейнера с кнопками
const roleButtonsContainer = document.querySelector('.select-role');

// Выбор всех кнопок внутри контейнера
const buttons = roleButtonsContainer.querySelectorAll('button');

// Получение скрытого поля ввода
const hiddenInput = document.getElementById('selected_option');

// Обработчик нажатия на кнопку
buttons.forEach(button => {
    button.addEventListener('click', function() {
        // Снимаем класс 'selected' со всех кнопок
        buttons.forEach(btn => btn.classList.remove('selected'));

        // Добавляем класс 'selected' к активной кнопке
        this.classList.add('selected');

        // Заполняем скрытое поле выбранным значением
        hiddenInput.value = this.dataset.value;
    });
});