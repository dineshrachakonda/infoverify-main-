import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './App.css';
import Auth from './components/Auth';
import PIIDetectionPage from './components/PIIDetectionPage';

function Home() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'black', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      {/* Top Image */}
      <div style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
        <img 
          src="https://verifyonline.co.uk/wp-content/uploads/2019/06/document-verification-1.png" 
          alt="Top Image" 
          style={{ maxWidth: '90%', maxHeight: '300px', borderRadius: '10px' }}
        />
      </div>
      {/* Bottom Content */}
      <div style={{ backgroundColor: '#1e1e1e', padding: '40px', borderRadius: '10px', textAlign: 'center', width: '80%', maxWidth: '800px' }}>
        <img 
          src="https://nanonets.com/blog/content/images/size/w1600/format/webp/2022/06/shutterstock_1785042593.jpg" 
          alt="Shield Icon" 
          style={{ width: '120px', height: '100px', margin: '0 auto' }}
        />
        <h1 style={{ color: 'white', fontSize: '28px', marginTop: '15px' }}>Info Verify</h1>
        <p style={{ color: '#bbb', marginTop: '15px' }}>
          Extraction and Verification of Information from Semi-Categorised data.
        </p>
        <p style={{ color: '#bbb', marginTop: '15px' }}>
          Click Below To Sign-in
        </p>
        <div style={{ marginTop: '25px' }}>
          <Link to="/auth" style={{ color: 'white', fontSize: '20px', textDecoration: 'underline' }}>
            Proceed to Sign-in
          </Link>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Toaster position="top-center" />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/PIIDetectionPage" element={<PIIDetectionPage />} />
      </Routes>
    </Router>
  );
}

export default App;



