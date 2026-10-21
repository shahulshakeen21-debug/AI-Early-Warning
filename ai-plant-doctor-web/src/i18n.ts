import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslation from './data/en.json';
import taTranslation from './data/ta.json';

const savedLang = localStorage.getItem('plant_doctor_lang') || 'en';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: enTranslation },
    ta: { translation: taTranslation }
  },
  lng: savedLang,
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false
  }
});

export default i18n;
