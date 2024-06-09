<script setup>
import { ref, onMounted } from 'vue'

const containers = ref([])

const updateDockerContainers = () => {
  fetch('/api/docker_containers')
    .then((response) => response.json())
    .then((data) => {
      containers.value = data
    })
    .catch((error) => console.error('Error fetching Docker containers:', error))
}

const confirmAction = (action, id) => {
  const actionMessages = {
    start: 'start this container',
    stop: 'stop this container',
    remove: 'remove this container',
  }
  if (confirm(`Are you sure you want to ${actionMessages[action]}?`)) {
    performAction(action, id)
  }
}

const performAction = (action, id) => {
  const urls = {
    start: '/api/docker_start',
    stop: '/api/docker_stop',
    remove: '/api/docker_remove',
  }
  fetch(urls[action], {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: id }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(`Container ${action}ed successfully`)
      updateDockerContainers()
    })
    .catch((error) => console.error(`Error ${action}ing container:`, error))
}

onMounted(() => {
  updateDockerContainers()
  setInterval(updateDockerContainers, 60000)
})
</script>

<template>
  <div class="panel-module">
    <h2>Docker</h2>
    <ul>
      <li v-for="container in containers" :key="container.id">
        <span :class="['status-dot', container.status === 'running' ? 'online' : 'offline']"></span>
        {{ container.name }} - {{ container.image }} - {{ container.status }}
        <button @click="confirmAction('start', container.id)">Start</button>
        <button @click="confirmAction('stop', container.id)">Stop</button>
        <button @click="confirmAction('remove', container.id)">Remove</button>
      </li>
    </ul>
  </div>
</template>