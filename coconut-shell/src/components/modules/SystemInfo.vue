<template>
    <div class="panel-module system-info">
        <div class="left-panel">
            <h2>System Information</h2>
            <p>CPU Usage: {{ cpuUsage }}%</p>
            <p>RAM Usage: {{ ramUsage }}%</p>
            <p>Disk Usage: {{ diskUsage }}</p>
        </div>
        <div class="right-panel">
            <button @click="showModal('shutdown')" class="btn btn-shutdown" title="Poweroff computer">Shutdown</button>
            <button @click="showModal('reboot')" class="btn btn-reboot" title="Reboot computer">Reboot</button>
        </div>

        <Modal 
            v-if="modalVisible" 
            :title="modalTitle" 
            :visible="modalVisible" 
            :confirmText="modalConfirmText" 
            :cancelText="'Cancel'" 
            @close="modalVisible = false" 
            @confirm="performAction">
            <p>Are you sure you want to {{ modalAction }} the system?</p>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from './Modal.vue'

const cpuUsage = ref('Loading...')
const ramUsage = ref('Loading...')
const diskUsage = ref('Loading...')
const modalVisible = ref(false)
const modalTitle = ref('')
const modalConfirmText = ref('')
const modalAction = ref('')

const updateSystemInfo = () => {
  fetch('/api/system_info')
    .then((response) => response.json())
    .then((data) => {
      cpuUsage.value = data.cpu_usage
      ramUsage.value = data.ram_usage
      diskUsage.value = data.disk_used
    })
    .catch((error) => console.error('Error fetching system info:', error))
}

const showModal = (action) => {
  modalAction.value = action
  modalTitle.value = action.charAt(0).toUpperCase() + action.slice(1)
  modalConfirmText.value = action.charAt(0).toUpperCase() + action.slice(1)
  modalVisible.value = true
}

const performAction = () => {
  const action = modalAction.value
  const urls = {
    shutdown: '/api/shutdown',
    reboot: '/api/reboot'
  }
  
  fetch(urls[action], { method: 'POST' })
    .then((response) => response.json())
    .then((data) => {
      console.log(`${action.charAt(0).toUpperCase() + action.slice(1)} initiated`)
      modalVisible.value = false
    })
    .catch((error) => {
      console.error(`Error ${action}ing:`, error)
      modalVisible.value = false
    })
}

onMounted(() => {
  updateSystemInfo()
  setInterval(updateSystemInfo, 2000)
})
</script>