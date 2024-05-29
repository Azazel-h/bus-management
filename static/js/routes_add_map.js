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
                    var visited = new Set();

                    stations.forEach(function (station) {
                        if (!visited.has(station.departure)) {
                            waypoints.push(station.departure);
                            visited.add(station.departure);
                        }
                        if (!visited.has(station.arrival)) {
                            waypoints.push(station.arrival);
                            visited.add(station.arrival);
                        }
                    });

                    // Создание мультимаршрута
                    ymaps.route(waypoints, {
                        multiRoute: true
                    }).done(function (route) {
                        route.options.set("mapStateAutoApply", true);
                        map.geoObjects.add(route);
                    }, function (err) {
                        console.log("Error:", err.message);
                    });
                } else if (xhr.readyState === 4) {
                    console.log("Error:", xhr.statusText);
                }
            };
            xhr.send();
        });
    }
});


