var socket = io.connect('http://' + document.domain + ':' + location.port);

// Обновление статуса бота //
document.addEventListener("DOMContentLoaded", onPageLoadForStatus);

function onPageLoadForStatus() { // Создаём цикл обновлений на каждые 5 секунд
    setInterval(statusBot, 5000);
    statusBot();
}

function statusBot() { // Функция запроса статуса
    socket.emit('requestBotStatus');
}

socket.on('getBotStatus', function(data) { // Обработка статуса
    var botStatusElement = document.getElementById("botStatus");

    if (data == true) {
        botStatusElement.textContent = "Онлаин";
        botStatusElement.classList.add('green');
        botStatusElement.classList.remove('red'); 
    } else {
        botStatusElement.textContent = "Оффлаин";
        botStatusElement.classList.add('red'); 
        botStatusElement.classList.remove('green');
    }
})

// Работа с токеном //
document.addEventListener("DOMContentLoaded", onPageLoadForToken);

function onPageLoadForToken() { // Загружаем токен из бинарника
    hasToken();
}

function sendToken() { // Отправка даты на обработку для кода
    var botToken = document.getElementById("botToken").value;
    socket.emit('sendToken', botToken);
}

function hasToken() { // Проверка есть ли токен
    socket.emit('isHasToken');
}

socket.on('getIsHasToken', function(data) {
    var botStatusElement = document.getElementById("botHasToken");

    if (data == true) {
        botStatusElement.textContent = "Существует";
        botStatusElement.classList.add('green');
        botStatusElement.classList.remove('red'); 
    } else {
        botStatusElement.textContent = "Не существует";
        botStatusElement.classList.add('red'); 
        botStatusElement.classList.remove('green');
    }
})

// Запуск бота //
function startBot() {
    socket.emit('startBot');
}

// Связь бота с пользователем //
socket.on('anserFromPy', function(data) { // Обновляем поле и говорим что хотели
    document.getElementById("anserFromPy").innerHTML = data;
});
