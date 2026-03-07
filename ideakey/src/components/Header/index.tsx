import { useState } from 'react'
import { ChevronDown, Menu, X } from 'lucide-react'

const navItems = [
  {
    title: '회사소개',
    submenu: ['아이디어키 소개', '비전', '연혁·조직도', '협력사', '제휴', '오시는 길']
  },
  {
    title: '광고서비스',
    submenu: ['Search AD', 'Display AD', 'E-commerce', 'Mobile', 'Contents', 'Influencer', '언론홍보']
  },
  {
    title: '웹마케팅',
    submenu: ['웹·프로모션 페이지', '솔루션']
  },
  {
    title: '인재채용',
    submenu: ['인사제도', '채용안내', '교육제도']
  },
  {
    title: '고객센터',
    submenu: ['공지사항', '견적문의', '카드결제', '자주 묻는 질문']
  }
]

export default function Header() {
  const [activeMenu, setActiveMenu] = useState<number | null>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white shadow-md' : 'bg-white/90 backdrop-blur-sm'
      }`}
    >
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* Logo */}
        <div className="text-2xl font-bold text-primary">
          아이디어키
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex gap-8">
          {navItems.map((item, index) => (
            <div 
              key={index}
              className="relative"
              onMouseEnter={() => setActiveMenu(index)}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button className="flex items-center gap-1 text-gray-700 hover:text-primary font-medium">
                {item.title}
                <ChevronDown size={16} />
              </button>
              
              {/* Submenu */}
              {activeMenu === index && (
                <div className="absolute top-full left-0 mt-2 w-48 bg-white shadow-lg rounded-lg py-2">
                  {item.submenu.map((subItem, subIndex) => (
                    <a 
                      key={subIndex}
                      href="#"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-50 hover:text-primary"
                    >
                      {subItem}
                    </a>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Mobile Menu Button */}
        <button 
          className="md:hidden"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X /> : <Menu />}
        </button>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t">
          {navItems.map((item, index) => (
            <div key={index} className="border-b">
              <button className="w-full px-6 py-3 text-left flex justify-between items-center">
                {item.title}
                <ChevronDown size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </header>
  )
}
