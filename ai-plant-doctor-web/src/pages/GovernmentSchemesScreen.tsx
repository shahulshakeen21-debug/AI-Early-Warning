import React from 'react';
import { AppHeader } from '../components/AppHeader';
import { ExternalLink, CheckCircle } from 'lucide-react';
import schemesData from '../data/schemes.json';

export const GovernmentSchemesScreen: React.FC = () => {
  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6">
          <h1 className="text-2xl font-extrabold text-gray-900">Government Agricultural Schemes & Welfare Portals</h1>
          <p className="text-sm text-gray-500 mt-1">
            Access verified financial support, subsidized crop insurance, and soil health initiatives from the Government of India and State Departments.
          </p>
        </div>

        {/* 3-Column Responsive Grid on Desktop */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemesData.map((scheme: any) => (
            <div
              key={scheme.id}
              className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-green-300 transition-all group"
            >
              <div>
                <div className="flex items-start gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center text-[#1B7F3B] shrink-0 font-bold text-lg group-hover:scale-105 transition-transform">
                    🌾
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-gray-900 leading-snug">
                      {scheme.name?.en || scheme.id}
                    </h3>
                    <p className="text-[11px] text-gray-500 mt-0.5">
                      {scheme.department?.en || 'Ministry of Agriculture & Farmers Welfare'}
                    </p>
                  </div>
                </div>

                {/* Details Breakdown */}
                <div className="text-xs space-y-2 text-gray-600 bg-gray-50/80 rounded-xl p-3 mb-4">
                  <div>
                    <strong className="text-gray-900 block mb-0.5">Key Benefits:</strong>
                    <span className="leading-relaxed">
                      {Array.isArray(scheme.key_benefits?.en)
                        ? scheme.key_benefits.en.join('; ')
                        : scheme.key_benefits?.en || 'Direct income assistance to eligible farmer families.'}
                    </span>
                  </div>
                  <div>
                    <strong className="text-gray-900 block mb-0.5">Eligibility:</strong>
                    <span className="leading-relaxed">
                      {Array.isArray(scheme.eligibility?.en)
                        ? scheme.eligibility.en.join('; ')
                        : scheme.eligibility?.en || 'Small and marginal farmers across all states.'}
                    </span>
                  </div>
                  <div>
                    <strong className="text-gray-900 block mb-0.5">Application Procedure:</strong>
                    <span className="leading-relaxed">
                      {scheme.application_procedure?.en || 'Apply online via the designated government portal or at local Common Service Centres (CSC).'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Official Link Button */}
              <a
                href={scheme.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white text-xs font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-xs group-hover:shadow-md cursor-pointer"
              >
                <span>Visit Official Portal</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
