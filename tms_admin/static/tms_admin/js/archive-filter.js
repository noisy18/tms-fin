document.addEventListener('DOMContentLoaded', function () {
    const filterType = document.getElementById('filterType');
    const dateFilter = document.querySelector('.date-filter');
    const carNumberFilter = document.querySelector('.car-number-filter');
    const completedStatusFilter = document.querySelector('.completed-status-filter'); // Новый фильтр
    const hiddenField = document.getElementById('filterValue');
    
    // Показываем соответствующий фильтр при загрузке страницы
    showActiveFilter();

    // Обработчик изменения значения в select
    filterType.addEventListener('change', function () {
        showActiveFilter();
    });

    // Обработчик отправки формы
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Отменяем стандартную отправку формы
        updateHiddenField(); // Устанавливаем значение скрытого поля
        this.submit(); // Отправляем форму вручную
    });

    function showActiveFilter() {
        switch(filterType.value) {
            case 'date':
                dateFilter.style.display = 'block';
                carNumberFilter.style.display = 'none';
                completedStatusFilter.style.display = 'none';
                break;
            case 'carNumber':
                carNumberFilter.style.display = 'block';
                dateFilter.style.display = 'none';
                completedStatusFilter.style.display = 'none';
                break;
            case 'completedStatus': // Обработка нового фильтра
                completedStatusFilter.style.display = 'block';
                dateFilter.style.display = 'none';
                carNumberFilter.style.display = 'none';
                break;
        }
    }

    function updateHiddenField() {
        switch(filterType.value) {
            case 'date':
                hiddenField.value = document.getElementById('dateInput').value;
                break;
            case 'carNumber':
                hiddenField.value = document.getElementById('carNumberInput').value;
                break;
            case 'completedStatus': // Обработка нового фильтра
                hiddenField.value = document.getElementById('completedStatusSelect').value;
                break;
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const completedTasksList = document.querySelector('.completed-tasks-list');
    const uncompletedTasksList = document.querySelector('.uncompleted-tasks-list');

    // Скрываем блоки, если они пустые
    if (completedTasksList.children.length === 0) {
        completedTasksList.style.display = 'none';
    } else {
        completedTasksList.style.display = 'block';
    }

    if (uncompletedTasksList.children.length === 0) {
        uncompletedTasksList.style.display = 'none';
    } else {
        uncompletedTasksList.style.display = 'block';
    }
});