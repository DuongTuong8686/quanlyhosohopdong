'use client'

import { useState } from 'react'
import { Menu, X, Scan } from 'lucide-react'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <Scan className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">CDS Scanner</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="text-gray-600 hover:text-primary-600 transition-colors">
              Trang chủ
            </a>
            <a href="#features" className="text-gray-600 hover:text-primary-600 transition-colors">
              Tính năng
            </a>
            <a href="#about" className="text-gray-600 hover:text-primary-600 transition-colors">
              Giới thiệu
            </a>
            <a href="#contact" className="text-gray-600 hover:text-primary-600 transition-colors">
              Liên hệ
            </a>
          </nav>

          {/* CTA Button */}
          <div className="hidden md:block">
            <button className="btn-primary">
              Bắt đầu scan
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-primary-600"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-100">
              <a href="#home" className="block px-3 py-2 text-gray-600 hover:text-primary-600">
                Trang chủ
              </a>
              <a href="#features" className="block px-3 py-2 text-gray-600 hover:text-primary-600">
                Tính năng
              </a>
              <a href="#about" className="block px-3 py-2 text-gray-600 hover:text-primary-600">
                Giới thiệu
              </a>
              <a href="#contact" className="block px-3 py-2 text-gray-600 hover:text-primary-600">
                Liên hệ
              </a>
              <div className="pt-4">
                <button className="btn-primary w-full">
                  Bắt đầu scan
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  )
} 