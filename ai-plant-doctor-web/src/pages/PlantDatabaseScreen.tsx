import React, { useState } from 'react';
import { AppHeader } from '../components/AppHeader';
import { Search } from 'lucide-react';
import plantsData from '../data/plants.json';

interface PlantItem {
  id: string;
  name_en: string;
  name_ta: string;
  scientific_name: string;
  category: string;
  support_status: string;
  image_url?: string;
  description?: string;
}

export const PlantDatabaseScreen: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCat, setSelectedCat] = useState('All Categories');
  const [selectedStatus, setSelectedStatus] = useState('All Status');

  const plantImages: Record<string, string> = {
    tomato: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=400&q=80',
    rice: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80',
    mango: 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=400&q=80',
    rose: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80',
    turmeric: 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=400&q=80',
    banana: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=400&q=80',
    cotton: 'https://images.unsplash.com/photo-1606041008023-472dfb5e530f?auto=format&fit=crop&w=400&q=80',
    potato: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=400&q=80',
    chilli: 'https://images.unsplash.com/photo-1563865436874-9aef32095fad?auto=format&fit=crop&w=400&q=80',
  };

  const plantsList: PlantItem[] = Object.entries(plantsData).map(([id, p]: [string, any]) => ({
    id,
    name_en: p.name?.en || id,
    name_ta: p.name?.ta || id,
    scientific_name: p.scientific_name || 'Plantae',
    category: p.category || 'Vegetables',
    support_status: p.support_status || 'both_models',
    image_url: plantImages[id] || 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=400&q=80',
    description: p.description?.en || '',
  }));

  const filteredPlants = plantsList.filter((p) => {
    const matchQuery =
      p.name_en.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.scientific_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchCat = selectedCat === 'All Categories' || p.category.toLowerCase() === selectedCat.toLowerCase();
    const matchStatus =
      selectedStatus === 'All Status' ||
      (selectedStatus === 'Disease Model' && p.support_status.includes('disease')) ||
      (selectedStatus === 'Information Only' && p.support_status.includes('info'));

    return matchQuery && matchCat && matchStatus;
  });

  const getStatusBadges = (plant: PlantItem) => {
    if (plant.id === 'tomato') {
      return (
        <div className="flex flex-wrap gap-1.5 mt-2">
          <span className="bg-emerald-50 text-emerald-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-emerald-200">
            Disease Model
          </span>
          <span className="bg-blue-50 text-blue-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-blue-200">
            Supported
          </span>
        </div>
      );
    }
    if (plant.id === 'rose') {
      return (
        <div className="flex flex-wrap gap-1.5 mt-2">
          <span className="bg-purple-50 text-purple-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-purple-200">
            Identification Model
          </span>
          <span className="bg-blue-50 text-blue-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-blue-200">
            Supported
          </span>
        </div>
      );
    }
    return (
      <div className="flex flex-wrap gap-1.5 mt-2">
        <span className="bg-amber-50 text-amber-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-amber-200">
          Information Only
        </span>
        <span className="bg-blue-50 text-blue-700 text-[10px] font-bold px-2.5 py-1 rounded-md border border-blue-200">
          Verified
        </span>
      </div>
    );
  };

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">Botanical & Crop Species Database</h1>
            <p className="text-sm text-gray-500 mt-1">
              Browse Indian agricultural crops, taxonomic classifications, and AI model compatibility.
            </p>
          </div>

          {/* Filters Bar */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative min-w-[220px]">
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3 pointer-events-none" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search species..."
                className="w-full bg-white border border-gray-200 text-xs text-gray-800 rounded-xl pl-9 pr-3 py-2.5 focus:outline-none focus:border-[#1B7F3B]"
              />
            </div>

            <select
              value={selectedCat}
              onChange={(e) => setSelectedCat(e.target.value)}
              className="bg-white border border-gray-200 text-xs text-gray-700 rounded-xl px-3 py-2.5 focus:outline-none focus:border-[#1B7F3B]"
            >
              <option>All Categories</option>
              <option>Vegetables</option>
              <option>Cereals</option>
              <option>Fruits</option>
              <option>Flowers</option>
              <option>Spices</option>
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-white border border-gray-200 text-xs text-gray-700 rounded-xl px-3 py-2.5 focus:outline-none focus:border-[#1B7F3B]"
            >
              <option>All Status</option>
              <option>Disease Model</option>
              <option>Information Only</option>
            </select>
          </div>
        </div>

        {/* Responsive Multi-column Grid for Website */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {filteredPlants.map((plant) => (
            <div
              key={plant.id}
              className="bg-white rounded-2xl p-4 shadow-xs border border-gray-100 flex flex-col justify-between hover:shadow-lg hover:border-green-300 transition-all group"
            >
              <div>
                <div className="h-44 rounded-xl overflow-hidden bg-gray-100 shadow-xs mb-3 group-hover:scale-[1.02] transition-transform">
                  <img
                    src={plant.image_url}
                    alt={plant.name_en}
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                </div>
                <h3 className="font-bold text-base text-gray-900 leading-snug">
                  {plant.name_en}
                </h3>
                <p className="text-xs text-gray-400 italic">
                  ({plant.scientific_name})
                </p>
                {plant.description && (
                  <p className="text-xs text-gray-500 mt-2 line-clamp-2 leading-relaxed">
                    {plant.description}
                  </p>
                )}
              </div>
              <div>{getStatusBadges(plant)}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
