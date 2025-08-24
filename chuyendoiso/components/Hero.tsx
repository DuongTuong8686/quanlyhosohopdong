'use client'

import { Scan, FileText, Download, Zap } from 'lucide-react'

export default function Hero() {
  return (
    <section id="home" className="relative bg-gradient-to-br from-primary-500 to-primary-700 text-white overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
        <div className="text-center">
          {/* Main Heading */}
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Scan dữ liệu từ giấy
            <span className="block text-primary-200">một cách thông minh</span>
          </h1>
          
          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto leading-relaxed">
            Website hỗ trợ scan ảnh tài liệu và trích xuất văn bản tự động bằng AI.
            Liên hệ: 0818 442 335 • Email: Hungmine2k5@gmail.com
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <button className="btn-primary bg-white text-primary-600 hover:bg-gray-100 px-8 py-4 text-lg">
              <Scan className="w-5 h-5 mr-2 inline" />
              Bắt đầu scan ngay
            </button>
            <button className="btn-secondary border-white text-white hover:bg-white hover:text-primary-600 px-8 py-4 text-lg">
              <FileText className="w-5 h-5 mr-2 inline" />
              Xem demo
            </button>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="w-8 h-8 text-primary-200" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Nhanh chóng</h3>
              <p className="text-primary-200">Scan và xử lý trong vài giây</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-primary-200" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Chính xác</h3>
              <p className="text-primary-200">Độ chính xác OCR lên đến 99%</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Download className="w-8 h-8 text-primary-200" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Dễ dàng</h3>
              <p className="text-primary-200">Xuất dữ liệu nhiều định dạng</p>
            </div>
          </div>
        </div>
      </div>

      {/* Wave Separator */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg className="w-full h-16 text-gray-50" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="currentColor"></path>
          <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,25.13,69.15,56.53C1000.67,96.58,1040.34,96.74,1200,97.81V0Z" opacity=".5" fill="currentColor"></path>
          <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" fill="currentColor"></path>
        </svg>
      </div>
    </section>
  )
} 