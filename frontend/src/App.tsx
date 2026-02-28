import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ResultPage from './pages/ResultPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* HomePage */}
        <Route path="/" element={<HomePage />} />
        
        {/* ResultPage */}
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
