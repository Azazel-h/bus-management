document.addEventListener("DOMContentLoaded", function () {
        ymaps.ready(init);

        function init() {
            var map = new ymaps.Map("map", {
                center: [55.751574, 37.573856],
                zoom: 9
            });

            // Функция для создания предпросмотра маршрута
            function createRoutePreview() {
                // Получаем порядок станций из сервера
                fetch("/applications/list/")
                    .then(response => response.json())
                    .then(stations => {
                        var waypoints = [];
                        var visited = new Set();

                        stations.forEach(function (station) {
                            if (!visited.has(station.departure_id)) {
                                waypoints.push({id: station.departure_id, name: station.departure});
                                visited.add(station.departure_id);
                            }
                            if (!visited.has(station.arrival_id)) {
                                waypoints.push({id: station.arrival_id, name: station.arrival});
                                visited.add(station.arrival_id);
                            }
                        });

                        // Оптимизация порядка точек с использованием метода ветвей и границ
                        var coords = waypoints.map(function (waypoint) {
                            return ymaps.geocode(waypoint.name).then(function (res) {
                                var firstGeoObject = res.geoObjects.get(0);
                                return {
                                    id: waypoint.id,
                                    coordinates: firstGeoObject.geometry.getCoordinates(),
                                };
                            });
                        });

                        Promise.all(coords).then(function (points) {
                            var optimalRoute = solveTSPBranchAndBound(points);

                            // Создание маршрута на карте на основе оптимального порядка точек
                            var routePoints = optimalRoute.map(function (point) {
                                return point.coordinates;
                            });

                            ymaps.route(routePoints, {
                                multiRoute: true,
                                routingMode: 'driving'
                            }).then(function (route) {
                                route.options.set("mapStateAutoApply", true);
                                map.geoObjects.add(route);

                                var data = optimalRoute.map(function (point) {
                                    return point.id; // Возвращаем ID точек
                                });
                                var route_data;
                                // Получение данных о маршруте
                                route.getRoutes().each(function (route_part) {
                                    console.log('route data:', route_part.properties.getAll());
                                    route_data = route_part.properties.getAll();
                                });

                                // Сохраняем данные в глобальную переменную для использования при отправке формы
                                window.routeData = {
                                    waypoints: data,
                                    route_data: route_data,
                                    user_applications: stations,
                                };

                                // Вывод порядка точек в консоль
                                console.log("Оптимальный порядок точек для посещения:", optimalRoute.map(p => p.id));
                            }, function (err) {
                                console.log("Error:", err.message);
                            });
                        });
                    })
                    .catch(error => console.error('Ошибка при получении данных о станциях:', error));
            }

            // Вызываем функцию для создания предпросмотра маршрута при загрузке страницы
            createRoutePreview();

            // Обработчик события нажатия на кнопку создания маршрута
            document.getElementById('create-route-btn').addEventListener('click', function () {
                // Отправляем запрос на сервер только при нажатии на кнопку
                sendRouteRequest();
            });

            // Функция для отправки запроса на сервер
            function sendRouteRequest() {
                var formData = new FormData(document.querySelector("form"));

                // Добавление дополнительных параметров из сохраненной глобальной переменной
                formData.append('waypoints', JSON.stringify(window.routeData.waypoints));
                formData.append('route_data', JSON.stringify(window.routeData.route_data));
                formData.append('applications', JSON.stringify(window.routeData.user_applications));
                formData.append('driver', JSON.stringify(document.getElementById("id_driver").value));
                console.log(formData.get("waypoints"))
                fetch('/routes/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: formData
                })
                    .then(response => {
                        if (response.ok) {
                            location.reload();
                            console.log('Порядок точек сохранен на сервере.');
                        } else {
                            console.error('Ошибка при сохранении порядка точек на сервере.');
                        }
                    })
                    .catch(error => console.error('Ошибка при выполнении запроса:', error));
            }
        }

        // Функция для решения задачи коммивояжера методом ветвей и границ
        function solveTSPBranchAndBound(points) {
            var n = points.length;
            var minPath = [];
            var minDist = Infinity;
            var visited = Array(n).fill(false);
            var path = Array(n).fill(-1);
            var currentPath = Array(n).fill(-1);

            // Рекурсивная функция для нахождения оптимального маршрута
            function tsp(currPos, cost, level) {
                if (level === n && cost < minDist) {
                    minPath = currentPath.slice();
                    minDist = cost;
                    return;
                }

                for (var i = 0; i < n; i++) {
                    if (!visited[i]) {
                        visited[i] = true;
                        currentPath[level] = i;
                        tsp(i, cost + distanceBetweenPoints(points[currPos].coordinates, points[i].coordinates), level + 1);
                        visited[i] = false;
                    }
                }
            }

            // Находим нижнюю границу для оценки оптимальности маршрута
            var minBound = 0;
            for (var i = 0; i < n; i++) {
                var min1 = Infinity, min2 = Infinity;
                for (var j = 0; j < n; j++) {
                    if (i !== j) {
                        var dist = distanceBetweenPoints(points[i].coordinates, points[j].coordinates);
                        if (dist < min1) {
                            min2 = min1;
                            min1 = dist;
                        } else if (dist < min2 && dist !== min1) {
                            min2 = dist;
                        }
                    }
                }
                minBound += (min1 + min2);
            }
            minBound = Math.ceil(minBound / 2);

            // Начинаем с первой точки
            visited[0] = true;
            currentPath[0] = 0;

            // Начинаем поиск оптимального маршрута
            tsp(0, 0, 1);

            return minPath.map(function (index) {
                return points[index];
            });
        }

        // Вычисление расстояния между двумя точками
        function distanceBetweenPoints(point1, point2) {
            return ymaps.coordSystem.geo.getDistance(point1, point2);
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }
)
;
