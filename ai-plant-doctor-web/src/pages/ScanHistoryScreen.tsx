import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppHeader } from '../components/AppHeader';
import { getAllScanRecords, deleteScanRecord, clearAllScanRecords, ScanRecord } from '../services/storage';
import { Download, Trash2, Camera, Calendar, CheckCircle } from 'lucide-react';

export const ScanHistoryScreen: React.FC = () => {
  const navigate = useNavigate();
  const [scans, setScans] = useState<ScanRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const loadScans = async () => {
    setLoading(true);
    try {
      const records = await getAllScanRecords();
      setScans(records);
    } catch (err) {
      console.error('Failed to load scan records:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadScans();
  }, []);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    await deleteScanRecord(id);
    await loadScans();
  };

  const handleClearAll = async () => {
    if (confirm('Are you sure you want to delete all scan history records?')) {
      await clearAllScanRecords();
      await loadScans();
    }
  };

  const seedDemoData = () => {
    return [
      {
        id: 'seed_1',
        plantName: 'Tomato',
        diseaseName: 'Early Blight',
        timestamp: 'Apr 25, 2025 10:30 AM',
        confidence: 78,
        imageThumbnail: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=300&q=80',
      },
      {
        id: 'seed_2',
        plantName: 'Tomato',
        diseaseName: 'Healthy Foliage',
        timestamp: 'Apr 24, 2025 04:15 PM',
        confidence: 95,
        imageThumbnail: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=300&q=80',
      },
      {
        id: 'seed_3',
        plantName: 'Rice',
        diseaseName: 'Blast Risk',
        timestamp: 'Apr 23, 2025 11:20 AM',
        confidence: 82,
        imageThumbnail: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=300&q=80',
      },
      {
        id: 'seed_4',
        plantName: 'Rose',
        diseaseName: 'Black Spot',
        timestamp: 'Apr 22, 2025 09:10 AM',
        confidence: 76,
        imageThumbnail: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=300&q=80',
      },
      {
        id: 'seed_5',
        plantName: 'Mango',
        diseaseName: 'Healthy Foliage',
        timestamp: 'Apr 21, 2025 06:45 PM',
        confidence: 91,
        imageThumbnail: 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=300&q=80',
      },
    ];
  };

  const displayList = scans.length > 0 ? scans : seedDemoData();

  return (
    <div className="flex flex-col min-h-full">
      <AppHeader showBack backTo="/" title="AI Plant Doctor" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">Crop Health Diagnostic History</h1>
            <p className="text-sm text-gray-500 mt-1">
              Private on-device scan records stored in your browser's IndexedDB.
            </p>
          </div>
          {scans.length > 0 && (
            <button
              onClick={handleClearAll}
              className="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-xl text-xs font-bold transition-colors cursor-pointer"
            >
              Clear All History
            </button>
          )}
        </div>

        {/* 2 or 3-Column Grid of History Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayList.map((item: any) => {
            const isSeed = item.id.startsWith('seed_');
            return (
              <div
                key={item.id}
                onClick={() => navigate(`/report/${item.id}`)}
                className="bg-white rounded-2xl p-4 shadow-xs border border-gray-100 flex items-center justify-between hover:shadow-md hover:border-green-300 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <img
                    src={item.imageThumbnail}
                    alt={item.plantName}
                    className="w-16 h-16 rounded-xl object-cover bg-gray-100 border border-gray-100 shrink-0 shadow-xs"
                  />
                  <div className="min-w-0">
                    <h3 className="font-bold text-sm text-gray-900 truncate">
                      {item.plantName} — {item.diseaseName}
                    </h3>
                    <p className="text-[11px] text-gray-400 mt-0.5">
                      {item.timestamp?.includes('T')
                        ? new Date(item.timestamp).toLocaleString()
                        : item.timestamp}
                    </p>
                    <p className="text-xs text-[#1B7F3B] font-bold mt-1">
                      Confidence: {item.confidence || item.diseaseConfidence}%
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0 ml-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/report/${item.id}`);
                    }}
                    title="Download Report"
                    className="w-8 h-8 rounded-lg bg-green-50 text-[#1B7F3B] flex items-center justify-center hover:bg-green-100 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                  </button>

                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    disabled={isSeed}
                    title="Delete record"
                    className="w-8 h-8 rounded-lg bg-red-50 text-red-600 flex items-center justify-center hover:bg-red-100 disabled:opacity-40 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {scans.length === 0 && (
          <div className="mt-8 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-center text-xs text-gray-500">
            Showing benchmark diagnostic samples. Real leaf scans performed in this browser session are persisted here.
          </div>
        )}
      </div>
    </div>
  );
};
