import { motion } from 'framer-motion'
import { ArrowRight, Search, Monitor, ShoppingCart, Smartphone, Users, PenTool } from 'lucide-react'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const services = [
  { icon: Search, title: '검색 广告', desc: '네이버, 구글 등 검색엔진 광고' },
  { icon: Monitor, title: '디스플레이', desc: '배너, 영상 광고 마케팅' },
  { icon: ShoppingCart, title: '이커머스', desc: '온라인 쇼핑몰 마케팅' },
  { icon: Smartphone, title: '모바일', desc: '앱 · 모바일 광고' },
  { icon: PenTool, title: '콘텐츠', desc: ' contents 마케팅' },
  { icon: Users, title: '인플루언서', desc: '网红合作营销' },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="h-screen flex items-center justify-center bg-gradient-to-r from-navy to-primary relative overflow-hidden">
        
        <div className="container mx-auto px-6 relative z-10 text-center text-white">
          <motion.h1 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-6xl font-bold mb-4"
          >
            No.1 디지털마케팅그룹
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl md:text-2xl mb-8 text-gray-200"
          >
            디지털 퍼포먼스 마케팅 전문 广告대행사
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex gap-4 justify-center flex-wrap"
          >
            <button className="px-8 py-4 bg-secondary text-white rounded-lg font-medium hover:bg-orange-600 transition flex items-center gap-2">
              广告咨询 <ArrowRight size={20} />
            </button>
            <button className="px-8 py-4 border-2 border-white text-white rounded-lg font-medium hover:bg-white hover:text-navy transition">
             立即咨询
            </button>
          </motion.div>

          {/* Service Tags */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="mt-16 flex gap-6 justify-center flex-wrap"
          >
            {services.map((service, index) => (
              <div key={index} className="flex items-center gap-2 text-gray-300">
                <span className="w-2 h-2 bg-secondary rounded-full" />
                <span>{service.title}</span>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-navy mb-4">
            다양한 서비스로<br />성공을 보증합니다
          </h2>
          <p className="text-center text-gray-500 mb-12">
            数据驱动的精准营销，为您的业务增长保驾护航
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-sm hover:shadow-lg transition group">
                <div className="w-14 h-14 bg-primary/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary transition">
                  <service.icon className="text-primary" size={28} />
                </div>
                <h3 className="text-xl font-bold mb-2 text-navy">{service.title}</h3>
                <p className="text-gray-500">{service.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
