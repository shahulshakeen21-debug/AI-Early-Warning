import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { HomeScreen } from './pages/HomeScreen';
import { ScanScreen } from './pages/ScanScreen';
import { PlantIdResultScreen } from './pages/PlantIdResultScreen';
import { DiseaseResultScreen } from './pages/DiseaseResultScreen';
import { WeatherScreen } from './pages/WeatherScreen';
import { PlantDatabaseScreen } from './pages/PlantDatabaseScreen';
import { PlantCareScreen } from './pages/PlantCareScreen';
import { GovernmentSchemesScreen } from './pages/GovernmentSchemesScreen';
import { ScanHistoryScreen } from './pages/ScanHistoryScreen';
import { ReportDownloadScreen } from './pages/ReportDownloadScreen';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/scan" element={<ScanScreen />} />
          <Route path="/result/identify" element={<PlantIdResultScreen />} />
          <Route path="/result/disease" element={<DiseaseResultScreen />} />
          <Route path="/weather" element={<WeatherScreen />} />
          <Route path="/plants" element={<PlantDatabaseScreen />} />
          <Route path="/care" element={<PlantCareScreen />} />
          <Route path="/schemes" element={<GovernmentSchemesScreen />} />
          <Route path="/history" element={<ScanHistoryScreen />} />
          <Route path="/report/:id" element={<ReportDownloadScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
