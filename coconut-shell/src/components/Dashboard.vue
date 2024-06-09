<script setup>
import Header from './Header.vue'
import SystemInfo from './modules/SystemInfo.vue'
import DockerContainers from './modules/Docker.vue'
</script>

<template>
    <Header />

    <main class="main-content">
        <SystemInfo />
        <DockerContainers />
    </main>
</template>
