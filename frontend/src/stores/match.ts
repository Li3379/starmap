import { defineStore } from 'pinia'
import { ref } from 'vue'

/** 匹配诊断结果 store */
export interface SkillGap {
  skill: string
  importance: 'required' | 'bonus'
  gap_level: '完全缺失' | '部分掌握' | '已掌握'
  learning_path: string[]
}

export interface MatchResult {
  target_position: string
  match_score: number
  matched_skills: string[]
  missing_required: string[]
  missing_bonus: string[]
  skill_gap_detail: SkillGap[]
  overall_assessment: string
  estimated_learning_time: string
}

export const useMatchStore = defineStore('match', () => {
  const result = ref<MatchResult | null>(null)
  const loading = ref(false)

  async function runMatch(targetPosition: string, skillNames: string[]) {
    loading.value = true
    try {
      const resp = await fetch('/api/v1/match/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_position: targetPosition, skills: skillNames }),
      })
      const data = await resp.json()
      result.value = data as MatchResult
    } finally {
      loading.value = false
    }
  }

  return { result, loading, runMatch }
})
