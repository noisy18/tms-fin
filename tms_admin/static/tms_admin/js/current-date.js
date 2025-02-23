// Функция для обновления текущего времени
function updateCurrentDate() {
    const currentDate = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('currentDateTime').innerText = currentDate.toLocaleString("ru-RU", options);
}

// Обновляем время каждые 1000 миллисекунд (1 секунда)
setInterval(updateCurrentDate, 1000);

// Сразу обновим при загрузке страницы
updateCurrentDate();