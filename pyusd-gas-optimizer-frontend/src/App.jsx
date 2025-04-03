import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CurrentGas from './components/CurrentGas';
import GasHistory from './components/GasHistory';
import GasEstimate from './components/GasEstimate';
import GasPrediction from './components/GasPrediction';

function App() {
  return (
    <Router>
      <div className="container">
        <h1>PYUSD Gas Optimizer</h1>
        <nav>
          <Link to="/">Home</Link> | <Link to="/predict">Predicted Gas Price</Link>
        </nav>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <CurrentGas />
                <GasHistory />
                <GasEstimate />
              </>
            }
          />
          <Route path="/predict" element={<GasPrediction />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;