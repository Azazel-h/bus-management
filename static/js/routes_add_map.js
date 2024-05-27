document.addEventListener("DOMContentLoaded", function () {
    ymaps.ready(init);

    function init() {
        var map = new ymaps.Map("map", {
            center: [55.751574, 37.573856],
            zoom: 9
        });

        // Обработчик события нажатия на кнопку создания маршрута
        document.getElementById('create-route-btn').addEventListener('click', function () {
            // Получаем порядок станций из сервера
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/booking/list/", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var stations = JSON.parse(xhr.responseText);
                    var waypoints = [];
                    stations.forEach(function (station) {
                        waypoints.push(station.departure, station.arrival);
                    });

                    ymaps.route({
                        // Задаем точки маршрута
                        referencePoints: waypoints,
                        // Оптимальный маршрут для автомобиля
                        routingMode: 'auto'
                    }).then(function (route) {
                        map.geoObjects.add(route);
                    }, function (error) {
                        console.log("Error:", error.message);
                    });
                }
            };
            xhr.send();
        });
    }
});
