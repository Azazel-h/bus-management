document.addEventListener("DOMContentLoaded", function() {
    ymaps.ready(init);

    function init() {
        var map = new ymaps.Map("map", {
            center: [55.751574, 37.573856],
            zoom: 9
        });

        // Загрузка существующих станций
        fetch('/stations/list')
            .then(response => response.json())
            .then(data => {
                data.forEach(station => {
                    var placemark = new ymaps.Placemark([station.latitude, station.longitude], {
                        balloonContent: station.name
                    });
                    map.geoObjects.add(placemark);

                    // Добавление возможности удаления метки
                    placemark.events.add('contextmenu', function (e) {
                        e.preventDefault();
                        if (confirm('Вы уверены, что хотите удалить эту станцию?')) {
                            fetch(`/stations/${station.id}/delete`, {
                                method: 'DELETE',
                                headers: {
                                    'X-CSRFToken': getCookie('csrftoken')
                                }
                            }).then(response => {
                                if (response.ok) {
                                    map.geoObjects.remove(placemark);
                                }
                            });
                        }
                    });
                });
            });

        // Добавление новой станции
        map.events.add('click', function (e) {
            var coords = e.get('coords');

            // Получение адреса по координатам
            ymaps.geocode(coords).then(function (res) {
                var firstGeoObject = res.geoObjects.get(0);
                var address = firstGeoObject.getAddressLine();

                // Отправка данных на сервер
                fetch('/stations/create/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        name: address,
                        latitude: coords[0],
                        longitude: coords[1]
                    })
                })
                .then(response => response.json())
                .then(data => {
                    var placemark = new ymaps.Placemark([data.latitude, data.longitude], {
                        balloonContent: data.name
                    });
                    map.geoObjects.add(placemark);

                    // Добавление возможности удаления метки
                    placemark.events.add('contextmenu', function (e) {
                        e.preventDefault();
                        if (confirm('Вы уверены, что хотите удалить эту станцию?')) {
                            fetch(`/stations/${data.id}/delete`, {
                                method: 'DELETE',
                                headers: {
                                    'X-CSRFToken': getCookie('csrftoken')
                                }
                            }).then(response => {
                                if (response.ok) {
                                    map.geoObjects.remove(placemark);
                                }
                            });
                        }
                    });
                });
            });
        });
    }

    // Функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

