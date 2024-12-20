<template>
  <h1>订阅端</h1>
  <el-button @click="router.push('/home')">主页</el-button>
  <el-button @click="router.push('/pub')">发布端</el-button>
</template>

<script setup lang='ts'>
import {useRouter} from 'vue-router'

const router = useRouter()
</script>

<style scoped lang='css'>
</style>
