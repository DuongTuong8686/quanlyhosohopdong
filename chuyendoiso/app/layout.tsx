import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CDS Document Scanner - Scan dữ liệu từ giấy',
  description: 'Website scan và trích xuất dữ liệu từ giấy với công nghệ OCR hiện đại',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  )
} 