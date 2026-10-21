import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AppHeader } from '../components/AppHeader';
import { Camera, CloudSun, BookOpen, Landmark, Info, ArrowRight, ShieldCheck, Sparkles, CheckCircle2 } from 'lucide-react';

export const HomeScreen: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader />

      {/* Hero Banner Section */}
      <section className="relative bg-gradient-to-br from-green-950 via-green-900 to-[#0F5A2B] text-white overflow-hidden py-12 lg:py-20 px-4 sm:px-6 lg:px-8">
        {/* Subtle background pattern */}
        <div className="absolute inset-0 opacity-15 mix-blend-overlay pointer-events-none">
          <img
            src="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1600&q=80"
            alt="Agricultural farmland"
            className="w-full h-full object-cover"
          />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left Content Column */}
            <div className="lg:col-span-7 space-y-5">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs font-semibold text-green-300 backdrop-blur-xs">
                <Sparkles className="w-3.5 h-3.5" />
                <span>{t('brand_line', 'Better Plants. Healthier Crops. Brighter Future')}</span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
                {t('welcome_title', 'Welcome to AI Plant Doctor')}
              </h1>

              <p className="text-base sm:text-lg text-green-100/90 max-w-2xl font-normal leading-relaxed">
                {t('welcome_sub', 'Detect plant diseases, get weather alerts, find expert advice and more.')}
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <button
                  onClick={() => navigate('/scan')}
                  className="bg-white text-[#1B7F3B] hover:bg-green-50 font-bold px-6 py-3.5 rounded-xl text-sm shadow-lg hover:shadow-xl transition-all flex items-center gap-2 group active:scale-95"
                >
                  <Camera className="w-4 h-4 text-[#1B7F3B]" />
                  <span>{t('scan_now', 'Scan a Plant Now')}</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </button>

                <button
                  onClick={() => navigate('/weather')}
                  className="bg-white/15 hover:bg-white/25 text-white font-semibold px-5 py-3.5 rounded-xl text-sm border border-white/25 backdrop-blur-xs transition-colors flex items-center gap-2"
                >
                  <CloudSun className="w-4 h-4" />
                  <span>{t('view_weather', 'Live Weather Forecast')}</span>
                </button>
              </div>

              {/* Feature Highlights */}
              <div className="pt-4 grid grid-cols-3 gap-3 text-xs text-green-200 border-t border-white/15 max-w-xl">
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-green-400 shrink-0" />
                  <span>Instant Plant ID</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-green-400 shrink-0" />
                  <span>Live Weather Risks</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-green-400 shrink-0" />
                  <span>Verified Schemes</span>
                </div>
              </div>
            </div>

            {/* Right Card / Visual Column */}
            <div className="lg:col-span-5 hidden lg:block">
              <div className="relative mx-auto max-w-md bg-white/10 backdrop-blur-md rounded-3xl p-4 border border-white/20 shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80"
                  alt="High quality plant scan preview"
                  className="rounded-2xl w-full h-72 object-cover shadow-inner"
                />
                <div className="mt-4 p-3 bg-white text-gray-900 rounded-2xl flex items-center justify-between shadow-md">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-[#1B7F3B]">
                      <ShieldCheck className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold">Smart Diagnostic Engine</h4>
                      <p className="text-[11px] text-gray-500">Early Blight, Powdery Mildew, Rust & more</p>
                    </div>
                  </div>
                  <span className="text-[11px] font-bold text-[#1B7F3B] bg-green-50 px-2.5 py-1 rounded-full border border-green-200">
                    92% Accuracy
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Feature Cards Section (Full-width grid) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full flex-1">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-gray-900">
              Agricultural Diagnostic & Decision Services
            </h2>
            <p className="text-xs sm:text-sm text-gray-500 mt-1">
              Select an automated tool below to inspect crop health, forecast localized hazards, and browse advisory records.
            </p>
          </div>
        </div>

        {/* 4 Feature Cards (Responsive 4-column layout on Desktop, 2-column on Tablet, 1 on Mobile) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* Card 1: Scan a Plant */}
          <div className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-green-300 transition-all group">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-[#EAF6EC] flex items-center justify-center text-[#1B7F3B] mb-3.5 group-hover:scale-110 transition-transform">
                <Camera className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-base text-gray-900">
                {t('scan_a_plant', 'Scan a Plant')}
              </h3>
              <p className="text-xs text-gray-500 mt-1.5 leading-relaxed">
                {t('scan_desc', 'Identify plants and detect diseases using AI')}
              </p>
            </div>
            <button
              onClick={() => navigate('/scan')}
              className="mt-5 w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white text-xs font-bold py-2.5 px-4 rounded-xl transition-all shadow-xs flex items-center justify-center gap-1.5"
            >
              <span>{t('scan_now', 'Scan Now')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Card 2: Weather Alerts */}
          <div className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-blue-300 transition-all group">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 mb-3.5 group-hover:scale-110 transition-transform">
                <CloudSun className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-base text-gray-900">
                {t('weather_alerts', 'Weather Alerts')}
              </h3>
              <p className="text-xs text-gray-500 mt-1.5 leading-relaxed">
                {t('weather_desc', 'Get local weather and crop risk alerts')}
              </p>
            </div>
            <button
              onClick={() => navigate('/weather')}
              className="mt-5 w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white text-xs font-bold py-2.5 px-4 rounded-xl transition-all shadow-xs flex items-center justify-center gap-1.5"
            >
              <span>{t('view_weather', 'View Weather')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Card 3: Plant Care & Advice */}
          <div className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-emerald-300 transition-all group">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 flex items-center justify-center text-emerald-700 mb-3.5 group-hover:scale-110 transition-transform">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-base text-gray-900">
                {t('plant_care_advice', 'Plant Care & Advice')}
              </h3>
              <p className="text-xs text-gray-500 mt-1.5 leading-relaxed">
                {t('care_desc', 'Learn about plant care, pests and diseases')}
              </p>
            </div>
            <button
              onClick={() => navigate('/care')}
              className="mt-5 w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white text-xs font-bold py-2.5 px-4 rounded-xl transition-all shadow-xs flex items-center justify-center gap-1.5"
            >
              <span>{t('get_advice', 'Get Advice')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Card 4: Government Schemes */}
          <div className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-amber-300 transition-all group">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center text-amber-600 mb-3.5 group-hover:scale-110 transition-transform">
                <Landmark className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-base text-gray-900">
                {t('government_schemes', 'Government Schemes')}
              </h3>
              <p className="text-xs text-gray-500 mt-1.5 leading-relaxed">
                {t('schemes_desc', 'Explore schemes and official links')}
              </p>
            </div>
            <button
              onClick={() => navigate('/schemes')}
              className="mt-5 w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white text-xs font-bold py-2.5 px-4 rounded-xl transition-all shadow-xs flex items-center justify-center gap-1.5"
            >
              <span>{t('view_schemes', 'View Schemes')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Advisory / Decision-Support Alert Banner */}
        <div className="mt-8 bg-blue-50/80 border border-blue-200/80 rounded-2xl p-4 flex items-start gap-3 shadow-xs">
          <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold text-blue-900">Decision Support Advisory</h4>
            <p className="text-xs text-blue-800 leading-relaxed mt-0.5">
              {t('home_disclaimer', 'Predictions may be less accurate on real field photos. This is decision support, not a replacement for experts.')}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};
