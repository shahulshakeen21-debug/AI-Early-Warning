import React, { useState } from 'react';
import { AppHeader } from '../components/AppHeader';
import { ChevronDown, ChevronUp, Leaf, AlertCircle, Shield, Sprout, Eye, Stethoscope, HelpCircle, Book } from 'lucide-react';

export const PlantCareScreen: React.FC = () => {
  const [selectedPlant, setSelectedPlant] = useState('Tomato');
  const [selectedDisease, setSelectedDisease] = useState('Early Blight');
  const [openSection, setOpenSection] = useState<string | null>('about');

  const toggleSection = (section: string) => {
    setOpenSection(openSection === section ? null : section);
  };

  const sections = [
    {
      id: 'about',
      title: 'About the Disease',
      icon: Leaf,
      content:
        'Early blight is a fungal disease caused by Alternaria solani. It affects tomato leaves, stems, and fruits, leading to premature defoliation and severe yield loss if untreated.',
    },
    {
      id: 'symptoms',
      title: 'Symptoms',
      icon: AlertCircle,
      content:
        'Small, circular brownish-black spots on older lower leaves that enlarge and exhibit concentric rings ("target board" appearance). Surrounding leaf tissue yellows before dropping.',
    },
    {
      id: 'prevention',
      title: 'Prevention Methods',
      icon: Shield,
      content:
        'Use certified disease-resistant seeds. Practice 3-year crop rotation with non-solanaceous crops. Space plants adequately for sufficient air movement and sun penetration.',
    },
    {
      id: 'cultural',
      title: 'Cultural Management',
      icon: Sprout,
      content:
        'Stake and prune indeterminate vines to elevate foliage from moist ground. Mulch beds with clean straw. Water exclusively at the base using drip irrigation.',
    },
    {
      id: 'monitoring',
      title: 'Monitoring Tips',
      icon: Eye,
      content:
        'Inspect the lower third of the crop canopy twice weekly, especially following warm rain or heavy morning dew.',
    },
    {
      id: 'treatment',
      title: 'Treatment Guidance',
      icon: Stethoscope,
      content:
        'Apply copper-based fungicides or neem extract (5ml/L) upon first symptom notice. For verified severe outbreaks, consult local extension office before synthetic spraying.',
    },
    {
      id: 'consult',
      title: 'When to Consult Expert',
      icon: HelpCircle,
      content:
        'Contact your block Agriculture Officer or Krishi Vigyan Kendra (KVK) if spots spread rapidly to upper foliage or fruit calyxes within 48 hours.',
    },
    {
      id: 'references',
      title: 'References',
      icon: Book,
      content:
        'Tamil Nadu Agricultural University (TNAU) Agritech Portal & Indian Council of Agricultural Research (ICAR) Disease Management Guidelines.',
    },
  ];

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">Plant Care & Agronomic Disease Management</h1>
            <p className="text-sm text-gray-500 mt-1">
              Comprehensive guidance on disease prevention, biological treatments, and cultural practices.
            </p>
          </div>

          {/* Plant & Disease Selectors */}
          <div className="flex items-center gap-3">
            <select
              value={selectedPlant}
              onChange={(e) => setSelectedPlant(e.target.value)}
              className="bg-white border border-gray-200 text-xs font-bold text-gray-800 rounded-xl px-4 py-2.5 focus:outline-none focus:border-[#1B7F3B]"
            >
              <option>Tomato</option>
              <option>Rice</option>
              <option>Mango</option>
              <option>Potato</option>
              <option>Banana</option>
            </select>

            <select
              value={selectedDisease}
              onChange={(e) => setSelectedDisease(e.target.value)}
              className="bg-white border border-gray-200 text-xs font-bold text-gray-800 rounded-xl px-4 py-2.5 focus:outline-none focus:border-[#1B7F3B]"
            >
              <option>Early Blight</option>
              <option>Late Blight</option>
              <option>Leaf Curl Virus</option>
              <option>Bacterial Wilt</option>
            </select>
          </div>
        </div>

        {/* 2-Column Grid for Accordions on Website */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sections.map((sec) => {
            const Icon = sec.icon;
            const isOpen = openSection === sec.id;
            return (
              <div
                key={sec.id}
                className="bg-white rounded-2xl border border-gray-100 shadow-xs overflow-hidden flex flex-col justify-start"
              >
                <button
                  type="button"
                  onClick={() => toggleSection(sec.id)}
                  className="w-full p-4 flex items-center justify-between text-left hover:bg-gray-50/70 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-green-50 flex items-center justify-center text-[#1B7F3B] shrink-0">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="font-bold text-sm text-gray-800">{sec.title}</span>
                  </div>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-gray-400" />
                  )}
                </button>

                {isOpen && (
                  <div className="px-5 pb-5 text-xs text-gray-600 leading-relaxed border-t border-gray-50 pt-3">
                    {sec.content}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Advisory Disclaimer Notice Box */}
        <div className="bg-emerald-50/80 border border-emerald-200/70 rounded-2xl p-4 flex items-start gap-3 mt-6">
          <Leaf className="w-5 h-5 text-[#1B7F3B] shrink-0 mt-0.5" />
          <p className="text-xs text-emerald-950 leading-relaxed">
            <strong>Advisory Note: </strong>This information is general agronomic guidance. Please consult your local block agriculture officer or Krishi Vigyan Kendra (KVK) for farm-specific prescriptions.
          </p>
        </div>
      </div>
    </div>
  );
};
