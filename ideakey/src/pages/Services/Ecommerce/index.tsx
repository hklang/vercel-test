import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import Breadcrumb from '../../../components/Breadcrumb'
import { ShoppingCart } from 'lucide-react'

export default function Ecommerce() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="pt-20">
        <div className="bg-gray-50 py-4">
          <div className="container mx-auto px-6">
            <Breadcrumb items={[{ label: '이커머스 마케팅' }]} />
          </div>
        </div>
        <section className="py-16 bg-gradient-to-r from-navy to-primary text-white">
          <div className="container mx-auto px-6 text-center">
            <ShoppingCart className="mx-auto mb-4" size={48} />
            <h1 className="text-4xl font-bold mb-4">이커머스 마케팅</h1>
            <p className="text-xl">온라인 쇼핑몰 마케팅 서비스</p>
          </div>
        </section>
        <section className="py-16 container mx-auto px-6">
          <p className="text-center text-gray-600">电商营销页面建设中...</p>
        </section>
      </main>
      <Footer />
    </div>
  )
}
