<script setup lang="ts">
// 主布局：顶部导航 + 内容区
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <el-container style="height: 100vh">
    <el-header style="background: #001529; display: flex; align-items: center">
      <span style="color: #fff; font-size: 20px; font-weight: bold; margin-right: 40px">
        ★ 星图 StarMap
      </span>
      <el-menu
        :default-active="route.path"
        mode="horizontal"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
      >
        <el-menu-item index="/">全景图谱</el-menu-item>
        <el-menu-item index="/match">匹配诊断</el-menu-item>
        <el-menu-item index="/evolution">演化看板</el-menu-item>
        <el-menu-item index="/quality">图谱质量</el-menu-item>
        <el-menu-item index="/admin">管理后台</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <slot />
    </el-main>
  </el-container>
</template>
