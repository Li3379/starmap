<script setup lang="ts">
/**
 * 岗位搜索下拉组件 — 支持搜索过滤 + 预设列表
 * 对应任务文档：匹配诊断第2步
 */
import { ref, onMounted } from 'vue'

const emit = defineEmits<{
  select: [position: string]
}>()

const options = ref<{ label: string; value: string }[]>([])
const selected = ref('')
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const resp = await fetch('/api/v1/positions/search?q=')
    const data = await resp.json()
    options.value = (data.items ?? []).map((p: { name: string }) => ({
      label: p.name,
      value: p.name,
    }))
  } finally {
    loading.value = false
  }
})

async function remoteMethod(q: string) {
  loading.value = true
  try {
    const resp = await fetch(`/api/v1/positions/search?q=${encodeURIComponent(q)}`)
    const data = await resp.json()
    options.value = (data.items ?? []).map((p: { name: string }) => ({
      label: p.name,
      value: p.name,
    }))
  } finally {
    loading.value = false
  }
}

function handleChange(val: string) {
  if (val) emit('select', val)
}
</script>

<template>
  <div class="position-search">
    <el-select
      v-model="selected"
      filterable
      remote
      reserve-keyword
      placeholder="请搜索并选择目标岗位"
      :remote-method="remoteMethod"
      :loading="loading"
      style="width: 100%"
      size="large"
      @change="handleChange"
    >
      <el-option
        v-for="opt in options"
        :key="opt.value"
        :label="opt.label"
        :value="opt.value"
      />
    </el-select>
    <div class="hint">
      输入岗位名称关键词搜索，如"数据分析"、"前端"、"Java"等
    </div>
  </div>
</template>

<style scoped>
.position-search {
  width: 100%;
}

.hint {
  margin-top: 8px;
  font-size: 13px;
  color: #c0c4cc;
}
</style>
