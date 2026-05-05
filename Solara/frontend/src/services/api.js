import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:10000";
// const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const getSolarPrediction = async (lat, lon, device = "solar_car") => {
    try {
        const response = await axios.post(`${BASE_URL}/predict`, {
            lat: parseFloat(lat),
            lon: parseFloat(lon),
            device: device
        });
        return response.data;
    } catch (error) {
        console.error("Backend Error:", error);
        throw error;
    }
};

// OpenStreetMap Geocoding (Convert "Kolkata" to Lat/Lon)
export const searchLocation = async (query) => {
    try {
        const res = await axios.get(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`);
        if (res.data.length > 0) {
            return {
                lat: res.data[0].lat,
                lon: res.data[0].lon,
                display_name: res.data[0].display_name
            };
        }
        return null;
    } catch (e) { return null; }
};

