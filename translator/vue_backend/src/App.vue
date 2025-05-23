<script setup>
import Translator from './components/Translator.vue'
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>Deep Translate</h1>
    </header>
    <main class="app-main">
      <Translator />
    </main>
  </div>
</template>

<style>
:root {
  --primary-color: #21c55d;
  --primary-color-dark: #16a34a;
  --background-color: #181c1f;
  --surface-color: #23272a;
  --border-color: #2d333b;
  --text-color: #e5e7eb;
  --text-color-secondary: #a1a1aa;
  --hover-color: #1f2428;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, #app {
  width: 100vw !important;
  min-width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--background-color);
  color: var(--text-color);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: var(--surface-color);
  padding: 1rem 0 1rem 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  width: 100vw;
}

.app-header h1 {
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: 600;
  margin-left: 2rem;
  letter-spacing: 1px;
}

.app-main {
  flex: 1;
  width: 100vw;
  padding: 2rem 0 0 0;
  background: var(--background-color);
}
</style>
