import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import Breadcrumb from '../../../components/Breadcrumb'
import { PenTool } from 'lucide-react'

export default function Contents() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="pt-20">
        <div className="bg-gray-50 py-4">
          <div className="container mx-auto px-6">
            <Breadcrumb items={[{ label: '콘텐츠 마케팅' }]} />
          </div>
        </div>
        <section className="py-16 bg-gradient-to-r from-navy to-primary text-white">
          <div className="container mx-auto px-6 text-center">
            <PenTool className="mx-auto mb-4" size={48} />
            <h1 className="text-4xl font-bold mb-4">콘텐츠 마케팅</h1>
            <p className="text-xl">内容营销服务</p>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
