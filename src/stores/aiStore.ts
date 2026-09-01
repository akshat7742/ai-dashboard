import { ref } from 'vue'

import { defineStore } from 'pinia'

import {
  analyzeDashboard
} from '@/services/aiService'


export const useAiStore =
  defineStore(
    'ai',

    () => {

      // ----------------------------------------------
      // Conversation ID
      // ----------------------------------------------

      const conversationId = ref(
        crypto.randomUUID()
      )


      // ----------------------------------------------
      // AI answer
      // ----------------------------------------------

      const answer = ref('')


      // ----------------------------------------------
      // Loading state
      // ----------------------------------------------

      const loading = ref(false)


      // ----------------------------------------------
      // Error state
      // ----------------------------------------------

      const error = ref('')


      // ----------------------------------------------
      // Ask AI question
      // ----------------------------------------------

      const askQuestion = async (
        question: string
      ) => {

        if (!question.trim()) {

          return

        }


        loading.value = true

        error.value = ''


        try {

          const response =
            await analyzeDashboard(

              question,

              conversationId.value

            )


          if (response.success) {

            answer.value =
              response.answer || ''

          }
          else {

            answer.value = ''

            error.value =
              response.message ||
              'Unable to analyze the dashboard.'

          }

        }
        catch (err) {

          console.error(
            'AI request failed:',
            err
          )


          answer.value = ''

          error.value =
            'Unable to connect to the AI backend.'

        }
        finally {

          loading.value = false

        }
      }


      // ----------------------------------------------
      // Start a new conversation
      // ----------------------------------------------

      const newConversation = () => {

        conversationId.value =
          crypto.randomUUID()

        answer.value = ''

        error.value = ''

      }


      return {

        conversationId,

        answer,

        loading,

        error,

        askQuestion,

        newConversation

      }

    }
  )