import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import Breadcrumb from '../../../components/Breadcrumb'
import { Check, ExternalLink } from 'lucide-react'

const features = [
  '비즈니스 목표에 따라 다양한 매체에 시각적으로 광고 노출',
  '가망고객에 대한 타겟팅이 가능해 단기적으로 performance를 낼 수 있음',
  '다양한 타겟 트래픽 유도로 브랜드 홍보 및 이미지 구축효과 탁월',
  '광고 매체 및 타깃에 맞는 브랜딩을 위해 그래픽 이미지, 텍스트 등 맞춤형 소재제작',
]

const pricing = [
  { title: 'CPM 방식', desc: '노출 기준으로 광고단가를 책정하여 비용을 지불하는 방식' },
  { title: 'CPC 방식', desc: '클릭이 일어난 횟수만큼 비용을 지불하는 방식' },
]

const process = [
  { title: '목표수립', desc: '광고주의 니즈 및 비즈니스에 맞는 KPI 수립' },
  { title: '시장조사', desc: '자사 및 타사 동종업계 레퍼런스를 활용한 분석 및 논의' },
  { title: '매체설정', desc: '광고를 노출하고자하는 주요 매체 및 성별, 연령, 지역 등 상세 타깃 설정' },
  { title: '컨텐츠', desc: '매체 및 타깃에 맞는 브랜딩을 위해 그래픽 이미지, 텍스트 등 광고주 맞춤형 소재제작' },
  { title: '광고검토', desc: '광고 검토 진행 완료 후 노출' },
  { title: '효과분석', desc: '배너광고 클릭을 통한 제품 구매자 및 일자별 유입수 조회/분석후 피드백' },
]

export default function DisplayAD() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="bg-gray-50 py-4">
          <div className="container mx-auto px-6">
            <Breadcrumb 
              items={[
                { label: '광고서비스', href: '/services' },
                { label: '디스플레이광고' },
              ]}
            />
          </div>
        </div>

        {/* Page Title */}
        <section className="py-16 bg-gradient-to-r from-navy to-primary text-white">
          <div className="container mx-auto px-6 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">디스플레이광고</h1>
            <p className="text-xl text-gray-200">
              이미지, 애니메이션, 동영상 등 다양한 형태로 메시지를 전달하며<br />
              주요포털 메인화면 및 제휴 네트워크사에 노출되는 배너 광고
            </p>
          </div>
        </section>

        {/* Features */}
        <section className="py-16">
          <div className="container mx-auto px-6">
            <h2 className="text-2xl font-bold text-center mb-12">디스플레이광고 강점</h2>
            <div className="grid md:grid-cols-2 gap-6">
              {features.map((feature, index) => (
                <div key={index} className="flex items-start gap-4 p-6 bg-gray-50 rounded-xl">
                  <Check className="text-secondary flex-shrink-0 mt-1" size={24} />
                  <p className="text-gray-700">{feature}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Exposure */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-6">
            <h2 className="text-2xl font-bold text-center mb-8">디스플레이광고 노출위치</h2>
            <ul className="max-w-2xl mx-auto space-y-4">
              <li className="flex items-center gap-3 text-lg">
                <span className="w-3 h-3 bg-secondary rounded-full" />
                주요 포털 메인화면 및 섹션
              </li>
              <li className="flex items-center gap-3 text-lg">
                <span className="w-3 h-3 bg-secondary rounded-full" />
                제휴된 네트워크사
              </li>
            </ul>
          </div>
        </section>

        {/* Pricing */}
        <section className="py-16">
          <div className="container mx-auto px-6">
            <h2 className="text-2xl font-bold text-center mb-12">디스플레이광고 과금방식</h2>
            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              {pricing.map((item, index) => (
                <div key={index} className="p-8 border-2 border-gray-200 rounded-xl text-center hover:border-secondary transition">
                  <h3 className="text-xl font-bold mb-4 text-navy">{item.title}</h3>
                  <p className="text-gray-500">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Process */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-6">
            <h2 className="text-2xl font-bold text-center mb-12">진행流程</h2>
            <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-4">
              {process.map((step, index) => (
                <div key={index} className="text-center">
                  <div className="w-12 h-12 bg-secondary text-white rounded-full flex items-center justify-center font-bold mx-auto mb-3">
                    {index + 1}
                  </div>
                  <h3 className="font-bold text-navy mb-2">{step.title}</h3>
                  <p className="text-sm text-gray-500">{step.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Related Links */}
        <section className="py-16">
          <div className="container mx-auto px-6">
            <h2 className="text-2xl font-bold text-center mb-8">相关链接</h2>
            <div className="flex flex-wrap gap-4 justify-center">
              <a href="#" className="flex items-center gap-2 px-6 py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
                네이버 디스플레이광고 <ExternalLink size={16} />
              </a>
              <a href="#" className="flex items-center gap-2 px-6 py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
                카카오(다음) 디스플레이광고 <ExternalLink size={16} />
              </a>
              <a href="#" className="flex items-center gap-2 px-6 py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
                네트워크 디스플레이광고 <ExternalLink size={16} />
              </a>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}
