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

<style scoped lang="scss">
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    padding: 2rem;
}
</style>