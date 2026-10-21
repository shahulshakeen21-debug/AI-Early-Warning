import { openDB, DBSchema, IDBPDatabase } from 'idb';

export interface ScanRecord {
  id: string;
  timestamp: string;
  plantName: string;
  plantScientificName?: string;
  plantConfidence?: number;
  diseaseName: string;
  diseaseScientificName?: string;
  diseaseConfidence?: number;
  isHealthy: boolean;
  symptoms?: string[];
  recommendedActions?: string[];
  imageThumbnail: string; // Base64 data URL
  weatherSnapshot?: {
    location: string;
    temperature: number;
    humidity: number;
  };
}

interface PlantDoctorDB extends DBSchema {
  scans: {
    key: string;
    value: ScanRecord;
    indexes: { 'by-date': string };
  };
}

let dbPromise: Promise<IDBPDatabase<PlantDoctorDB>> | null = null;

export function getDB() {
  if (!dbPromise) {
    dbPromise = openDB<PlantDoctorDB>('plant_doctor_db', 1, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('scans')) {
          const store = db.createObjectStore('scans', { keyPath: 'id' });
          store.createIndex('by-date', 'timestamp');
        }
      },
    });
  }
  return dbPromise;
}

export async function saveScanRecord(record: ScanRecord): Promise<void> {
  const db = await getDB();
  await db.put('scans', record);
}

export async function getAllScanRecords(): Promise<ScanRecord[]> {
  const db = await getDB();
  const all = await db.getAll('scans');
  return all.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
}

export async function getScanRecordById(id: string): Promise<ScanRecord | undefined> {
  const db = await getDB();
  return db.get('scans', id);
}

export async function deleteScanRecord(id: string): Promise<void> {
  const db = await getDB();
  await db.delete('scans', id);
}

export async function clearAllScanRecords(): Promise<void> {
  const db = await getDB();
  await db.clear('scans');
}
