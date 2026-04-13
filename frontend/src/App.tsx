import { useState, useCallback, useEffect, useRef } from 'react'
import { useDropzone } from 'react-dropzone'
import toast, { Toaster } from 'react-hot-toast'
import {
  Upload, FileText, X, Send, MessageSquare, Sparkles,
  ChevronRight, Download, RotateCcw, Bot, User,
  FileSearch, CheckCircle2, AlertCircle, MoreHorizontal
} from 'lucide-react'

// ---------- Types ----------
interface SchemaField {
  field: string
  type: 'number' | 'text' | 'date' | 'percentage'
  description: string
}

interface ExtractionResult {
  field: string
  value: string
  confidence: number
  page: number
  source_text: string
}

interface ExtractResponse {
  results: ExtractionResult[]
  extraction_id: string
  processing_time_seconds: number
  filename: string
  model?: string
  tokens_input?: number
  tokens_output?: number
  tokens_total?: number
}

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

interface ChatResponse {
  response: string
  model: string
  tokens_input: number
  tokens_output: number
}

// ---------- Data ----------
const PREDEFINED_SCHEMAS: Record<string, { name: string; fields: SchemaField[] }> = {
  balance_general: {
    name: 'Balance General',
    fields: [
      { field: 'Total Activos', type: 'number', description: 'Suma total de todos los activos' },
      { field: 'Activos Corrientes', type: 'number', description: 'Activos < 1 año' },
      { field: 'Activos No Corrientes', type: 'number', description: 'Activos de largo plazo' },
      { field: 'Efectivo y Equivalentes', type: 'number', description: 'Caja y bancos' },
      { field: 'Cuentas por Cobrar', type: 'number', description: 'Deudas de clientes' },
      { field: 'Total Pasivos', type: 'number', description: 'Suma total de obligaciones' },
      { field: 'Patrimonio Neto', type: 'number', description: 'Activos menos pasivos' },
      { field: 'Período', type: 'text', description: 'Fecha del estado financiero' },
      { field: 'Moneda', type: 'text', description: 'Moneda (S/, USD, etc.)' },
    ],
  },
  estado_resultados: {
    name: 'Estado de Resultados',
    fields: [
      { field: 'Ingresos Totales', type: 'number', description: 'Ventas netas' },
      { field: 'Costo de Ventas', type: 'number', description: 'Costo de bienes vendidos' },
      { field: 'Utilidad Bruta', type: 'number', description: 'Ingresos - Costos' },
      { field: 'Gastos Operativos', type: 'number', description: 'Administración y ventas' },
      { field: 'Utilidad Neta', type: 'number', description: 'Resultado final' },
      { field: 'Período', type: 'text', description: 'Período cubierto' },
    ],
  },
  flujo_caja: {
    name: 'Flujo de Caja',
    fields: [
      { field: 'Flujo Operativo', type: 'number', description: 'Flujo de efectivo de actividades operativas' },
      { field: 'Flujo de Inversión', type: 'number', description: 'Flujo de efectivo de actividades de inversión' },
      { field: 'Flujo de Financiamiento', type: 'number', description: 'Flujo de efectivo de actividades de financiamiento' },
      { field: 'Variación Neta de Efectivo', type: 'number', description: 'Cambio total en caja durante el período' },
      { field: 'Saldo Inicial de Efectivo', type: 'number', description: 'Caja al inicio del período' },
      { field: 'Saldo Final de Efectivo', type: 'number', description: 'Caja al cierre del período' },
      { field: 'Depreciación y Amortización', type: 'number', description: 'Ajuste no monetario incluido en flujo operativo' },
      { field: 'CAPEX', type: 'number', description: 'Inversión en activos fijos (Capex)' },
      { field: 'Período', type: 'text', description: 'Período cubierto por el estado' },
      { field: 'Moneda', type: 'text', description: 'Moneda del documento (S/, USD, etc.)' },
    ],
  },
}

// ---------- Components ----------
function ConfBar({ value }: { value: number }) {
  const col = value >= 0.85 ? 'var(--green)' : value >= 0.70 ? 'var(--yellow)' : 'var(--red)'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <div style={{ flex: 1, height: '4px', background: 'var(--border)', borderRadius: '2px', overflow: 'hidden' }}>
        <div style={{
          height: '100%', width: `${value * 100}%`,
          background: col, borderRadius: '2px',
          animation: 'barGrow 0.9s ease-out both',
        }} />
      </div>
      <span style={{
        fontFamily: 'var(--font-mono)', fontSize: '11px',
        color: col, minWidth: '34px', textAlign: 'right' as const,
      }}>
        {(value * 100).toFixed(0)}%
      </span>
    </div>
  )
}

const STEP_LABELS = [
  { id: 'upload', label: 'Subir PDF', icon: Upload },
  { id: 'schema', label: 'Definir campos', icon: FileSearch },
  { id: 'results', label: 'Resultados', icon: CheckCircle2 }
] as const

function StepBar({ step }: { step: 'upload' | 'schema' | 'results' }) {
  const idx = step === 'upload' ? 0 : step === 'schema' ? 1 : 2
  return (
    <div style={{ display: 'flex', alignItems: 'center', padding: '24px 0' }}>
      {STEP_LABELS.map((s, i) => {
        const Icon = s.icon
        const isActive = i === idx
        const isDone = i < idx
        return (
          <div key={s.id} style={{ display: 'flex', alignItems: 'center', flex: i < 2 ? 1 : 'none' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0 }}>
              <div style={{
                width: '32px', height: '32px', borderRadius: '8px',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: isDone ? 'var(--green)' : isActive ? 'var(--accent)' : 'var(--bg-card)',
                border: `1.5px solid ${isDone ? 'var(--green)' : isActive ? 'var(--accent)' : 'var(--border)'}`,
                transition: 'all 0.35s ease',
              }}>
                <Icon size={16} color={isDone ? 'var(--bg)' : isActive ? 'var(--bg)' : 'var(--text-muted)'} />
              </div>
              <span style={{
                fontSize: '13px',
                fontWeight: isActive ? '600' : '400',
                color: isActive ? 'var(--text)' : isDone ? 'var(--green)' : 'var(--text-muted)',
                transition: 'color 0.35s ease',
                whiteSpace: 'nowrap' as const,
              }}>{s.label}</span>
            </div>
            {i < 2 && (
              <div style={{
                flex: 1, height: '2px', margin: '0 16px',
                background: isDone ? 'var(--green)' : 'var(--border)',
                transition: 'background 0.5s ease',
              }} />
            )}
          </div>
        )
      })}
    </div>
  )
}

// ---------- Chat Panel Component ----------
function ChatPanel({
  pdfFile,
  pdfBase64,
  isOpen,
  onClose
}: {
  pdfFile: File | null
  pdfBase64: string
  isOpen: boolean
  onClose: () => void
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: '¡Hola! He analizado tu documento. ¿Qué te gustaría saber sobre él? Puedes preguntarme sobre valores específicos, periodos, o pedirme un resumen.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async () => {
    if (!input.trim() || !pdfBase64 || loading) return

    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf_base64: pdfBase64,
          messages: [...messages, { role: 'user', content: userMsg }].slice(-6),
          filename: pdfFile?.name || 'document.pdf'
        })
      })

      if (!res.ok) throw new Error('Error en el chat')

      const data: ChatResponse = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (e: any) {
      toast.error(`Error: ${e.message}`)
      setMessages(prev => [...prev, { role: 'assistant', content: 'Lo siento, hubo un error al procesar tu pregunta. Intenta de nuevo.' }])
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      right: 0, top: 60, bottom: 0,
      width: '380px',
      background: 'var(--bg-card)',
      borderLeft: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 100,
      animation: 'slideIn 0.3s ease'
    }}>
      {/* Header */}
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--bg-elevated)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Bot size={20} color="var(--accent)" />
          <span style={{ fontWeight: 600, fontSize: '14px' }}>Chat con documento</span>
        </div>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '4px' }}>
          <X size={18} color="var(--text-muted)" />
        </button>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflow: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '90%',
            background: m.role === 'user' ? 'var(--accent)' : 'var(--bg-elevated)',
            color: m.role === 'user' ? 'var(--bg)' : 'var(--text)',
            padding: '12px 16px',
            borderRadius: m.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
            fontSize: '13px',
            lineHeight: '1.5'
          }}>
            {m.content}
          </div>
        ))}
        {loading && (
          <div style={{ alignSelf: 'flex-start', display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 16px', background: 'var(--bg-elevated)', borderRadius: '16px 16px 16px 4px' }}>
            <div style={{ width: '14px', height: '14px', border: '2px solid var(--border)', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Pensando...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{ padding: '16px', borderTop: '1px solid var(--border)', background: 'var(--bg-elevated)' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder="Pregunta sobre el documento..."
            disabled={loading}
            style={{
              flex: 1,
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '10px 14px',
              color: 'var(--text)',
              fontSize: '13px',
              outline: 'none'
            }}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            style={{
              background: 'var(--accent)',
              border: 'none',
              borderRadius: '8px',
              padding: '10px 14px',
              cursor: loading ? 'wait' : 'pointer',
              opacity: input.trim() ? 1 : 0.5
            }}
          >
            <Send size={16} color="var(--bg)" />
          </button>
        </div>
        <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', textAlign: 'center' }}>
          Pregunta: "¿Cuál es el total de activos?" o "Resume el documento"
        </p>
      </div>
    </div>
  )
}

// ---------- Grupo Macro Logo ----------
function GrupoMacroLogo({ height = 30 }: { height?: number }) {
  const w = Math.round(height * (180 / 48))
  return (
    <svg width={w} height={height} viewBox="0 0 180 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Grupo Macro">
      <rect x="0" y="2" width="9" height="44" rx="1.5" fill="#2EAD63"/>
      <rect x="13" y="2" width="9" height="44" rx="1.5" fill="#2EAD63"/>
      <rect x="26" y="2" width="9" height="44" rx="1.5" fill="#2EAD63"/>
      <text x="44" y="21" fontFamily="Plus Jakarta Sans, Arial, sans-serif" fontWeight="800" fontSize="17" fill="#2EAD63" letterSpacing="2">GRUPO</text>
      <text x="44" y="42" fontFamily="Plus Jakarta Sans, Arial, sans-serif" fontWeight="800" fontSize="17" fill="#2EAD63" letterSpacing="2">MACRO</text>
    </svg>
  )
}

// ---------- Doc icon SVG ----------
function DocIcon() {
  return (
    <svg width="60" height="76" viewBox="0 0 60 76" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="1" y="1" width="50" height="66" rx="5" fill="var(--bg-elevated)" stroke="var(--border-hi)" strokeWidth="1.5"/>
      {([10,20,30,40,50] as number[]).map((y, i) => (
        <rect key={i} x="8" y={y} width={[36,28,34,22,30][i]} height="2.5" rx="1.25" fill="var(--text-muted)" opacity={0.45}/>
      ))}
      <path d="M36 1 L51 1 L51 15 L36 1" fill="var(--bg-card)"/>
      <path d="M36 1 L51 15" stroke="var(--border-hi)" strokeWidth="1.5"/>
    </svg>
  )
}

// ---------- Main App ----------
export default function App() {
  const [step, setStep] = useState<'upload' | 'schema' | 'results'>('upload')
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [pdfBase64, setPdfBase64] = useState<string>('')
  const [schema, setSchema] = useState<SchemaField[]>(PREDEFINED_SCHEMAS.balance_general.fields)
  const [results, setResults] = useState<ExtractionResult[]>([])
  const [meta, setMeta] = useState<{
    time: number; filename: string
    model?: string; tokensIn?: number; tokensOut?: number; tokensTotal?: number
  } | null>(null)
  const [loading, setLoading] = useState(false)
  const [chatOpen, setChatOpen] = useState(false)
  const [theme, setTheme] = useState<'dark' | 'light'>(
    () => (localStorage.getItem('ocr-theme') as 'dark' | 'light') || 'dark'
  )

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('ocr-theme', theme)
  }, [theme])

  const onDrop = useCallback(async (files: File[]) => {
    if (files[0]) {
      const file = files[0]
      setPdfFile(file)
      // Convertir a base64 para chat y extracción
      const ab = await file.arrayBuffer()
      const bytes = new Uint8Array(ab)
      let binary = ''
      for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i])
      setPdfBase64(btoa(binary))
      setStep('schema')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
  })

  const loadSchema = (key: string) => setSchema([...PREDEFINED_SCHEMAS[key].fields])
  const addField = () => setSchema([...schema, { field: '', type: 'number', description: '' }])
  const updateField = (i: number, key: keyof SchemaField, value: string) => {
    const u = [...schema];(u[i] as any)[key] = value; setSchema(u)
  }
  const removeField = (i: number) => setSchema(schema.filter((_, j) => j !== i))

  const handleExtract = async () => {
    if (!pdfFile || !pdfBase64) return
    setLoading(true)
    try {
      const res = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdf_base64: pdfBase64, schema: schema.filter(f => f.field.trim()), filename: pdfFile.name }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data: ExtractResponse = await res.json()
      setResults(data.results)
      setMeta({
        time: data.processing_time_seconds,
        filename: data.filename,
        model: data.model,
        tokensIn: data.tokens_input,
        tokensOut: data.tokens_output,
        tokensTotal: data.tokens_total,
      })
      setStep('results')
      toast.success(`Extracción completada en ${data.processing_time_seconds}s`)
    } catch (e: any) {
      toast.error(`Error: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  const updateResult = (i: number, value: string) => {
    const u = [...results]; u[i] = { ...u[i], value }; setResults(u)
  }

  const downloadCSV = () => {
    const header = 'Campo,Valor,Confianza,Página\n'
    const rows = results.map(r => `"${r.field}","${r.value}",${(r.confidence * 100).toFixed(0)}%,${r.page}`).join('\n')
    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `extraccion_${meta?.filename || 'eeff'}.csv`; a.click()
  }

  const reset = () => {
    setPdfFile(null)
    setPdfBase64('')
    setResults([])
    setMeta(null)
    setChatOpen(false)
    setStep('upload')
  }

  const avgConf = results.length > 0 ? results.reduce((s, r) => s + r.confidence, 0) / results.length : 0
  const lowConf = results.filter(r => r.confidence < 0.7).length

  // ── shared input style
  const inputBase: React.CSSProperties = {
    width: '100%', background: 'transparent', border: 'none',
    borderBottom: '1px solid var(--border)', padding: '4px 0',
    color: 'var(--text)', fontSize: '13px', fontFamily: 'var(--font-body)',
    outline: 'none', transition: 'border-color 0.2s',
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Toaster
        position="top-right"
        toastOptions={{ style: { background: 'var(--bg-card)', color: 'var(--text)', border: '1px solid var(--border-hi)', fontFamily: 'var(--font-body)', fontSize: '13px' } }}
      />

      {/* ── Header ── */}
      <header style={{ borderBottom: '1px solid var(--border)', height: '60px', display: 'flex', alignItems: 'center', padding: '0 32px', flexShrink: 0 }}>
        <div style={{ maxWidth: '1100px', width: '100%', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>

          {/* Left: Grupo Macro logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <GrupoMacroLogo height={30} />
            <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontFamily: 'var(--font-display)', fontWeight: '700', fontSize: '14px', letterSpacing: '0.04em', color: 'var(--text-sub)' }}>SEIDOR</span>
              <span style={{ color: 'var(--border-hi)', fontSize: '14px' }}>/</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', color: 'var(--accent)', fontWeight: '500' }}>S4-OCR</span>
            </div>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: '10px', letterSpacing: '0.1em', textTransform: 'uppercase' as const,
              padding: '2px 9px', borderRadius: '3px',
              background: 'var(--accent-dim)', border: '1px solid rgba(200,152,64,0.3)', color: 'var(--accent)',
            }}>Hackathon 2026</span>
          </div>

          {/* Right: chat + subtitle + theme toggle */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            {pdfBase64 && (
              <button
                onClick={() => setChatOpen(true)}
                title="Chat con el documento"
                style={{
                  background: chatOpen ? 'var(--accent-dim)' : 'transparent',
                  border: `1px solid ${chatOpen ? 'var(--accent)' : 'var(--border)'}`,
                  borderRadius: '8px',
                  padding: '8px 14px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  color: chatOpen ? 'var(--accent)' : 'var(--text-sub)',
                  fontSize: '13px',
                  fontFamily: 'var(--font-body)',
                  transition: 'all 0.2s',
                }}
              >
                <MessageSquare size={16} />
                <span>Chat</span>
              </button>
            )}
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)' }}>
              Extracción Inteligente · EEFF
            </span>
            <button
              onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}
              title={theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
              onMouseEnter={e => { e.currentTarget.style.background = 'var(--bg-elevated)'; e.currentTarget.style.borderColor = 'var(--border-hi)' }}
              onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.borderColor = 'var(--border)' }}
              style={{
                background: 'transparent', border: '1px solid var(--border)',
                borderRadius: '8px', width: '34px', height: '34px',
                cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '15px', transition: 'all 0.2s', flexShrink: 0,
              }}
            >
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </header>

      {/* ── Chat Panel ── */}
      <ChatPanel
        pdfFile={pdfFile}
        pdfBase64={pdfBase64}
        isOpen={chatOpen}
        onClose={() => setChatOpen(false)}
      />

      {/* ── Main ── */}
      <main style={{
        flex: 1,
        maxWidth: chatOpen ? 'calc(1100px - 380px)' : '1100px',
        width: '100%',
        margin: '0 auto',
        padding: '0 32px 56px',
        transition: 'max-width 0.3s ease'
      }}>
        <StepBar step={step} />

        {/* ── STEP 1: Upload ── */}
        {step === 'upload' && (
          <div className="anim-fade-up">
            {/* Info cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '24px' }}>
              {[
                { icon: FileText, title: 'Sube tu PDF', desc: 'EEFF, contratos, memorias' },
                { icon: Sparkles, title: 'IA extrae datos', desc: 'Automático en segundos' },
                { icon: MessageSquare, title: 'Chat inteligente', desc: 'Pregunta al documento' },
              ].map(({ icon: Icon, title, desc }) => (
                <div key={title} style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border)',
                  borderRadius: '12px',
                  padding: '20px',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px'
                }}>
                  <div style={{
                    width: '40px', height: '40px', borderRadius: '10px',
                    background: 'var(--accent-dim)', display: 'flex', alignItems: 'center', justifyContent: 'center'
                  }}>
                    <Icon size={20} color="var(--accent)" />
                  </div>
                  <div>
                    <p style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>{title}</p>
                    <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{desc}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Drop zone */}
            <div
              {...getRootProps()}
              className="grid-bg"
              style={{
                border: `2px dashed ${isDragActive ? 'var(--accent)' : 'var(--border-hi)'}`,
                borderRadius: '16px',
                padding: '60px 40px',
                textAlign: 'center',
                cursor: 'pointer',
                background: isDragActive ? 'rgba(232,185,96,0.08)' : 'var(--bg-card)',
                boxShadow: isDragActive ? '0 0 0 4px rgba(232,185,96,0.1), inset 0 0 60px rgba(232,185,96,0.03)' : 'none',
                transition: 'all 0.25s ease',
              }}
            >
              <input {...getInputProps()} />
              <div style={{
                width: '80px', height: '80px', borderRadius: '20px',
                background: isDragActive ? 'var(--accent-dim)' : 'var(--bg-elevated)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                margin: '0 auto 24px',
                transition: 'all 0.25s ease'
              }}>
                <Upload size={36} color={isDragActive ? 'var(--accent)' : 'var(--text-muted)'} />
              </div>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '26px', fontWeight: '700', marginBottom: '8px' }}>
                {isDragActive ? '¡Suelta el archivo aquí!' : 'Arrastra tu PDF aquí'}
              </h2>
              <p style={{ fontSize: '14px', color: 'var(--text-sub)', marginBottom: '8px' }}>
                o haz clic para seleccionar un archivo
              </p>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                Formatos: PDF · Tamaño máximo: 10MB
              </p>
            </div>

            {/* Supported types */}
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                Documentos soportados
              </p>
              <div style={{ display: 'inline-flex', gap: '8px', flexWrap: 'wrap' as const, justifyContent: 'center' }}>
                {['Balance General', 'Estado de Resultados', 'Flujo de Caja', 'Contratos', 'Memorias'].map(t => (
                  <span key={t} style={{
                    fontFamily: 'var(--font-mono)', fontSize: '11px',
                    padding: '5px 12px', borderRadius: '6px',
                    background: 'var(--bg-elevated)', border: '1px solid var(--border)', color: 'var(--text-sub)',
                  }}>{t}</span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── STEP 2: Schema ── */}
        {step === 'schema' && (
          <div className="anim-fade-up" style={{ position: 'relative', background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border)', overflow: 'hidden' }}>

            {/* Loading overlay */}
            {loading && (
              <div style={{
                position: 'absolute', inset: 0, background: 'var(--overlay)',
                borderRadius: '15px', zIndex: 10,
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '18px',
              }}>
                <div className="scan-host" style={{ width: '60px', height: '76px' }}>
                  <DocIcon />
                  <div className="scan-line" />
                </div>
                <p style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--accent)', letterSpacing: '0.06em' }}>
                  Procesando con IA...
                </p>
                <p style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)' }}>
                  {schema.filter(f => f.field.trim()).length} campos · {pdfFile?.name}
                </p>
              </div>
            )}

            {/* Card header */}
            <div style={{ padding: '18px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: '700', fontSize: '17px', marginBottom: '5px' }}>
                  ¿Qué datos extraer?
                </h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  <span style={{ color: 'var(--accent)' }}>▸</span>
                  <span>{pdfFile?.name}</span>
                </div>
              </div>
              <button
                onClick={reset}
                onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-hi)'; e.currentTarget.style.color = 'var(--text)' }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-sub)' }}
                style={{ fontSize: '12px', padding: '6px 12px', borderRadius: '6px', border: '1px solid var(--border)', background: 'transparent', color: 'var(--text-sub)', cursor: 'pointer', fontFamily: 'var(--font-body)', transition: 'all 0.2s' }}
              >
                Cambiar PDF
              </button>
            </div>

            {/* Templates */}
            <div style={{ padding: '14px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', letterSpacing: '0.06em', textTransform: 'uppercase' as const, flexShrink: 0 }}>
                Plantilla
              </span>
              {Object.entries(PREDEFINED_SCHEMAS).map(([key, val]) => (
                <button
                  key={key}
                  onClick={() => loadSchema(key)}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.background = 'var(--accent-dim)' }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-sub)'; e.currentTarget.style.background = 'var(--bg-elevated)' }}
                  style={{ fontSize: '12px', padding: '5px 14px', borderRadius: '20px', border: '1px solid var(--border)', background: 'var(--bg-elevated)', color: 'var(--text-sub)', cursor: 'pointer', fontFamily: 'var(--font-body)', transition: 'all 0.2s' }}
                >
                  {val.name}
                </button>
              ))}
            </div>

            {/* Table */}
            <div style={{ overflowX: 'auto' as const }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' as const }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}>
                    {['Campo a extraer', 'Tipo', 'Descripción (contexto para la IA)', ''].map((h, i) => (
                      <th key={i} style={{ padding: '10px 16px', textAlign: 'left' as const, fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)', textTransform: 'uppercase' as const, letterSpacing: '0.06em', fontWeight: '500', background: 'var(--bg-elevated)' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {schema.map((f, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                      <td style={{ padding: '10px 16px', width: '26%' }}>
                        <input
                          value={f.field}
                          onChange={e => updateField(i, 'field', e.target.value)}
                          placeholder="ej: Total Activos"
                          onFocus={e => { e.currentTarget.style.borderBottomColor = 'var(--accent)' }}
                          onBlur={e => { e.currentTarget.style.borderBottomColor = 'var(--border)' }}
                          style={inputBase}
                        />
                      </td>
                      <td style={{ padding: '10px 16px', width: '15%' }}>
                        <select
                          value={f.type}
                          onChange={e => updateField(i, 'type', e.target.value)}
                          style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 10px', color: 'var(--text-sub)', fontSize: '12px', fontFamily: 'var(--font-mono)', outline: 'none', cursor: 'pointer' }}
                        >
                          <option value="number">número</option>
                          <option value="text">texto</option>
                          <option value="date">fecha</option>
                          <option value="percentage">porcentaje</option>
                        </select>
                      </td>
                      <td style={{ padding: '10px 16px' }}>
                        <input
                          value={f.description}
                          onChange={e => updateField(i, 'description', e.target.value)}
                          placeholder="Ayuda a la IA a encontrar este dato..."
                          onFocus={e => { e.currentTarget.style.borderBottomColor = 'var(--accent)' }}
                          onBlur={e => { e.currentTarget.style.borderBottomColor = 'var(--border)' }}
                          style={{ ...inputBase, color: 'var(--text-sub)' }}
                        />
                      </td>
                      <td style={{ padding: '10px 16px', width: '44px' }}>
                        <button
                          onClick={() => removeField(i)}
                          onMouseEnter={e => { e.currentTarget.style.color = 'var(--red)' }}
                          onMouseLeave={e => { e.currentTarget.style.color = 'var(--text-muted)' }}
                          style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: '18px', lineHeight: '1', transition: 'color 0.2s', padding: 0 }}
                        >×</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Card footer */}
            <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <button
                onClick={addField}
                onMouseEnter={e => { e.currentTarget.style.color = 'var(--accent)' }}
                onMouseLeave={e => { e.currentTarget.style.color = 'var(--text-sub)' }}
                style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '13px', color: 'var(--text-sub)', fontFamily: 'var(--font-body)', display: 'flex', alignItems: 'center', gap: '6px', transition: 'color 0.2s' }}
              >
                <span style={{ fontSize: '17px', lineHeight: '1', marginTop: '-1px' }}>+</span> Agregar campo
              </button>
              <button
                onClick={handleExtract}
                disabled={loading || schema.filter(f => f.field.trim()).length === 0}
                style={{
                  background: 'var(--accent)', color: 'var(--bg)', border: 'none', borderRadius: '8px',
                  padding: '10px 24px', fontWeight: '700', fontSize: '13px', fontFamily: 'var(--font-body)',
                  cursor: loading ? 'wait' : 'pointer', display: 'flex', alignItems: 'center', gap: '8px',
                  opacity: schema.filter(f => f.field.trim()).length === 0 ? 0.35 : 1,
                  letterSpacing: '0.02em', transition: 'opacity 0.2s',
                }}
              >
                {loading
                  ? <><div className="anim-spin" style={{ width: '14px', height: '14px', border: '2px solid rgba(5,8,15,0.3)', borderTopColor: 'var(--bg)', borderRadius: '50%' }} /> Extrayendo...</>
                  : <><span>⚡</span> Extraer con IA</>
                }
              </button>
            </div>
          </div>
        )}

        {/* ── STEP 3: Results ── */}
        {step === 'results' && (
          <div className="anim-fade-up" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {/* Stats row */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '16px' }}>
              {[
                { label: 'Campos extraídos', val: String(results.length), unit: 'campos', col: 'var(--green)' },
                { label: 'Tiempo de proceso', val: meta?.time?.toFixed(1) ?? '—', unit: 'segundos', col: 'var(--accent)' },
                { label: 'Confianza promedio', val: `${(avgConf * 100).toFixed(0)}`, unit: '%', col: avgConf >= 0.80 ? 'var(--green)' : avgConf >= 0.65 ? 'var(--yellow)' : 'var(--red)' },
              ].map(({ label, val, unit, col }) => (
                <div key={label} style={{ background: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border)', padding: '20px 24px' }}>
                  <p style={{ fontSize: '10px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', textTransform: 'uppercase' as const, letterSpacing: '0.09em', marginBottom: '10px' }}>{label}</p>
                  <p style={{ fontFamily: 'var(--font-display)', fontSize: '36px', fontWeight: '800', color: col, lineHeight: '1' }}>{val}</p>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '5px', fontFamily: 'var(--font-mono)' }}>{unit}</p>
                </div>
              ))}
            </div>

            {/* Cost strip — executive view */}
            {meta?.tokensTotal != null && meta.tokensTotal > 0 && (() => {
              const cost = ((meta.tokensIn ?? 0) / 1_000_000) * 2.50 + ((meta.tokensOut ?? 0) / 1_000_000) * 10.00
              const costStr = cost < 0.0001 ? '< $0.0001' : `$${cost.toFixed(4)}`
              return (
                <div style={{
                  display: 'flex', alignItems: 'center', gap: '0',
                  background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: '10px',
                  overflow: 'hidden',
                }}>
                  {/* Model pill */}
                  <div style={{
                    padding: '12px 18px', borderRight: '1px solid var(--border)',
                    display: 'flex', flexDirection: 'column' as const, gap: '3px', flexShrink: 0,
                  }}>
                    <span style={{ fontFamily: 'var(--font-body)', fontSize: '10px', color: 'var(--text-muted)', letterSpacing: '0.05em', textTransform: 'uppercase' as const }}>Modelo IA</span>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '13px', fontWeight: '600',
                      color: '#4A9AFF', letterSpacing: '0.02em',
                    }}>{meta.model ?? 'gpt-4o'}</span>
                  </div>

                  {/* Cost hero */}
                  <div style={{
                    padding: '12px 24px', flex: 1,
                    display: 'flex', alignItems: 'center', gap: '16px',
                  }}>
                    <div>
                      <p style={{ fontFamily: 'var(--font-body)', fontSize: '11px', color: 'var(--text-muted)', marginBottom: '3px' }}>
                        Costo de esta extracción
                      </p>
                      <p style={{ fontFamily: 'var(--font-display)', fontSize: '22px', fontWeight: '800', color: 'var(--accent)', lineHeight: '1' }}>
                        {costStr} <span style={{ fontSize: '13px', fontWeight: '500', color: 'var(--text-sub)' }}>USD</span>
                      </p>
                    </div>

                  </div>
                </div>
              )
            })()}

            {/* Results table card */}
            <div style={{ background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border)', overflow: 'hidden' }}>
              <div style={{ padding: '16px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: '600', fontSize: '15px' }}>Datos extraídos</h3>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)', padding: '2px 9px', borderRadius: '3px', background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}>
                    {meta?.filename}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    onClick={downloadCSV}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-hi)'; e.currentTarget.style.color = 'var(--text)' }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-sub)' }}
                    style={{ fontSize: '12px', padding: '7px 14px', borderRadius: '8px', border: '1px solid var(--border)', background: 'transparent', color: 'var(--text-sub)', cursor: 'pointer', fontFamily: 'var(--font-body)', transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: '6px' }}
                  >
                    ↓ Exportar CSV
                  </button>
                  <button
                    onClick={reset}
                    style={{ fontSize: '12px', padding: '7px 14px', borderRadius: '8px', border: 'none', background: 'var(--accent)', color: 'var(--bg)', cursor: 'pointer', fontFamily: 'var(--font-body)', fontWeight: '700', letterSpacing: '0.02em' }}
                  >
                    + Nueva extracción
                  </button>
                </div>
              </div>

              <table style={{ width: '100%', borderCollapse: 'collapse' as const }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}>
                    {['Campo', 'Valor extraído', 'Confianza', 'Pág.', 'Texto fuente'].map((h, i) => (
                      <th key={i} style={{ padding: '10px 16px', textAlign: 'left' as const, fontSize: '10px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)', textTransform: 'uppercase' as const, letterSpacing: '0.07em', fontWeight: '500', background: 'var(--bg-elevated)' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {results.map((r, i) => (
                    <tr
                      key={i}
                      style={{ borderBottom: '1px solid var(--border)', transition: 'background 0.15s' }}
                      onMouseEnter={e => { (e.currentTarget as HTMLTableRowElement).style.background = 'var(--bg-elevated)' }}
                      onMouseLeave={e => { (e.currentTarget as HTMLTableRowElement).style.background = 'transparent' }}
                    >
                      <td style={{ padding: '13px 16px', fontWeight: '500', fontSize: '13px', whiteSpace: 'nowrap' as const, width: '18%' }}>{r.field}</td>
                      <td style={{ padding: '13px 16px', width: '22%' }}>
                        <input
                          value={r.value}
                          onChange={e => updateResult(i, e.target.value)}
                          onFocus={e => { e.currentTarget.style.borderBottomColor = 'var(--accent)' }}
                          onBlur={e => { e.currentTarget.style.borderBottomColor = 'var(--border)' }}
                          style={{ background: 'transparent', border: 'none', borderBottom: '1px solid var(--border)', color: 'var(--text)', fontFamily: 'var(--font-mono)', fontSize: '13px', padding: '3px 0', width: '100%', outline: 'none', transition: 'border-color 0.2s' }}
                        />
                      </td>
                      <td style={{ padding: '13px 16px', width: '22%' }}>
                        <ConfBar value={r.confidence} />
                      </td>
                      <td style={{ padding: '13px 16px', fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--text-muted)', width: '5%' }}>{r.page}</td>
                      <td style={{ padding: '13px 16px', maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' as const, fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{r.source_text}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Low confidence warning */}
            {lowConf > 0 && (
              <div style={{ padding: '14px 20px', borderRadius: '10px', border: '1px solid rgba(255,107,107,0.3)', background: 'var(--red-dim)', display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                <span style={{ fontSize: '15px', flexShrink: 0, marginTop: '1px' }}>⚠</span>
                <div>
                  <p style={{ fontWeight: '600', fontSize: '13px', color: 'var(--red)', marginBottom: '3px' }}>
                    {lowConf} campo{lowConf > 1 ? 's' : ''} con baja confianza
                  </p>
                  <p style={{ fontSize: '12px', color: 'var(--text-sub)' }}>
                    Revisa manualmente los valores marcados en rojo — la IA no encontró estos datos con certeza suficiente.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* ── Footer ── */}
      <footer style={{ borderTop: '1px solid var(--border)', padding: '14px 32px', flexShrink: 0 }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)' }}>
            SEIDOR IA Lab · Hackathon Grupo Macro Perú 2026
          </span>
          <div style={{ display: 'flex', gap: '20px' }}>
            {['mauro.hernandez@seidor.com', 'arvinder.ludhiarich@seidor.com'].map(email => (
              <a
                key={email}
                href={`mailto:${email}`}
                onMouseEnter={e => { e.currentTarget.style.color = 'var(--text-sub)' }}
                onMouseLeave={e => { e.currentTarget.style.color = 'var(--text-muted)' }}
                style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s' }}
              >{email}</a>
            ))}
          </div>
        </div>
      </footer>
    </div>
  )
}
