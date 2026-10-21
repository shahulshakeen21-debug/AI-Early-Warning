import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { Sprout, Heart, Shield, HelpCircle, ExternalLink } from 'lucide-react';
import { BottomNav } from './BottomNav';

export const AppShell: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#F4F6F3] flex flex-col font-sans text-gray-900 selection:bg-green-100 selection:text-green-900">
      {/* Main Website Container */}
      <main className="flex-1 w-full flex flex-col">
        <Outlet />
      </main>

      {/* Website Footer (Desktop & Tablet) */}
      <footer className="bg-[#132A1C] text-gray-300 border-t border-green-950 mt-16 pt-12 pb-24 lg:pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
            {/* Col 1: Brand Info */}
            <div className="space-y-3 md:col-span-1">
              <div className="flex items-center gap-2 text-white">
                <div className="w-9 h-9 rounded-xl bg-white/10 flex items-center justify-center p-1.5">
                  <Sprout className="w-5 h-5 text-green-400" />
                </div>
                <span className="font-bold text-lg text-white">AI Plant Doctor</span>
              </div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Smart Plant Identification, Disease Detection & Agricultural Early Warning System for farmers and gardeners.
              </p>
              <div className="flex items-center gap-2 text-xs text-green-400 font-medium">
                <Shield className="w-4 h-4" />
                <span>Verified Agricultural Advisory</span>
              </div>
            </div>

            {/* Col 2: Quick Features */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-3">Core Modules</h4>
              <ul className="space-y-2 text-xs">
                <li><NavLink to="/scan" className="hover:text-white transition-colors">Plant & Leaf Scanner</NavLink></li>
                <li><NavLink to="/weather" className="hover:text-white transition-colors">Agro-Weather Alerts</NavLink></li>
                <li><NavLink to="/plants" className="hover:text-white transition-colors">Botanical Species Database</NavLink></li>
                <li><NavLink to="/care" className="hover:text-white transition-colors">Plant Care & Disease Advice</NavLink></li>
              </ul>
            </div>

            {/* Col 3: Resources */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-3">Resources & Portals</h4>
              <ul className="space-y-2 text-xs">
                <li><NavLink to="/schemes" className="hover:text-white transition-colors">PM-KISAN & PMFBY Schemes</NavLink></li>
                <li><NavLink to="/history" className="hover:text-white transition-colors">Diagnosis History & Records</NavLink></li>
                <li><a href="https://open-meteo.com/" target="_blank" rel="noreferrer" className="hover:text-white transition-colors flex items-center gap-1">Open-Meteo Weather API <ExternalLink className="w-3 h-3" /></a></li>
                <li><a href="https://icar.org.in/" target="_blank" rel="noreferrer" className="hover:text-white transition-colors flex items-center gap-1">ICAR Advisory Guidelines <ExternalLink className="w-3 h-3" /></a></li>
              </ul>
            </div>

            {/* Col 4: Official Disclaimers */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-3">Important Notice</h4>
              <div className="bg-white/5 border border-white/10 rounded-xl p-3 text-[11px] text-gray-300 leading-relaxed">
                <p>
                  This portal serves as an AI-powered agricultural decision-support companion. For critical field outbreaks, always consult your local Agriculture Officer or Krishi Vigyan Kendra (KVK).
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-white/10 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-gray-400">
            <p>© {new Date().getFullYear()} AI Plant Doctor. Better Plants. Healthier Crops. Brighter Future.</p>
            <div className="flex items-center gap-1 text-xs">
              <span>Crafted for Indian Agriculture with</span>
              <Heart className="w-3.5 h-3.5 text-red-400 fill-red-400" />
            </div>
          </div>
        </div>
      </footer>

      {/* Mobile-Only Bottom Navigation (hidden on desktop screens >= 1024px) */}
      <div className="lg:hidden">
        <BottomNav />
      </div>
    </div>
  );
};
