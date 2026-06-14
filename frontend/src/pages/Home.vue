<script setup lang="ts">
// 全景图谱页（Home）— 对应文档 §8.3、模块C（§5.3）
// TODO(W3-W6 流C)：接入 AntV G6 力导向图，节点按类型着色
// TODO(W3-W6)：先用 MSW mock 数据，独立于流B（规范4 Mock优先）
import MainLayout from '@/layouts/MainLayout.vue'
</script>

<template>
  <MainLayout>
    <el-alert
      title="全景图谱（占位）"
      type="info"
      :closable="false"
    >
      W3-W6 流C 实现：AntV G6 力导向图，节点按类型着色（岗位=蓝/技能=绿/工具=橙）。
      支持技术栈视图、级别视图、热度视图、演化视图四种切换。
    </el-alert>
    <div
      ref="graphRef"
      style="width: 100%; height: 70vh; margin-top: 16px; background: #fafafa"
    >
      <!-- G6 图谱挂载点 -->
    </div>
  </MainLayout>
</template>
