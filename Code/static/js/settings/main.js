var socket = io.connect('http://' + document.domain + ':' + location.port);

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