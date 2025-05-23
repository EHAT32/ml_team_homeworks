import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export function useTranslation() {
  const sourceText = ref('')
  const translatedText = ref('')
  const sourceLanguage = ref('en')
  const targetLanguage = ref('es')
  const isLoading = ref(false)
  const error = ref(null)

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' }
  ]

  const translate = async () => {
    if (!sourceText.value) {
      translatedText.value = ''
      return
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: sourceText.value,
          source_language: sourceLanguage.value,
          target_language: targetLanguage.value
        })
      })

      if (!response.ok) {
        throw new Error('Translation request failed')
      }

      const data = await response.json()
      translatedText.value = data.translated_text
    } catch (err) {
      error.value = 'Translation failed. Please try again.'
      console.error('Translation error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const swapLanguages = () => {
    const temp = sourceLanguage.value
    sourceLanguage.value = targetLanguage.value
    targetLanguage.value = temp
    const tempText = sourceText.value
    sourceText.value = translatedText.value
    translatedText.value = tempText
  }

  const watchTranslation = () => {
    translate()
  }

  return {
    sourceText,
    translatedText,
    sourceLanguage,
    targetLanguage,
    languages,
    isLoading,
    error,
    translate,
    swapLanguages,
    watchTranslation
  }
} 