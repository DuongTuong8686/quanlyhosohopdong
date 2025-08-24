'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Scanner from '@/components/Scanner'
import Features from '@/components/Features'
import Footer from '@/components/Footer'

export default function Home() {
  const [scannedText, setScannedText] = useState<string>('')

  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <Scanner onTextExtracted={setScannedText} />
      <Features />
      <Footer />
    </main>
  )
} 