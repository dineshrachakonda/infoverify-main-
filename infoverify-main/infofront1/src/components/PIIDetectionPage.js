import React, { useState } from 'react';
import { Upload, FileCheck2 } from 'lucide-react';

const requiredDocuments = [
  { type: 'aadhar', label: 'Aadhar Card' },
  { type: 'tenth', label: '10th Scorecard' },
  { type: 'inter', label: 'Inter Scorecard' },
  { type: 'gate', label: 'GATE Scorecard' },
  { type: 'candidate', label: 'Candidate Details' },
];

function PIIDetectionPage() {
  const [documents, setDocuments] = useState([]);
  const [processingResults, setProcessingResults] = useState([]);

  const handleFileInput = (type) => (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const filteredDocs = documents.filter(doc => doc.type !== type);
      const newDocument = {
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        type: type,
      };
      setDocuments([...filteredDocs, newDocument]);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', padding: '24px', display: 'flex', flexDirection: 'column' }}>
      <header style={{ backgroundColor: 'white', padding: '16px', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h1 style={{ fontSize: '24px', fontWeight: '600', color: '#111827', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FileCheck2 style={{ width: '32px', height: '32px', color: '#2563eb' }} />
          RAC Document Verification System
        </h1>
      </header>

      <main style={{ display: 'flex', flex: '1', padding: '24px' }}>
        <div style={{ width: '66%', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', padding: '24px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '24px' }}>Upload Required Documents</h2>
          <div>
            {requiredDocuments.map(({ type, label }) => {
              const doc = documents.find(d => d.type === type);
              return (
                <div key={type} style={{ display: 'flex', alignItems: 'center', padding: '16px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '12px' }}>
                  <h3 style={{ fontWeight: '500', color: '#111827', width: '33%' }}>{label}</h3>
                  <div style={{ display: 'flex', alignItems: 'center', marginLeft: 'auto' }}>
                    <label style={{ display: 'inline-flex', alignItems: 'center', padding: '8px 16px', borderRadius: '6px', border: '1px solid #2563eb', color: '#2563eb', cursor: 'pointer' }}>
                      <Upload style={{ width: '16px', height: '16px', marginRight: '8px' }} />
                      {doc ? 'Replace' : 'Upload'}
                      <input type="file" style={{ display: 'none' }} onChange={handleFileInput(type)} accept=".pdf,.jpg,.jpeg,.png" />
                    </label>
                    <div style={{ fontSize: '14px', color: '#6b7280', marginLeft: '12px' }}>{doc ? doc.name : 'No file selected'}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <aside style={{ width: '30%', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', padding: '24px', marginLeft: 'auto', alignSelf: 'start', marginTop: '40px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '16px' }}>Processing Results</h2>
          <div style={{ color: '#4b5563', minHeight: '150px', border: '1px solid #e5e7eb', padding: '10px', borderRadius: '8px', overflowY: 'auto' }}>
            {processingResults.length > 0 ? processingResults.map((result, index) => (
              <p key={index} style={{ marginBottom: '5px' }}>{result}</p>
            )) : <p style={{ color: '#9ca3af', textAlign: 'center' }}>Results will appear here...</p>}
          </div>
        </aside>
      </main>

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <button style={{ padding: '12px 24px', backgroundColor: '#2563eb', color: 'white', fontSize: '18px', fontWeight: 'bold', borderRadius: '8px', cursor: 'pointer', border: 'none' }}>Process Documents</button>
      </div>
    </div>
  );
}

export default PIIDetectionPage;















