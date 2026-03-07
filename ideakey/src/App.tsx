import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import DisplayAD from './pages/Services/DisplayAD'
import SearchAD from './pages/Services/SearchAD'
import Ecommerce from './pages/Services/Ecommerce'
import Mobile from './pages/Services/Mobile'
import Contents from './pages/Services/Contents'
import Influencer from './pages/Services/Influencer'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/services/display-ad" element={<DisplayAD />} />
        <Route path="/services/search-ad" element={<SearchAD />} />
        <Route path="/services/ecommerce" element={<Ecommerce />} />
        <Route path="/services/mobile" element={<Mobile />} />
        <Route path="/services/contents" element={<Contents />} />
        <Route path="/services/influencer" element={<Influencer />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
