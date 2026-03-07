import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import Breadcrumb from '../../../components/Breadcrumb'
import { Search } from 'lucide-react'

export default function SearchAD() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="pt-20">
        <div className="bg-gray-50 py-4">
          <div className="container mx-auto px-6">
            <Breadcrumb items={[{ label: '검색광고' }]} />
          </div>
        </div>
        <section className="py-16 bg-gradient-to-r from-navy to-primary text-white">
          <div className="container mx-auto px-6 text-center">
            <Search className="mx-auto mb-4" size={48} />
            <h1 className="text-4xl font-bold mb-4">검색광고</h1>
            <p className="text-xl">네이버, 구글 등 검색엔진 광고 서비스</p>
          </div>
        </section>
        <section className="py-16 container mx-auto px-6">
          <p className="text-center text-gray-600">검색광고 페이지建设中...</p>
        </section>
      </main>
      <Footer />
    </div>
  )
}
