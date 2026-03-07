import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import Breadcrumb from '../../../components/Breadcrumb'
import { Smartphone } from 'lucide-react'

export default function Mobile() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="pt-20">
        <div className="bg-gray-50 py-4">
          <div className="container mx-auto px-6">
            <Breadcrumb items={[{ label: '모바일 광고' }]} />
          </div>
        </div>
        <section className="py-16 bg-gradient-to-r from-navy to-primary text-white">
          <div className="container mx-auto px-6 text-center">
            <Smartphone className="mx-auto mb-4" size={48} />
            <h1 className="text-4xl font-bold mb-4">모바일 광고</h1>
            <p className="text-xl">앱 · 모바일 광고 서비스</p>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
