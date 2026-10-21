import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Camera, CloudSun, Database, Landmark, History, MoreHorizontal } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export const BottomNav: React.FC = () => {
  const { t } = useTranslation();

  const navItems = [
    { to: '/', label: t('tab_home', 'Home'), icon: Home },
    { to: '/scan', label: t('tab_scan', 'Scan'), icon: Camera },
    { to: '/weather', label: t('tab_weather', 'Weather'), icon: CloudSun },
    { to: '/plants', label: t('tab_database', 'Database'), icon: Database },
    { to: '/schemes', label: t('tab_schemes', 'Schemes'), icon: Landmark },
    { to: '/history', label: t('tab_history', 'History'), icon: History },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-gray-200 z-40 py-1.5 px-2 shadow-lg">
      <div className="flex justify-around items-center">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center py-1 px-1.5 rounded-lg text-[10px] font-medium transition-colors ${
                  isActive
                    ? 'text-[#1B7F3B] font-bold'
                    : 'text-gray-500 hover:text-gray-900'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <div className={`p-1 rounded-full ${isActive ? 'bg-[#EAF6EC]' : ''}`}>
                    <Icon className={`w-5 h-5 ${isActive ? 'text-[#1B7F3B]' : 'text-gray-500'}`} />
                  </div>
                  <span className="mt-0.5 tracking-tight">{item.label}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
};
