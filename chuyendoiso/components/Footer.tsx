'use client'

import { Scan, Mail, Phone, MapPin, Github, Linkedin, Twitter } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Scan className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">CDS Scanner</span>
            </div>
            
            <p className="text-gray-300 mb-6 max-w-md">
              CDS Scanner là website giúp bạn scan ảnh tài liệu và trích xuất văn bản tự động
              bằng AI, tối ưu cho tiếng Việt và tiếng Anh. Nhanh, chính xác và dễ sử dụng cho
              học tập, công việc và lưu trữ số.
            </p>
            
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-6">Liên kết nhanh</h3>
            <ul className="space-y-3">
              <li>
                <a href="#home" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Trang chủ
                </a>
              </li>
              <li>
                <a href="#features" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Tính năng
                </a>
              </li>
              <li>
                <a href="#about" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Giới thiệu
                </a>
              </li>
              <li>
                <a href="#contact" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Liên hệ
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-6">Liên hệ</h3>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-primary-400" />
                <a href="mailto:Hungmine2k5@gmail.com" className="text-gray-300 hover:text-primary-300">
                  Hungmine2k5@gmail.com
                </a>
              </div>
              
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-primary-400" />
                <a href="tel:0818442335" className="text-gray-300 hover:text-primary-300">
                  0818 442 335
                </a>
              </div>
              
              <div className="flex items-center space-x-3">
                <MapPin className="w-5 h-5 text-primary-400" />
                <span className="text-gray-300">Hà Nội, Việt Nam</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 CDS Scanner. Tất cả quyền được bảo lưu.
            </p>
            
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Chính sách bảo mật
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Điều khoản sử dụng
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Sitemap
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
} 