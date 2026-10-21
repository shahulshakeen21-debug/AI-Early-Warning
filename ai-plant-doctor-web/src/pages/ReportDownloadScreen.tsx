import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppHeader } from '../components/AppHeader';
import { getScanRecordById, ScanRecord } from '../services/storage';
import { Sprout, Download, Info, CheckCircle2, AlertTriangle, ArrowLeft } from 'lucide-react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export const ReportDownloadScreen: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [record, setRecord] = useState<ScanRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function load() {
      if (id && !id.startsWith('seed_')) {
        const found = await getScanRecordById(id);
        if (found) {
          setRecord(found);
          setLoading(false);
          return;
        }
      }

      setRecord({
        id: id || 'sample_12',
        timestamp: '25 Apr 2025, 10:30 AM',
        plantName: 'Tomato',
        plantScientificName: 'Solanum lycopersicum',
        diseaseName: 'Early Blight',
        diseaseScientificName: 'Alternaria solani',
        diseaseConfidence: 78,
        plantConfidence: 92,
        isHealthy: false,
        symptoms: [
          'Dark brown circular spots with concentric rings',
          'Progressive yellowing and chlorosis of surrounding leaf margins',
          'Stem collar rot and premature leaf drop in advanced stages',
        ],
        recommendedActions: [
          'Immediately excise and destroy heavily infected lower foliage',
          'Apply prophylactic copper oxychloride or biological neem formulation',
          'Maintain adequate plant spacing (60 cm) to facilitate aeration',
          'Avoid overhead sprinkler irrigation; apply moisture at root level',
        ],
        imageThumbnail:
          'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=400&q=80',
        weatherSnapshot: {
          location: 'Coimbatore, Tamil Nadu',
          temperature: 28,
          humidity: 70,
        },
      });
      setLoading(false);
    }
    load();
  }, [id]);

  const handleDownloadPdf = async () => {
    if (!reportRef.current) return;
    setGenerating(true);
    try {
      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        useCORS: true,
      });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`AI_Plant_Doctor_Report_${record?.plantName || 'Plant'}.pdf`);
    } catch (err) {
      console.error('PDF export failed:', err);
    } finally {
      setGenerating(false);
    }
  };

  if (loading || !record) {
    return (
      <div className="flex flex-col min-h-full">
        <AppHeader showBack backTo="/history" title="AI Plant Doctor" />
        <div className="p-16 text-center text-xs text-gray-500">Loading diagnostic report details...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/history" title="AI Plant Doctor" />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">Diagnostic Certificate & Scan Report</h1>
            <p className="text-sm text-gray-500 mt-1">
              Official summary of pathological findings, clinical symptoms, and safe extension guidance.
            </p>
          </div>

          <button
            onClick={handleDownloadPdf}
            disabled={generating}
            className="bg-[#1B7F3B] hover:bg-[#0F5A2B] text-white font-bold py-3 px-6 rounded-xl text-xs transition-all shadow-md flex items-center justify-center gap-2 cursor-pointer shrink-0"
          >
            <Download className="w-4 h-4 text-green-200" />
            <span>{generating ? 'Compiling PDF...' : 'Download Official PDF Report'}</span>
          </button>
        </div>

        {/* Printable/Exportable Certificate Card */}
        <div
          ref={reportRef}
          className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200 flex flex-col gap-6 text-gray-800"
        >
          {/* Header of Report */}
          <div className="flex items-center justify-between border-b border-gray-100 pb-5">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-green-50 flex items-center justify-center text-[#1B7F3B] p-2">
                <Sprout className="w-8 h-8" />
              </div>
              <div>
                <h2 className="font-extrabold text-xl tracking-tight text-[#1B7F3B]">
                  AI Plant Doctor
                </h2>
                <p className="text-xs text-gray-400">
                  Agricultural Early Warning & Disease Decision Support
                </p>
              </div>
            </div>
            <div className="text-right">
              <span className="bg-green-100 text-[#1B7F3B] text-[11px] font-bold px-3 py-1 rounded-full uppercase tracking-wider block mb-1">
                Official Report
              </span>
              <span className="text-[11px] text-gray-400">
                Ref ID: #{record.id.slice(-8)}
              </span>
            </div>
          </div>

          {/* Plant & Date row with leaf thumbnail */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start bg-gray-50/70 rounded-2xl p-6 border border-gray-100">
            <div className="md:col-span-2 space-y-2.5 text-xs">
              <div className="grid grid-cols-3 gap-2">
                <span className="font-bold text-gray-500">Specimen Plant:</span>
                <span className="col-span-2 font-extrabold text-sm text-gray-900">
                  {record.plantName} <span className="text-xs font-normal italic text-gray-500">({record.plantScientificName || 'Solanum lycopersicum'})</span>
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2">
                <span className="font-bold text-gray-500">Date & Timestamp:</span>
                <span className="col-span-2 text-gray-800">
                  {record.timestamp.includes('T')
                    ? new Date(record.timestamp).toLocaleString()
                    : record.timestamp}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2">
                <span className="font-bold text-gray-500">Predicted Pathology:</span>
                <span className={`col-span-2 font-bold text-sm ${record.isHealthy ? 'text-green-700' : 'text-red-600'}`}>
                  {record.diseaseName}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2">
                <span className="font-bold text-gray-500">Confidence Metric:</span>
                <span className="col-span-2 font-extrabold text-gray-900">
                  {record.diseaseConfidence || 78}% Probability
                </span>
              </div>
            </div>

            <div className="flex justify-center md:justify-end">
              <img
                src={record.imageThumbnail}
                alt="Examined specimen"
                className="w-28 h-28 rounded-2xl object-cover bg-gray-100 shadow-xs border border-gray-200"
                crossOrigin="anonymous"
              />
            </div>
          </div>

          {/* Symptoms List */}
          <div className="space-y-2">
            <h3 className="font-bold text-sm text-gray-900">Observed Clinical Symptoms</h3>
            <ul className="space-y-1.5 text-xs text-gray-600 pl-2">
              {record.symptoms?.map((s, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-[#1B7F3B] font-bold">•</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Recommended Actions */}
          <div className="space-y-2">
            <h3 className="font-bold text-sm text-gray-900">Actionable Management & Spray Schedule</h3>
            <ul className="space-y-1.5 text-xs text-gray-600 pl-2">
              {record.recommendedActions?.map((a, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-[#1B7F3B] font-bold">•</span>
                  <span>{a}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Weather Snapshot */}
          <div className="space-y-1 bg-blue-50/50 rounded-2xl p-4 border border-blue-100 text-xs">
            <span className="font-bold text-gray-900 block">Environmental Snapshot during Scan</span>
            <span className="text-gray-600">
              Station: {record.weatherSnapshot?.location || 'Coimbatore, Tamil Nadu'} • Temperature: {record.weatherSnapshot?.temperature || 28}°C • Relative Humidity: {record.weatherSnapshot?.humidity || 70}%
            </span>
          </div>

          {/* Disclaimer box */}
          <div className="bg-emerald-50/80 border border-emerald-200 rounded-2xl p-4 flex items-start gap-3">
            <Info className="w-5 h-5 text-[#1B7F3B] shrink-0 mt-0.5" />
            <p className="text-xs text-emerald-950 leading-relaxed">
              This diagnostic document is generated for agricultural decision-support and academic purposes. For large-scale outbreaks or commercial spraying, please confirm with your local block Agricultural Officer or Krishi Vigyan Kendra (KVK).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
