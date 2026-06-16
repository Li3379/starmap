import { defineStore } from 'pinia'
import { ref } from 'vue'

/** 简历解析结果 store */
export interface ParsedSkill {
  skill: string
  category: 'hard_skill' | 'soft_skill'
  proficiency: '了解' | '熟悉' | '精通'
}

export interface ResumeParseResult {
  name: string
  skills: ParsedSkill[]
  experience_years: number
  education: string
}

export const useResumeStore = defineStore('resume', () => {
  const result = ref<ResumeParseResult | null>(null)
  const loading = ref(false)

  async function parseResume(file: File) {
    loading.value = true
    const formData = new FormData()
    formData.append('file', file)

    try {
      const resp = await fetch('/api/v1/resume/parse', { method: 'POST', body: formData })
      const data = await resp.json()
      result.value = data as ResumeParseResult
    } finally {
      loading.value = false
    }
  }

  return { result, loading, parseResume }
})
