var socket = io.connect('http://' + document.domain + ':' + location.port);

// Функции загрузки данных
document.addEventListener("DOMContentLoaded", function() {
    checkTokenStatus();
    checkAutoStartStatus();
});

// Работа с токеном
function saveTokenSettings(event) {
    event.preventDefault();

    var botToken = document.getElementById("token").value;
    socket.emit('settingSetUpToken', botToken);
}

socket.on('settingTokenStatusPopup', function(data) {
    if (data) {
        showPopup('success', 'Настройка токена сохранена');
    } else {
        showPopup('error', 'Введён неверный токен бота');
    }
});

function checkTokenStatus() {
    socket.emit('settingCheckToken');
}

socket.on('settingTokenStatusUpdate', function(data) {
    if (data) {
        document.getElementById("tokenStatus").textContent = "Токен существует";
    } else {
        document.getElementById("tokenStatus").textContent = "Токен не существует";
    }
});

// Работа с автозапуском
function saveAutoStartSetting() {
    var autoStart = document.getElementById("autoStart").checked;
    socket.emit('settingSetUpAutoStart', autoStart);
}

socket.on('settingAutoStartStatusPopup', function(data) {
    if (data) {
        showPopup('success', 'Настройка автозапуска сохранена');
    } else {
        showPopup('error', 'Ошибка сохранения настройки автозапуска');
    }
});

function checkAutoStartStatus() {
    socket.emit('settingCheckAutoStart');
}

socket.on('settingAutoStartStatusUpdate', function(data) {
    document.getElementById("autoStart").checked = data;
});
