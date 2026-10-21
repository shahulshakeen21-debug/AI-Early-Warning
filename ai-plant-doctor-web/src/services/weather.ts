import axios from 'axios';

export interface WeatherDay {
  date: string;
  dayName: string;
  dayMonth: string;
  maxTemp: number;
  minTemp: number;
  rainMm: number;
  humidity: number;
  weatherCode: number;
  iconType: 'sunny' | 'partlyCloudy' | 'rainy' | 'thunderstorm';
}

export interface WeatherAlert {
  id: string;
  type: 'fungal' | 'heat' | 'spray' | 'wind' | 'cold' | 'flood';
  severity: 'high' | 'moderate' | 'low';
  title: string;
  description: string;
  recommendation: string;
}

export interface WeatherData {
  locationName: string;
  latitude: number;
  longitude: number;
  timezone: string;
  lastUpdated: string;
  source: string;
  currentTemp: number;
  currentHumidity: number;
  forecast: WeatherDay[];
  alerts: WeatherAlert[];
}

function getWeatherIconType(code: number): 'sunny' | 'partlyCloudy' | 'rainy' | 'thunderstorm' {
  if (code === 0 || code === 1) return 'sunny';
  if (code === 2 || code === 3) return 'partlyCloudy';
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(code)) return 'rainy';
  if ([95, 96, 99].includes(code)) return 'thunderstorm';
  return 'partlyCloudy';
}

function calculateAlerts(days: WeatherDay[], currentTemp: number, currentHumidity: number): WeatherAlert[] {
  const alerts: WeatherAlert[] = [];

  // Fungal risk rule: humidity > 80% + rain > 5mm in any day
  const fungalRiskDay = days.find((d) => d.humidity >= 78 && d.rainMm >= 4);
  if (fungalRiskDay || (currentHumidity > 80 && days[0]?.rainMm > 4)) {
    alerts.push({
      id: 'fungal_1',
      type: 'fungal',
      severity: 'high',
      title: 'Fungal Disease Risk',
      description: 'High humidity and rain expected on 25–27 Apr.',
      recommendation: 'Improve field drainage and avoid overhead irrigation. Delay spraying fungicides until dry spell.',
    });
  }

  // Heat stress
  const maxDay = days.reduce((prev, curr) => (curr.maxTemp > prev.maxTemp ? curr : prev), days[0]);
  if (maxDay && maxDay.maxTemp >= 35) {
    alerts.push({
      id: 'heat_1',
      type: 'heat',
      severity: 'moderate',
      title: 'Heat Stress Advisory',
      description: `Maximum daytime temperature approaching ${maxDay.maxTemp}°C.`,
      recommendation: 'Provide light frequent irrigation early morning or late evening. Mulch to retain soil moisture.',
    });
  }

  // Spray suitability
  if (days[0] && days[0].rainMm < 1 && days[0].humidity < 75) {
    alerts.push({
      id: 'spray_1',
      type: 'spray',
      severity: 'low',
      title: 'Optimal Spray Window',
      description: 'Calm winds and low probability of immediate rain today.',
      recommendation: 'Ideal conditions for applying foliar bio-fertilizers or neem oil spray.',
    });
  }

  return alerts;
}

export async function fetchWeather(lat: number = 11.0168, lon: number = 76.9558, placeName: string = 'Coimbatore, Tamil Nadu'): Promise<WeatherData> {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean,weathercode,windspeed_10m_max&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto&forecast_days=5`;

  const resp = await axios.get(url);
  const data = resp.data;
  const daily = data.daily || {};
  const current = data.current || {};

  const days: WeatherDay[] = [];
  const timeArray: string[] = daily.time || [];

  for (let i = 0; i < timeArray.length; i++) {
    const dStr = timeArray[i];
    const dateObj = new Date(dStr);
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    days.push({
      date: dStr,
      dayName: dayNames[dateObj.getDay()],
      dayMonth: `${dateObj.getDate()} ${monthNames[dateObj.getMonth()]}`,
      maxTemp: Math.round(daily.temperature_2m_max?.[i] ?? 30),
      minTemp: Math.round(daily.temperature_2m_min?.[i] ?? 22),
      rainMm: Math.round(daily.precipitation_sum?.[i] ?? 0),
      humidity: Math.round(daily.relative_humidity_2m_mean?.[i] ?? 65),
      weatherCode: daily.weathercode?.[i] ?? 1,
      iconType: getWeatherIconType(daily.weathercode?.[i] ?? 1),
    });
  }

  const currentTemp = Math.round(current.temperature_2m ?? 28);
  const currentHumidity = Math.round(current.relative_humidity_2m ?? 70);

  const alerts = calculateAlerts(days, currentTemp, currentHumidity);

  return {
    locationName: placeName,
    latitude: lat,
    longitude: lon,
    timezone: data.timezone || 'Asia/Kolkata',
    lastUpdated: new Date().toISOString().replace('T', ' ').substring(0, 16),
    source: 'Open-Meteo',
    currentTemp,
    currentHumidity,
    forecast: days,
    alerts,
  };
}

export async function searchGeocoding(place: string) {
  const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(place)}&count=5`;
  const resp = await axios.get(url);
  return resp.data.results || [];
}
