'use client'

import { Scan, Shield, Zap, FileText, Download, Globe, Smartphone, BarChart3 } from 'lucide-react'

const features = [
  {
    icon: Scan,
    title: 'OCR Thông minh',
    description: 'Công nghệ OCR tiên tiến hỗ trợ tiếng Việt và tiếng Anh với độ chính xác lên đến 99%',
    color: 'primary'
  },
  {
    icon: Shield,
    title: 'Bảo mật dữ liệu',
    description: 'Dữ liệu của bạn được xử lý hoàn toàn trên trình duyệt, không gửi lên server bên ngoài',
    color: 'green'
  },
  {
    icon: Zap,
    title: 'Xử lý nhanh chóng',
    description: 'Trích xuất text trong vài giây với tối ưu hóa hiệu suất cao',
    color: 'yellow'
  },
  {
    icon: FileText,
    title: 'Đa dạng định dạng',
    description: 'Hỗ trợ nhiều loại tài liệu: báo cáo, hợp đồng, biểu mẫu, chứng từ...',
    color: 'blue'
  },
  {
    icon: Download,
    title: 'Xuất dữ liệu linh hoạt',
    description: 'Tải xuống kết quả dưới dạng text, PDF hoặc copy vào clipboard',
    color: 'purple'
  },
  {
    icon: Globe,
    title: 'Hỗ trợ đa ngôn ngữ',
    description: 'Nhận diện và xử lý chính xác cả tiếng Việt có dấu và tiếng Anh',
    color: 'indigo'
  },
  {
    icon: Smartphone,
    title: 'Responsive Design',
    description: 'Giao diện tối ưu cho mọi thiết bị từ desktop đến mobile',
    color: 'pink'
  },
  {
    icon: BarChart3,
    title: 'Thống kê chi tiết',
    description: 'Theo dõi số lượng tài liệu đã xử lý và độ chính xác trích xuất',
    color: 'orange'
  }
]

const colorClasses = {
  primary: 'bg-primary-100 text-primary-600',
  green: 'bg-green-100 text-green-600',
  yellow: 'bg-yellow-100 text-yellow-600',
  blue: 'bg-blue-100 text-blue-600',
  purple: 'bg-purple-100 text-purple-600',
  indigo: 'bg-indigo-100 text-indigo-600',
  pink: 'bg-pink-100 text-pink-600',
  orange: 'bg-orange-100 text-orange-600'
}

export default function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Tính năng nổi bật
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Khám phá những tính năng mạnh mẽ giúp việc scan và trích xuất dữ liệu 
            trở nên đơn giản và hiệu quả hơn bao giờ hết
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="group">
              <div className="card hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1">
                <div className={`w-16 h-16 rounded-xl flex items-center justify-center mb-6 ${colorClasses[feature.color as keyof typeof colorClasses]}`}>
                  <feature.icon className="w-8 h-8" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Info */}
        <div className="mt-20 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Tại sao chọn CDS Scanner?
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">Miễn phí hoàn toàn</h4>
                  <p className="text-gray-600">Không giới hạn số lượng tài liệu, không yêu cầu đăng ký</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">Bảo mật tuyệt đối</h4>
                  <p className="text-gray-600">Dữ liệu được xử lý hoàn toàn trên thiết bị của bạn</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">Độ chính xác cao</h4>
                  <p className="text-gray-600">Sử dụng AI và machine learning để cải thiện độ chính xác</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-8 text-white">
            <h4 className="text-2xl font-bold mb-4">Thống kê ấn tượng</h4>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <span className="text-primary-100">Độ chính xác OCR</span>
                <span className="text-3xl font-bold">99%</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-primary-100">Thời gian xử lý</span>
                <span className="text-3xl font-bold">&lt;5s</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-primary-100">Ngôn ngữ hỗ trợ</span>
                <span className="text-3xl font-bold">2+</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-primary-100">Định dạng file</span>
                <span className="text-3xl font-bold">5+</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
} 