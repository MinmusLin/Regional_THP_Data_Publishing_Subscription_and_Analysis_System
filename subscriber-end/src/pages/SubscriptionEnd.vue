<template>
  <h1>订阅端</h1>
  <el-button size='large' @click="router.push('/home')">主页</el-button>
  <el-button size='large' @click="router.push('/pub')">发布端</el-button>
  <el-button size='large' @click="toggleSubscription('temperature')">
    {{ isSubscribedToTemperature ? '取消订阅温度数据' : '订阅温度数据' }}
  </el-button>
  <el-button size='large' @click="toggleSubscription('humidity')">
    {{ isSubscribedToHumidity ? '取消订阅湿度数据' : '订阅湿度数据' }}
  </el-button>
  <el-button size='large' @click="toggleSubscription('pressure')">
    {{ isSubscribedToPressure ? '取消订阅气压数据' : '订阅气压数据' }}
  </el-button>
  <el-tabs v-model='activeName'>
    <el-tab-pane label='温度数据' name='temperature'>
      <img v-if='temperatureImageSrc' :src='`data:image/png;base64,${temperatureImageSrc}`' alt='temperatureImage'>
      <el-table :data='temperatureData' style='width: 100%'>
        <el-table-column prop='date' label='日期' width='180'/>
        <el-table-column prop='average' label='平均温度' width='180'/>
        <el-table-column label='查看图片'>
          <template #default='scope'>
            <el-button link type='primary' @click='showImage(scope.row.graph)'>
              数据折线图
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label='湿度数据' name='humidity'>
      <img v-if='humidityImageSrc' :src='`data:image/png;base64,${humidityImageSrc}`' alt='humidityImage'>
      <el-table :data='humidityData' style='width: 100%'>
        <el-table-column prop='date' label='日期' width='180'/>
        <el-table-column prop='average' label='平均湿度' width='180'/>
        <el-table-column label='查看图片'>
          <template #default='scope'>
            <el-button link type='primary' @click='showImage(scope.row.graph)'>
              数据折线图
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label='气压数据' name='pressure'>
      <img v-if='pressureImageSrc' :src='`data:image/png;base64,${pressureImageSrc}`' alt='pressureImage'>
      <el-table :data='pressureData' style='width: 100%'>
        <el-table-column prop='date' label='日期' width='180'/>
        <el-table-column prop='average' label='平均气压' width='180'/>
        <el-table-column label='查看图片'>
          <template #default='scope'>
            <el-button link type='primary' @click='showImage(scope.row.graph)'>
              数据折线图
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>
  <el-dialog v-model='imageDialogVisible' title='数据折线图' width='1200'>
    <img :src='imageSrc' alt='graph' style='width: 100%'/>
  </el-dialog>
</template>

<script setup lang='ts'>
import mqtt from 'mqtt'
import {ref, onMounted, onBeforeUnmount} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'

const router = useRouter()
const client = ref<mqtt.MqttClient | null>(null)
const temperatureData = ref<any[]>([])
const humidityData = ref<any[]>([])
const pressureData = ref<any[]>([])
const isSubscribedToTemperature = ref(false)
const isSubscribedToHumidity = ref(false)
const isSubscribedToPressure = ref(false)
const imageDialogVisible = ref(false)
const imageSrc = ref('')
const activeName = ref('temperature')
const temperatureImageSrc = ref('')
const humidityImageSrc = ref('')
const pressureImageSrc = ref('')

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
    const data = JSON.parse(messageStr)
    if (topic === 'temperature/data') {
      temperatureData.value.push({
        date: data.date,
        average: data.average,
        graph: data.graph
      })
      temperatureImageSrc.value = data.prediction
    } else if (topic === 'humidity/data') {
      humidityData.value.push({
        date: data.date,
        average: data.average,
        graph: data.graph
      })
      humidityImageSrc.value = data.prediction
    } else if (topic === 'pressure/data') {
      pressureData.value.push({
        date: data.date,
        average: data.average,
        graph: data.graph
      })
      pressureImageSrc.value = data.prediction
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

const showImage = (base64Image: string) => {
  imageSrc.value = `data:image/png;base64,${base64Image}`
  imageDialogVisible.value = true
}
</script>
