let map;
let markers = {};

function initMap() {
    map = L.map('map').setView([-6.200000, 106.816666], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetchSellers();
}

function fetchSellers() {
    fetch('/get_sellers')
        .then(response => response.json())
        .then(sellers => {
            sellers.forEach(seller => {
                let marker = L.marker([seller.latitude, seller.longitude]).addTo(map);
                markers[seller.van_id] = marker;

                marker.on('click', () => {
                    fetch(`/get_seller_details?van_id=${seller.van_id}`)
                        .then(response => response.json())
                        .then(details => {
                            alert(`Shop Name: ${details.name}`);
                        });
                });
            });
        })
        .catch(error => console.error('Error fetching sellers:', error));
}

document.addEventListener('DOMContentLoaded', initMap);