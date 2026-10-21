import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppHeader } from '../components/AppHeader';
import { useAppStore } from '../store/useAppStore';
import { ShieldAlert, CheckCircle, Trash2, Sprout, ShieldCheck, Check, ArrowRight, FileText } from 'lucide-react';
import { saveScanRecord } from '../services/storage';

export const DiseaseResultScreen: React.FC = () => {
  const navigate = useNavigate();
  const { currentScan } = useAppStore();
  const [savedId, setSavedId] = useState<string>('');

  const plantName = currentScan?.plantName || 'Tomato';
  const diseaseName = currentScan?.diseaseName || 'Early Blight';
  const scientificName = currentScan?.diseaseScientificName || 'Alternaria solani';
  const confidence = currentScan?.diseaseConfidence || 78;
  const isHealthy = currentScan?.isHealthy || false;
  const imageSrc =
    currentScan?.imageSrc ||
    'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80';

  const symptoms = currentScan?.symptoms || [
    'Dark brown spots with concentric rings ("target-board" lesions)',
    'Progressive chlorosis and yellowing of surrounding foliage',
    'Premature lower leaf defoliation in severe outbreaks',
  ];

  const actions = currentScan?.recommendedActions || [
    'Immediately prune and safely destroy infected lower leaves',
    'Ensure certified disease-free seed stock and resistant varieties',
    'Maintain adequate plant spacing (60 cm) for canopy aeration',
    'Apply copper oxychloride or biological neem oil at early stage',
  ];

  // Auto-save scan into IndexedDB on view
  useEffect(() => {
    const id = 'scan_' + Date.now();
    setSavedId(id);
    saveScanRecord({
      id,
      timestamp: new Date().toISOString(),
      plantName,
      plantScientificName: currentScan?.scientificName || 'Solanum lycopersicum',
      plantConfidence: currentScan?.plantConfidence || 92,
      diseaseName,
      diseaseScientificName: scientificName,
      diseaseConfidence: confidence,
      isHealthy,
      symptoms,
      recommendedActions: actions,
      imageThumbnail: imageSrc,
      weatherSnapshot: {
        location: 'Coimbatore, Tamil Nadu',
        temperature: 28,
        humidity: 70,
      },
    }).catch(console.error);
  }, []);

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/result/identify" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6">
          <span className="text-xs font-bold text-red-600 uppercase tracking-wider">
            Step 2 of 2: Pathological Diagnosis
          </span>
          <h1 className="text-2xl font-extrabold text-gray-900 mt-0.5">
            Crop Disease Detection Result
          </h1>
        </div>

        {/* 2-Column Responsive Layout for Website */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Specimen Image & Primary Diagnosis Card */}
          <div className="lg:col-span-6 space-y-5">
            <div className="h-80 rounded-2xl overflow-hidden bg-gray-100 shadow-sm border border-gray-100">
              <img
                src={imageSrc}
                alt="Examined crop specimen"
                className="w-full h-full object-cover"
              />
            </div>

            {/* Disease Detected / Healthy Status Banner */}
            {isHealthy ? (
              <div className="bg-[#1B7F3B] text-white rounded-2xl p-5 shadow-md flex items-center justify-between">
                <div className="flex items-center gap-3.5">
                  <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                    <CheckCircle className="w-6 h-6 text-green-200" />
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-green-200 tracking-wider uppercase">
                      Plant Health Status
                    </span>
                    <h2 className="text-xl font-extrabold leading-tight">Plant is Healthy</h2>
                    <p className="text-xs text-green-100">No active pathogens or leaf spots detected</p>
                  </div>
                </div>
                <div className="bg-white/20 text-white text-xs font-bold px-3.5 py-1.5 rounded-full border border-white/30">
                  Confidence: {confidence}%
                </div>
              </div>
            ) : (
              <div className="bg-[#DC2626] text-white rounded-2xl p-5 shadow-md flex items-center justify-between">
                <div className="flex items-center gap-3.5">
                  <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                    <ShieldAlert className="w-6 h-6 text-red-200" />
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-red-200 tracking-wider uppercase">
                      Pathogen Detected
                    </span>
                    <h2 className="text-xl font-extrabold leading-tight">{diseaseName}</h2>
                    <p className="text-xs text-red-100 italic">({scientificName})</p>
                  </div>
                </div>
                <div className="bg-white/20 text-white text-xs font-bold px-3.5 py-1.5 rounded-full border border-white/30">
                  Confidence: {confidence}%
                </div>
              </div>
            )}
          </div>

          {/* Right Column: Symptoms, Actions & Detailed Advice CTAs */}
          <div className="lg:col-span-6 space-y-5">
            {/* Symptoms Card */}
            <div className="bg-white rounded-2xl p-6 shadow-xs border border-gray-100 space-y-3">
              <h3 className="font-bold text-sm text-gray-900 flex items-center gap-2">
                <span>Diagnosed Clinical Symptoms</span>
              </h3>
              <ul className="space-y-2 text-xs text-gray-600">
                {symptoms.map((s, idx) => (
                  <li key={idx} className="flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 mt-1.5 shrink-0"></span>
                    <span className="leading-relaxed">{s}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommended Actions Card */}
            <div className="bg-white rounded-2xl p-6 shadow-xs border border-gray-100 space-y-3">
              <h3 className="font-bold text-sm text-gray-900 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-[#1B7F3B]" />
                <span>Recommended Action & Treatment Protocol</span>
              </h3>
              <div className="space-y-2.5 text-xs text-gray-700">
                {actions.map((act, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-2.5 rounded-xl bg-gray-50 border border-gray-100">
                    <div className="w-6 h-6 rounded-lg bg-green-100 flex items-center justify-center text-[#1B7F3B] shrink-0 font-bold">
                      <Check className="w-3.5 h-3.5" />
                    </div>
                    <span className="font-medium leading-relaxed">{act}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Action Buttons Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <button
                onClick={() => navigate('/care')}
                className="w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white font-bold py-3.5 px-4 rounded-xl text-xs transition-all shadow-md flex items-center justify-center gap-2 group cursor-pointer"
              >
                <span>View Detailed Care Advice</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={() => navigate(savedId ? `/report/${savedId}` : '/history')}
                className="w-full bg-white hover:bg-gray-50 text-gray-800 font-bold py-3.5 px-4 rounded-xl text-xs border border-gray-200 transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer"
              >
                <FileText className="w-4 h-4 text-[#1B7F3B]" />
                <span>Download Scan Report</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
