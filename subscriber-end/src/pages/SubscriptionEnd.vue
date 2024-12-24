<template>
  <h1>订阅端</h1>
  <el-button @click="router.push('/home')">主页</el-button>
  <el-button @click="router.push('/pub')">发布端</el-button>
  <el-button @click="toggleSubscription('temperature')">
    {{ isSubscribedToTemperature ? '取消订阅温度数据' : '订阅温度数据' }}
  </el-button>
  <el-button @click="toggleSubscription('humidity')">
    {{ isSubscribedToHumidity ? '取消订阅湿度数据' : '订阅湿度数据' }}
  </el-button>
  <el-button @click="toggleSubscription('pressure')">
    {{ isSubscribedToPressure ? '取消订阅气压数据' : '订阅气压数据' }}
  </el-button>
  <div>
    <h2>温度数据</h2>
    <div v-for='(message, index) in temperatureData' :key='index'>
      {{ message }}
    </div>
  </div>
  <div>
    <h2>湿度数据</h2>
    <div v-for='(message, index) in humidityData' :key='index'>
      {{ message }}
    </div>
  </div>
  <div>
    <h2>气压数据</h2>
    <div v-for='(message, index) in pressureData' :key='index'>
      {{ message }}
    </div>
  </div>
</template>

<script setup lang='ts'>
import mqtt from 'mqtt'
import {ref, onMounted, onBeforeUnmount} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'

const router = useRouter()
const client = ref<mqtt.MqttClient | null>(null)
const temperatureData = ref<string[]>([])
const humidityData = ref<string[]>([])
const pressureData = ref<string[]>([])
const isSubscribedToTemperature = ref(false)
const isSubscribedToHumidity = ref(false)
const isSubscribedToPressure = ref(false)

const connectToMQTT = () => {
  client.value = mqtt.connect('ws://118.89.72.217:8083', {
    username: 'mqtt_server',
    password: 'mqtt_password',
    clientId: crypto.randomUUID(),
    clean: true
  })
  // noinspection TypeScriptUnresolvedReference
  client.value.on('connect', () => {
    ElMessage.success('MQTT 代理已连接')
  })
  // noinspection TypeScriptUnresolvedReference
  client.value.on('message', (topic, message) => {
    const messageStr = message.toString()
    if (topic === 'temperature/data') {
      temperatureData.value.push(messageStr)
    } else if (topic === 'humidity/data') {
      humidityData.value.push(messageStr)
    } else if (topic === 'pressure/data') {
      pressureData.value.push(messageStr)
    }
  })
  // noinspection TypeScriptUnresolvedReference
  client.value.on('error', (err) => {
    ElMessage.error('MQTT 代理连接错误: ', err)
  })
  // noinspection TypeScriptUnresolvedReference
  client.value.on('close', () => {
    // ElMessage.warning('MQTT 代理连接关闭')
  })
}

const toggleSubscription = (topic: string) => {
  if (!client.value) {
    ElMessage.error('MQTT 代理未连接')
    return
  }
  if (topic === 'temperature') {
    if (isSubscribedToTemperature.value) {
      // noinspection TypeScriptUnresolvedReference
      client.value.unsubscribe('temperature/data', (err) => {
        if (err) {
          ElMessage.error('取消订阅温度数据失败: ', err)
        } else {
          ElMessage.warning('已取消订阅温度数据')
          isSubscribedToTemperature.value = false
        }
      })
    } else {
      // noinspection TypeScriptUnresolvedReference
      client.value.subscribe('temperature/data', {qos: 1}, (err) => {
        if (!err) {
          ElMessage.success('已订阅温度数据')
          isSubscribedToTemperature.value = true
        } else {
          ElMessage.error('订阅温度数据失败: ', err)
        }
      })
    }
  } else if (topic === 'humidity') {
    if (isSubscribedToHumidity.value) {
      // noinspection TypeScriptUnresolvedReference
      client.value.unsubscribe('humidity/data', (err) => {
        if (err) {
          ElMessage.error('取消订阅湿度数据失败: ', err)
        } else {
          ElMessage.warning('已取消订阅湿度数据')
          isSubscribedToHumidity.value = false
        }
      })
    } else {
      // noinspection TypeScriptUnresolvedReference
      client.value.subscribe('humidity/data', {qos: 1}, (err) => {
        if (!err) {
          ElMessage.success('已订阅湿度数据')
          isSubscribedToHumidity.value = true
        } else {
          ElMessage.error('订阅湿度数据失败: ', err)
        }
      })
    }
  } else if (topic === 'pressure') {
    if (isSubscribedToPressure.value) {
      // noinspection TypeScriptUnresolvedReference
      client.value.unsubscribe('pressure/data', (err) => {
        if (err) {
          ElMessage.error('取消订阅气压数据失败: ', err)
        } else {
          ElMessage.warning('已取消订阅气压数据')
          isSubscribedToPressure.value = false
        }
      })
    } else {
      // noinspection TypeScriptUnresolvedReference
      client.value.subscribe('pressure/data', {qos: 1}, (err) => {
        if (!err) {
          ElMessage.success('已订阅气压数据')
          isSubscribedToPressure.value = true
        } else {
          ElMessage.error('订阅气压数据失败: ', err)
        }
      })
    }
  }
}

onMounted(() => {
  connectToMQTT()
})

onBeforeUnmount(() => {
  if (client.value) {
    // noinspection TypeScriptUnresolvedReference
    client.value.end()
  }
})
</script>

<style scoped lang='css'>
</style>
