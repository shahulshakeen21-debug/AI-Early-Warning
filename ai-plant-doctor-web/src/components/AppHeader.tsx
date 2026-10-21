import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAppStore } from '../store/useAppStore';
import { Sprout, ChevronLeft, ChevronDown, Home, Camera, CloudSun, Database, Landmark, History } from 'lucide-react';
import { useNavigate, NavLink } from 'react-router-dom';

interface AppHeaderProps {
  showBack?: boolean;
  backTo?: string;
  title?: string;
}

export const AppHeader: React.FC<AppHeaderProps> = ({ showBack = false, backTo = '/', title = 'AI Plant Doctor' }) => {
  const { t, i18n } = useTranslation();
  const { selectedLanguage, setSelectedLanguage } = useAppStore();
  const navigate = useNavigate();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLang = e.target.value as 'en' | 'ta';
    setSelectedLanguage(newLang);
    i18n.changeLanguage(newLang);
  };

  const navLinks = [
    { to: '/', label: t('tab_home', 'Home'), icon: Home },
    { to: '/scan', label: t('tab_scan', 'Scan Plant'), icon: Camera },
    { to: '/weather', label: t('tab_weather', 'Weather Alerts'), icon: CloudSun },
    { to: '/plants', label: t('tab_database', 'Plant Database'), icon: Database },
    { to: '/care', label: t('plant_care_advice', 'Plant Care'), icon: Sprout },
    { to: '/schemes', label: t('tab_schemes', 'Govt Schemes'), icon: Landmark },
    { to: '/history', label: t('tab_history', 'Scan History'), icon: History },
  ];

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-[#1B7F3B] via-[#146730] to-[#0F5A2B] text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Title */}
          <div className="flex items-center gap-3">
            {showBack && (
              <button
                onClick={() => navigate(backTo)}
                className="flex items-center gap-1.5 text-white/90 hover:text-white font-medium text-sm transition-colors mr-2 bg-white/10 hover:bg-white/20 px-2.5 py-1.5 rounded-lg"
                aria-label="Back"
              >
                <ChevronLeft className="w-4 h-4" />
                <span className="hidden sm:inline">Back</span>
              </button>
            )}

            <NavLink to="/" className="flex items-center gap-2.5 group">
              <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center p-1.5 shadow-xs group-hover:scale-105 transition-transform">
                <Sprout className="w-6 h-6 text-green-200" />
              </div>
              <div className="flex flex-col">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight leading-none">
                  AI Plant Doctor
                </span>
                <span className="text-[10px] text-green-200/90 font-medium tracking-wide mt-0.5 hidden sm:inline">
                  {selectedLanguage === 'ta' ? 'விவசாயிகளுக்கான AI முன் எச்சரிக்கை அமைப்பு' : 'Smart Plant ID & Farming Warning System'}
                </span>
              </div>
            </NavLink>
          </div>

          {/* Desktop Navigation Menu Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navLinks.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                      isActive
                        ? 'bg-white/25 text-white shadow-xs'
                        : 'text-white/80 hover:text-white hover:bg-white/10'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 opacity-90" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Right Actions: Language Switcher + Quick CTA */}
          <div className="flex items-center gap-3">
            <div className="relative inline-flex items-center">
              <select
                value={selectedLanguage}
                onChange={handleLanguageChange}
                className="appearance-none bg-white/15 hover:bg-white/20 text-white text-xs font-semibold px-3 py-2 pr-7 rounded-xl cursor-pointer border border-white/25 focus:outline-none focus:ring-2 focus:ring-white/40 shadow-xs transition-colors"
                aria-label="Select Language"
              >
                <option value="en" className="text-gray-900 bg-white">English (EN)</option>
                <option value="ta" className="text-gray-900 bg-white">தமிழ் (Tamil)</option>
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-white pointer-events-none absolute right-2.5" />
            </div>

            <button
              onClick={() => navigate('/scan')}
              className="hidden sm:flex items-center gap-1.5 bg-white text-[#1B7F3B] hover:bg-green-50 font-bold text-xs px-3.5 py-2 rounded-xl shadow-xs transition-transform active:scale-95"
            >
              <Camera className="w-3.5 h-3.5" />
              <span>Scan Now</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
