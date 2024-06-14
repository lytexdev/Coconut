<script setup>
import Header from './Header.vue'
import SystemInfo from './modules/SystemInfo.vue'
import DockerContainers from './modules/Docker.vue'
import Backup from './modules/Backup.vue';
</script>

<template>
    <Header />

    <main class="main-content">
        <SystemInfo />
        <Backup />
        <DockerContainers />
    </main>
</template>
