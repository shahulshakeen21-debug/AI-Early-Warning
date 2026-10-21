import { create } from 'zustand';

export interface ScanResult {
  plantName: string;
  scientificName: string;
  plantConfidence: number;
  isHealthy: boolean;
  diseaseName: string;
  diseaseScientificName: string;
  diseaseConfidence: number;
  symptoms: string[];
  recommendedActions: string[];
  imageSrc: string; // Preview data URL
}

interface AppState {
  currentScan: ScanResult | null;
  setCurrentScan: (scan: ScanResult | null) => void;
  selectedCategory: string;
  setSelectedCategory: (cat: string) => void;
  selectedLanguage: 'en' | 'ta';
  setSelectedLanguage: (lang: 'en' | 'ta') => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentScan: null,
  setCurrentScan: (scan) => set({ currentScan: scan }),
  selectedCategory: 'Vegetables',
  setSelectedCategory: (selectedCategory) => set({ selectedCategory }),
  selectedLanguage: (localStorage.getItem('plant_doctor_lang') as 'en' | 'ta') || 'en',
  setSelectedLanguage: (selectedLanguage) => {
    localStorage.setItem('plant_doctor_lang', selectedLanguage);
    set({ selectedLanguage });
  },
}));
