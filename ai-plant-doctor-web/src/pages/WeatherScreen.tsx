import React, { useState, useEffect } from 'react';
import { AppHeader } from '../components/AppHeader';
import { fetchWeather, searchGeocoding, WeatherData } from '../services/weather';
import { Search, MapPin, AlertTriangle, Sun, Cloud, CloudRain, Zap, RefreshCw, Wind, Droplets } from 'lucide-react';

export const WeatherScreen: React.FC = () => {
  const [query, setQuery] = useState('');
  const [latLongInput, setLatLongInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);

  const loadWeather = async (lat: number, lon: number, place: string) => {
    setLoading(true);
    try {
      const data = await fetchWeather(lat, lon, place);
      setWeatherData(data);
    } catch (err) {
      console.error('Weather load error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWeather(11.0168, 76.9558, 'Coimbatore, Tamil Nadu');
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (latLongInput.trim()) {
      const parts = latLongInput.split(',').map((p) => parseFloat(p.trim()));
      if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
        loadWeather(parts[0], parts[1], query.trim() || `${parts[0]}, ${parts[1]}`);
        return;
      }
    }

    if (!query.trim()) return;
    try {
      const results = await searchGeocoding(query);
      if (results && results.length > 0) {
        const top = results[0];
        const placeName = `${top.name}, ${top.admin1 || top.country}`;
        loadWeather(top.latitude, top.longitude, placeName);
      }
    } catch (err) {
      console.error('Geocoding error:', err);
    }
  };

  const handleAutoLocate = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          loadWeather(pos.coords.latitude, pos.coords.longitude, 'My Current Location');
        },
        (err) => {
          console.warn('Geolocation denied:', err);
        }
      );
    }
  };

  const renderWeatherIcon = (type: string) => {
    switch (type) {
      case 'sunny':
        return <Sun className="w-8 h-8 text-amber-500 mx-auto" />;
      case 'rainy':
        return <CloudRain className="w-8 h-8 text-blue-500 mx-auto" />;
      case 'thunderstorm':
        return <Zap className="w-8 h-8 text-purple-600 mx-auto" />;
      default:
        return <Cloud className="w-8 h-8 text-gray-400 mx-auto" />;
    }
  };

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">Agro-Meteorological Forecast & Crop Early Warning</h1>
            <p className="text-sm text-gray-500 mt-1">
              Live Open-Meteo multi-day forecasts with automated disease outbreak warnings for your farming zone.
            </p>
          </div>

          {/* Search Bar on desktop header */}
          <form onSubmit={handleSearch} className="flex items-center gap-2 max-w-md w-full">
            <div className="relative flex-1">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search district, city or village..."
                className="w-full bg-white border border-gray-200 text-xs text-gray-800 rounded-xl px-3.5 py-2.5 pr-9 focus:outline-none focus:border-[#1B7F3B]"
              />
              <button
                type="submit"
                className="absolute right-1 top-1 w-7 h-7 rounded-lg bg-[#1B7F3B] text-white flex items-center justify-center hover:bg-[#0F5A2B]"
              >
                <Search className="w-3.5 h-3.5" />
              </button>
            </div>
            <button
              type="button"
              onClick={handleAutoLocate}
              className="px-3 py-2.5 rounded-xl bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold flex items-center gap-1.5 shrink-0"
              title="Detect Current Location"
            >
              <MapPin className="w-3.5 h-3.5 text-[#1B7F3B]" />
              <span>GPS</span>
            </button>
          </form>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-gray-400">
            <RefreshCw className="w-8 h-8 animate-spin text-[#1B7F3B]" />
            <span className="text-sm font-semibold">Fetching meteorological feed from Open-Meteo API...</span>
          </div>
        ) : weatherData ? (
          <div className="space-y-6">
            {/* Location & Metadata Bar */}
            <div className="bg-white rounded-2xl p-4 shadow-xs border border-gray-100 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2 font-bold text-gray-900 text-sm">
                <MapPin className="w-4 h-4 text-[#1B7F3B]" />
                <span>Station: {weatherData.locationName}</span>
              </div>
              <div className="flex items-center gap-4 text-gray-500 text-[11px]">
                <span>Source: <strong className="text-gray-700">{weatherData.source}</strong></span>
                <span>•</span>
                <span>Updated: {weatherData.lastUpdated}</span>
                <span>•</span>
                <span>Timezone: {weatherData.timezone}</span>
              </div>
            </div>

            {/* 5-day Forecast Cards Grid (Responsive 5-column grid) */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              {weatherData.forecast.slice(0, 5).map((d, idx) => (
                <div
                  key={idx}
                  className="bg-white rounded-2xl p-4 text-center shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-md hover:border-green-200 transition-all"
                >
                  <div className="border-b border-gray-50 pb-2">
                    <span className="text-xs font-bold text-gray-900 block">
                      {d.dayMonth}
                    </span>
                    <span className="text-[10px] text-gray-400 uppercase font-semibold block">
                      {d.dayName}
                    </span>
                  </div>

                  <div className="my-3">{renderWeatherIcon(d.iconType)}</div>

                  <div className="space-y-1 text-xs">
                    <div className="font-extrabold text-base text-gray-900">{d.maxTemp}°C</div>
                    <div className="text-[11px] text-gray-400 font-medium">Night: {d.minTemp}°C</div>
                    <div className="text-[11px] text-blue-600 font-semibold flex items-center justify-center gap-1 mt-1">
                      <Droplets className="w-3 h-3" />
                      <span>{d.rainMm} mm</span>
                    </div>
                    <div className="text-[11px] text-gray-500">
                      Humidity: {d.humidity}%
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Crop Risk Alerts Section */}
            <div className="space-y-3">
              <h2 className="text-lg font-bold text-gray-900">Active Crop Hazard & Disease Risk Alerts</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {weatherData.alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className="bg-amber-50/90 border border-amber-200 rounded-2xl p-5 text-amber-950 shadow-xs flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 rounded-xl bg-amber-200/80 flex items-center justify-center text-amber-900 shrink-0">
                          <AlertTriangle className="w-4 h-4" />
                        </div>
                        <h3 className="font-bold text-sm text-amber-900">{alert.title}</h3>
                      </div>
                      <p className="text-xs font-medium leading-relaxed text-amber-900">
                        {alert.description}
                      </p>
                    </div>
                    <p className="text-xs text-amber-800 mt-3 pt-3 border-t border-amber-200/60 leading-relaxed">
                      <strong className="text-amber-950">Actionable Advisory: </strong>
                      {alert.recommendation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};
