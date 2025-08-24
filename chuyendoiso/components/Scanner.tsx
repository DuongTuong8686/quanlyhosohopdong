'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { createWorker } from 'tesseract.js'
import { Upload, FileText, Download, Copy, Check, Loader2 } from 'lucide-react'

interface ScannerProps {
  onTextExtracted: (text: string) => void
}

export default function Scanner({ onTextExtracted }: ScannerProps) {
  const [image, setImage] = useState<string | null>(null)
  const [extractedText, setExtractedText] = useState<string>('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [copied, setCopied] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = () => {
        setImage(reader.result as string)
        setExtractedText('')
      }
      reader.readAsDataURL(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    multiple: false
  })

  const processImage = async () => {
    if (!image) return

    setIsProcessing(true)
    try {
      // tesseract.js v4 API: cần loadLanguage và initialize trước khi recognize
      const worker = await createWorker({
        logger: () => {},
        // Các CDN dự phòng giúp tránh lỗi tải model/worker trong môi trường doanh nghiệp
        workerPath: 'https://cdn.jsdelivr.net/npm/tesseract.js@4.1.1/dist/worker.min.js',
        corePath: 'https://cdn.jsdelivr.net/npm/tesseract.js-core@4.0.2/tesseract-core.wasm.js',
        langPath: 'https://tessdata.projectnaptha.com/4.0.0',
      })

      await worker.loadLanguage('vie+eng')
      await worker.initialize('vie+eng')
      const { data: { text } } = await worker.recognize(image)
      setExtractedText(text)
      onTextExtracted(text)
      await worker.terminate()
    } catch (error: any) {
      console.error('Error processing image:', error)
      const message = error?.message ? `Có lỗi khi xử lý: ${error.message}` : 'Có lỗi xảy ra khi xử lý hình ảnh. Vui lòng thử lại.'
      setExtractedText(message)
    } finally {
      setIsProcessing(false)
    }
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(extractedText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const downloadText = () => {
    const blob = new Blob([extractedText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'extracted-text.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Scan và trích xuất dữ liệu
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload hình ảnh tài liệu và để AI trích xuất text một cách tự động. 
            Hỗ trợ tiếng Việt và tiếng Anh với độ chính xác cao.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Upload Section */}
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Upload hình ảnh
              </h3>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragActive
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                }`}
              >
                <input {...getInputProps()} />
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                {isDragActive ? (
                  <p className="text-primary-600 font-medium">Thả file vào đây...</p>
                ) : (
                  <div>
                    <p className="text-gray-600 mb-2">
                      Kéo thả file hoặc <span className="text-primary-600 font-medium">click để chọn</span>
                    </p>
                    <p className="text-sm text-gray-500">
                      Hỗ trợ: JPEG, PNG, BMP, TIFF
                    </p>
                  </div>
                )}
              </div>

              {image && (
                <div className="mt-6">
                  <img
                    src={image}
                    alt="Uploaded document"
                    className="w-full h-64 object-contain rounded-lg border border-gray-200"
                  />
                  <button
                    onClick={processImage}
                    disabled={isProcessing}
                    className="btn-primary w-full mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                        Đang xử lý...
                      </>
                    ) : (
                      <>
                        <FileText className="w-5 h-5 mr-2" />
                        Trích xuất text
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Kết quả trích xuất
              </h3>
              
              {extractedText ? (
                <div className="space-y-4">
                  <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                    <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
                      {extractedText}
                    </pre>
                  </div>
                  
                  <div className="flex gap-3">
                    <button
                      onClick={copyToClipboard}
                      className="flex-1 btn-secondary flex items-center justify-center"
                    >
                      {copied ? (
                        <>
                          <Check className="w-4 h-4 mr-2" />
                          Đã copy
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4 mr-2" />
                          Copy text
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={downloadText}
                      className="flex-1 btn-primary flex items-center justify-center"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Tải xuống
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                  <p>Kết quả trích xuất sẽ hiển thị ở đây</p>
                </div>
              )}
            </div>

            {/* Tips */}
            <div className="card bg-primary-50 border-primary-200">
              <h4 className="text-lg font-semibold text-primary-800 mb-3">
                💡 Mẹo để có kết quả tốt nhất
              </h4>
              <ul className="text-primary-700 space-y-2 text-sm">
                <li>• Đảm bảo hình ảnh rõ nét và có độ tương phản tốt</li>
                <li>• Tránh bóng mờ và ánh sáng không đều</li>
                <li>• Đặt tài liệu phẳng và thẳng hàng</li>
                <li>• Sử dụng độ phân giải tối thiểu 300 DPI</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
} 