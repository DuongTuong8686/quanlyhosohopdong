# CDS Document Scanner

Website scan và trích xuất dữ liệu từ giấy với giao diện hiện đại và công nghệ OCR tiên tiến.

## 🌟 Tính năng chính

- **OCR Thông minh**: Hỗ trợ tiếng Việt và tiếng Anh với độ chính xác lên đến 99%
- **Bảo mật tuyệt đối**: Dữ liệu được xử lý hoàn toàn trên trình duyệt
- **Xử lý nhanh chóng**: Trích xuất text trong vài giây
- **Đa dạng định dạng**: Hỗ trợ JPEG, PNG, BMP, TIFF
- **Responsive Design**: Tối ưu cho mọi thiết bị
- **Xuất dữ liệu linh hoạt**: Copy, download text

## 🚀 Công nghệ sử dụng

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS
- **OCR Engine**: Tesseract.js
- **UI Components**: Lucide React Icons
- **File Upload**: React Dropzone

## 📦 Cài đặt

1. **Clone repository**
```bash
git clone <repository-url>
cd cds-document-scanner
```

2. **Cài đặt dependencies**
```bash
npm install
# hoặc
yarn install
```

3. **Chạy development server**
```bash
npm run dev
# hoặc
yarn dev
```

4. **Mở trình duyệt**
```
http://localhost:3000
```

## 🏗️ Build Production

```bash
npm run build
npm start
```

## 📁 Cấu trúc dự án

```
cds-document-scanner/
├── app/                    # Next.js App Router
│   ├── globals.css        # CSS toàn cục
│   ├── layout.tsx         # Layout chính
│   └── page.tsx           # Trang chủ
├── components/             # React components
│   ├── Header.tsx         # Header navigation
│   ├── Hero.tsx           # Hero section
│   ├── Scanner.tsx        # Scanner component chính
│   ├── Features.tsx       # Features section
│   └── Footer.tsx         # Footer
├── public/                 # Static files
├── package.json            # Dependencies
├── tailwind.config.js      # Tailwind CSS config
├── next.config.js          # Next.js config
└── tsconfig.json           # TypeScript config
```

## 🎨 Giao diện

Website sử dụng **màu xanh lá** làm chủ đạo với thiết kế hiện đại, responsive và thân thiện người dùng.

### Màu sắc chính:
- **Primary**: Xanh lá (#22c55e)
- **Secondary**: Xám (#64748b)
- **Background**: Xám nhạt (#f8fafc)

## 🔧 Sử dụng

1. **Upload hình ảnh**: Kéo thả hoặc click để chọn file hình ảnh
2. **Xử lý OCR**: Click "Trích xuất text" để bắt đầu xử lý
3. **Kết quả**: Xem text được trích xuất
4. **Xuất dữ liệu**: Copy text hoặc download file

## 📱 Responsive

Website được thiết kế responsive hoàn toàn, tối ưu cho:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (< 768px)

## 🌐 Hỗ trợ ngôn ngữ

- **Tiếng Việt**: Hỗ trợ đầy đủ dấu tiếng Việt
- **Tiếng Anh**: Hỗ trợ tiếng Anh chuẩn
- **Giao diện**: 100% tiếng Việt

## 🔒 Bảo mật

- Dữ liệu được xử lý hoàn toàn trên thiết bị người dùng
- Không gửi dữ liệu lên server bên ngoài
- Không lưu trữ thông tin cá nhân

## 📄 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Liên hệ

- **Email**: info@cdsscanner.com
- **Website**: https://cdsscanner.com
- **Địa chỉ**: Hà Nội, Việt Nam

---

**CDS Scanner** - Giải pháp scan dữ liệu thông minh cho người Việt Nam 🇻🇳 