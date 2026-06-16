import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/** 图谱质量数据 store */
export interface QualityMetrics {
  total_nodes: number
  total_edges: number
  avg_trust_score: number
  high_trust_ratio: number
  hallucination_rate: number
  pending_count: number
  weekly_new_nodes: number
  audit_pass_rate: number
  source_distribution: { name: string; count: number; trust: number }[]
  hallucination_trend: { date: string; rate: number }[]
  audit_queue: { id: number; position: string; skill: string; trust: number }[]
  trust_distribution: { range: string; count: number }[]
}

export const useQualityStore = defineStore('quality', () => {
  const metrics = ref<QualityMetrics | null>(null)
  const loading = ref(false)

  async function fetchQuality() {
    loading.value = true
    try {
      const resp = await fetch('/api/v1/quality/metrics')
      const data = await resp.json()
      metrics.value = data as QualityMetrics
    } finally {
      loading.value = false
    }
  }

  const kpiCards = computed(() => {
    if (!metrics.value) return []
    const m = metrics.value
    return [
      { label: '总节点数', value: m.total_nodes, color: '#409eff' },
      { label: '平均信任度', value: m.avg_trust_score.toFixed(1), color: '#67c23a' },
      { label: '幻觉率', value: (m.hallucination_rate * 100).toFixed(1) + '%', color: '#e6a23c' },
      { label: '待审核', value: m.pending_count, color: '#f56c6c' },
    ]
  })

  return { metrics, loading, kpiCards, fetchQuality }
})
