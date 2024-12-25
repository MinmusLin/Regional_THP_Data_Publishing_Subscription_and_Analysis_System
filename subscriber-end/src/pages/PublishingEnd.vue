<template>
  <h1>发布端</h1>
  <el-button size='large' @click="router.push('/home')">主页</el-button>
  <el-button size='large' @click="router.push('/sub')">订阅端</el-button>
  <el-button size='large' @click="fetchDataByTopic('temperature')">发布 / 暂停发布温度数据</el-button>
  <el-button size='large' @click="fetchDataByTopic('humidity')">发布 / 暂停发布湿度数据</el-button>
  <el-button size='large' @click="fetchDataByTopic('pressure')">发布 / 暂停发布气压数据</el-button>
  <p>{{ responseData }}</p>
</template>

<script setup lang='ts'>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import axios from 'axios'

const router = useRouter()
const responseData = ref()

function fetchDataByTopic(topic: string) {
  axios.get(`http://122.152.212.194:3000/pub/${topic}`).then((response) => {
    responseData.value = response.data
  }).catch(() => {
    responseData.value = null
  })
}
</script>
