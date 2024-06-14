<template>
	<div class="panel-module">
		<div class="left-panel">
			<h2>System Information</h2>
			<p>CPU Usage: {{ cpuUsage }}%</p>
			<p>RAM Usage: {{ ramUsage }}%</p>
			<p>Disk Usage: {{ diskUsage }}</p>
		</div>
		<div class="right-panel">
			<button @click="shutdown" class="btn btn-shutdown" title="Poweroff computer">Shutdown</button>
			<button @click="reboot" class="btn btn-reboot" title="Reboot computer">Reboot</button>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cpuUsage = ref('Loading...')
const ramUsage = ref('Loading...')
const diskUsage = ref('Loading...')

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

const shutdown = () => {
	fetch('/api/shutdown', { method: 'POST' })
		.then((response) => response.json())
		.then((data) => console.log('Shutdown initiated'))
		.catch((error) => console.error('Error shutting down:', error))
}

const reboot = () => {
	fetch('/api/reboot', { method: 'POST' })
		.then((response) => response.json())
		.then((data) => console.log('Reboot initiated'))
		.catch((error) => console.error('Error rebooting:', error))
}

onMounted(() => {
	updateSystemInfo()
	setInterval(updateSystemInfo, 2000)
})
</script>
