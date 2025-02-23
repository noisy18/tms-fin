document.addEventListener('DOMContentLoaded', function() {
    // Обработчик клика по кнопке для показа/скрытия календаря
    document.getElementById('calendar-button').addEventListener('click', function () {
        const calendarContainer = document.getElementById('calendar-container');
        if (calendarContainer.style.display === 'none') {
            calendarContainer.style.display = 'block';
            // Устанавливаем фокус на input после открытия календаря
            document.getElementById('date-picker').focus();
        } else {
            calendarContainer.style.display = 'none';
        }
    });
    
    // Обработчик изменения значения в input[type=date]
    document.getElementById('date-picker').addEventListener('change', function(event) {
        const selectedDate = event.target.value;
        // Если выбрана дата, меняем текст кнопки
        if (selectedDate) {
            document.getElementById('calendar-button').innerText = selectedDate;
        } else { // Если дата очищена, возвращаем исходный текст
            document.getElementById('calendar-button').innerText = 'Выбрать дату';
        }

        // Переходим на страницу с новой датой
        window.location.href = '?date=' + selectedDate;
    });
});