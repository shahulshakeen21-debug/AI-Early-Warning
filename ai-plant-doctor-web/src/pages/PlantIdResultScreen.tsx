import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppHeader } from '../components/AppHeader';
import { useAppStore } from '../store/useAppStore';
import { Leaf, Info, ArrowRight, ShieldCheck, CheckCircle } from 'lucide-react';

export const PlantIdResultScreen: React.FC = () => {
  const navigate = useNavigate();
  const { currentScan } = useAppStore();

  const plantName = currentScan?.plantName || 'Tomato';
  const scientificName = currentScan?.scientificName || 'Solanum lycopersicum';
  const confidence = currentScan?.plantConfidence || 92;
  const imageSrc =
    currentScan?.imageSrc ||
    'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80';

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/scan" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6">
          <span className="text-xs font-bold text-[#1B7F3B] uppercase tracking-wider">
            Step 1 of 2: Botanical Identification
          </span>
          <h1 className="text-2xl font-extrabold text-gray-900 mt-0.5">
            Plant Identification Result
          </h1>
        </div>

        {/* 2-Column Responsive Layout for Website */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Leaf Imagery and Thumbnails */}
          <div className="lg:col-span-6 bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col gap-4">
            <div className="h-80 rounded-2xl overflow-hidden bg-gray-100 shadow-inner">
              <img
                src={imageSrc}
                alt={plantName}
                className="w-full h-full object-cover"
              />
            </div>

            {/* Reference Thumbnails */}
            <div>
              <p className="text-xs font-semibold text-gray-500 mb-2">
                Comparative Taxonomy Reference Matches:
              </p>
              <div className="grid grid-cols-3 gap-3">
                <div className="rounded-xl overflow-hidden bg-gray-100 border border-gray-200 aspect-video">
                  <img
                    src="https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=300&q=80"
                    alt="Ref 1"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="rounded-xl overflow-hidden bg-gray-100 border border-gray-200 aspect-video">
                  <img
                    src="https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=300&q=80"
                    alt="Ref 2"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="rounded-xl overflow-hidden bg-gray-100 border border-gray-200 aspect-video">
                  <img
                    src="https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=300&q=80"
                    alt="Ref 3"
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Identification Details & Disease Check Action */}
          <div className="lg:col-span-6 space-y-5">
            {/* Green "Plant Identified" Banner */}
            <div className="bg-[#1B7F3B] text-white rounded-2xl p-5 shadow-md flex items-center justify-between">
              <div className="flex items-center gap-3.5">
                <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                  <Leaf className="w-6 h-6 text-green-200" />
                </div>
                <div>
                  <span className="text-[11px] font-bold text-green-200 tracking-wider uppercase">
                    Plant Identified
                  </span>
                  <h2 className="text-xl font-extrabold leading-tight">{plantName}</h2>
                  <p className="text-xs text-green-100 italic">({scientificName})</p>
                </div>
              </div>
              <div className="bg-white/20 text-white text-xs font-bold px-3.5 py-1.5 rounded-full border border-white/30">
                Confidence: {confidence}%
              </div>
            </div>

            {/* About this plant Card */}
            <div className="bg-white rounded-2xl p-6 shadow-xs border border-gray-100 space-y-2">
              <h3 className="font-bold text-sm text-gray-900">About this plant</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                {plantName} is a widely cultivated crop of high nutritional and economic importance.
                It thrives in well-drained loamy soils with adequate moisture and sunlight, requiring proactive monitoring for fungal foliage blights during warm, humid weather.
              </p>
            </div>

            {/* Info notice box */}
            <div className="bg-blue-50/80 border border-blue-200/70 rounded-2xl p-4 flex items-start gap-3">
              <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
              <p className="text-xs text-blue-950 leading-relaxed">
                This plant is fully supported by our integrated disease identification model. You can now run the pathology check to evaluate symptoms, leaf spots, and get treatment protocols.
              </p>
            </div>

            {/* CTA: Check for Diseases */}
            <div className="pt-2">
              <button
                onClick={() => navigate('/result/disease')}
                className="w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white font-bold py-4 px-6 rounded-xl text-sm transition-all shadow-md flex items-center justify-center gap-2 group cursor-pointer"
              >
                <span>Proceed to Disease Detection</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
