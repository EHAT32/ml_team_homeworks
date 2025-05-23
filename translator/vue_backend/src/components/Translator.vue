<script setup>
import { useTranslation } from '../composables/useTranslation'

const {
  sourceText,
  translatedText,
  sourceLanguage,
  targetLanguage,
  languages,
  isLoading,
  error,
  translate,
  swapLanguages
} = useTranslation()

</script>

<template>
  <div class="translate-container">
    <div class="language-selector">
      <div class="language-select-wrapper">
        <select v-model="sourceLanguage" class="language-select">
          <option v-for="lang in languages" :key="lang.code" :value="lang.code">
            {{ lang.name }}
          </option>
        </select>
      </div>
      
      <button @click="swapLanguages" class="swap-button" title="Swap languages">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M7 16V4M7 4L3 8M7 4L11 8M17 8v12M17 20l4-4M17 20l-4-4"/>
        </svg>
      </button>

      <div class="language-select-wrapper">
        <select v-model="targetLanguage" class="language-select">
          <option v-for="lang in languages" :key="lang.code" :value="lang.code">
            {{ lang.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="translate-btn-row">
      <button class="translate-btn" @click="translate" :disabled="isLoading || !sourceText">
        {{ isLoading ? 'Translating...' : 'Translate' }}
      </button>
    </div>
    <div class="translation-boxes">
      <div class="text-box">
        <div class="text-box-header">
          <span class="language-name">{{ languages.find(l => l.code === sourceLanguage)?.name }}</span>
        </div>
        <textarea
          v-model="sourceText"
          placeholder="Enter text"
          class="text-area"
          :disabled="isLoading"
        ></textarea>
      </div>

      <div class="text-box">
        <div class="text-box-header">
          <span class="language-name">{{ languages.find(l => l.code === targetLanguage)?.name }}</span>
        </div>
        <div v-if="isLoading" class="loading-indicator">
          <div class="loading-spinner"></div>
          <span>Translating...</span>
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <textarea
          v-model="translatedText"
          placeholder="Translation"
          class="text-area"
          readonly
        ></textarea>
      </div>
    </div>
  </div>
</template>

<style scoped>
.translate-container {
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.language-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
  width: 100%;
}

.language-select-wrapper {
  flex: 1;
  max-width: 350px;
}

.language-select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--surface-color);
  color: var(--text-color);
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.language-select:hover {
  border-color: var(--primary-color);
}

.language-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(33, 197, 93, 0.2);
}

.swap-button {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  cursor: pointer;
  padding: 0.75rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: var(--primary-color);
}

.swap-button:hover {
  background-color: var(--hover-color);
  border-color: var(--primary-color);
  color: var(--primary-color-dark);
}

.translate-btn-row {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.translate-btn {
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(33,197,93,0.08);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}

.translate-btn:hover:not(:disabled) {
  background: var(--primary-color-dark);
  color: #fff;
}

.translate-btn:disabled {
  background: var(--border-color);
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

.translation-boxes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  height: calc(100vh - 320px);
  min-height: 400px;
  width: 100vw;
  box-sizing: border-box;
}

.text-box {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  background-color: var(--surface-color);
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.text-box-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--hover-color);
}

.language-name {
  font-weight: 500;
  color: var(--primary-color);
  letter-spacing: 0.5px;
}

.text-area {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: 200px;
  padding: 1rem;
  border: none;
  resize: none;
  font-size: 1rem;
  line-height: 1.5;
  background-color: var(--surface-color);
  color: var(--text-color);
  box-sizing: border-box;
}

.text-area:focus {
  outline: none;
  border: 1px solid var(--primary-color);
}

.text-area:disabled {
  background-color: var(--hover-color);
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

.loading-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(24, 28, 31, 0.95);
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background-color: #2d1517;
  color: #f87171;
  padding: 1rem;
  font-size: 0.9rem;
  text-align: center;
  border-bottom: 1px solid #991b1b;
}

@media (max-width: 768px) {
  .translate-container {
    padding: 0 0.5rem;
    width: 100vw;
  }

  .translation-boxes {
    grid-template-columns: 1fr;
    height: auto;
    gap: 1rem;
    width: 100vw;
  }
  
  .language-selector {
    flex-direction: column;
    align-items: stretch;
    width: 100vw;
  }
  
  .language-select-wrapper {
    max-width: none;
  }
  
  .swap-button {
    align-self: center;
  }

  .text-box {
    height: 300px;
  }
}
</style> 