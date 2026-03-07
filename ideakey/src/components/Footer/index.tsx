import { Facebook, Instagram, Youtube } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-navy text-white py-12">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-xl font-bold mb-4">아이디어키</h3>
            <p className="text-gray-300 text-sm">
              디지털 퍼포먼스 마케팅<br />
              전문 광고대행사
            </p>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-bold mb-4">서비스</h4>
            <ul className="space-y-2 text-gray-300 text-sm">
              <li><a href="#" className="hover:text-white">검색 광고</a></li>
              <li><a href="#" className="hover:text-white">디스플레이 광고</a></li>
              <li><a href="#" className="hover:text-white">이커머스 마케팅</a></li>
              <li><a href="#" className="hover:text-white">SNS 마케팅</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold mb-4">CONTACT</h4>
            <ul className="space-y-2 text-gray-300 text-sm">
              <li>서울특별시...</li>
              <li>TEL: 02-1234-5678</li>
              <li>FAX: 02-1234-5679</li>
              <li>Email: info@ideakey.co.kr</li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold mb-4">SOCIAL</h4>
            <div className="flex gap-4">
              <a href="#" className="text-gray-300 hover:text-white">
                <Facebook size={24} />
              </a>
              <a href="#" className="text-gray-300 hover:text-white">
                <Instagram size={24} />
              </a>
              <a href="#" className="text-gray-300 hover:text-white">
                <Youtube size={24} />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>© 2024 아이디어키 All Rights Reserved.</p>
          <p className="mt-2">
            <a href="#" className="hover:text-white mr-4">이용약관</a>
            <a href="#" className="hover:text-white mr-4">개인정보처리방침</a>
            <a href="#" className="hover:text-white">이메일무단수집거부</a>
          </p>
        </div>
      </div>
    </footer>
  )
}
