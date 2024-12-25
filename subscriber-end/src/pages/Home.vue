<template>
  <div class='container'>
    <img src='/background1.png' class='background1' alt='Background 1'>
    <img src='/background2.png' class='background2' alt='Background 2'>
    <img src='/background3.png' class='background3' alt='Background 3'>
    <img src='/background4.png' class='background4' alt='Background 4'>
    <img src='/background5.png' class='background5' alt='Background 5'>
    <div class='project-title'>某区域温度 / 湿度 / 气压数据<br>发布订阅及分析处理系统</div>
    <div class='buttons'>
      <button @click="router.push('/pub')" class='subscribe-btn'>发布端</button>
      <button @click="router.push('/sub')" class='publish-btn'>订阅端</button>
    </div>
  </div>
</template>

<script setup lang='ts'>
import {useRouter} from 'vue-router'

const router = useRouter()
</script>

<style scoped lang='css'>
.container {
  position: relative;
  width: 100%;
  height: calc(100vh - 16px);
  overflow: hidden;
}

.background1 {
  position: absolute;
  left: 10%;
  top: -30%;
  width: 500px;
  height: auto;
}

.background2 {
  position: absolute;
  top: 9%;
  left: 34%;
  width: 90px;
  height: auto;
}

.background3 {
  position: absolute;
  top: -17%;
  right: -5%;
  width: 250px;
  height: auto;
}

.background4 {
  position: absolute;
  bottom: -50%;
  left: -10%;
  width: 700px;
  height: auto;
}

.background5 {
  position: absolute;
  top: 10%;
  right: 10%;
  width: 650px;
  height: auto;
}

.project-title {
  position: absolute;
  top: 34%;
  left: 12%;
  font-size: 54px;
  font-weight: bold;
  line-height: 1.75;
  color: #333;
}

.buttons {
  position: absolute;
  top: 65%;
  left: 25%;
  display: flex;
  gap: 80px;
}

.subscribe-btn, .publish-btn {
  padding: 10px 20px;
  font-size: 26px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: rgba(255, 101, 167, 1);
  color: white;
  width: 200px;
}

.subscribe-btn:hover, .publish-btn:hover {
  background-color: rgb(189, 79, 129);
}
</style>
