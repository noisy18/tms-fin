// Получение элементов
const modal = document.getElementById('myModal');
const openModalButton = document.getElementById('openDeleteModalButton');
const closeButton = document.querySelector('.close-button');
const modalBackground = document.createElement('div');
modalBackground.className = 'modal-background';

document.body.appendChild(modalBackground);

// Открытие модального окна
openModalButton.onclick = function() {
    modal.style.display = 'block';
    modalBackground.style.display = 'block';
};

// Закрытие модального окна
closeButton.onclick = function() {
    modal.style.display = 'none';
    modalBackground.style.display = 'none';
};

// Закрытие модального окна при клике вне его области
window.onclick = function(event) {
    if (event.target == modal || event.target == modalBackground) {
        modal.style.display = 'none';
        modalBackground.style.display = 'none';
    }
};