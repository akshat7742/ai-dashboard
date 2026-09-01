import axios from 'axios'


const API_URL =
  'http://localhost:8000'


export interface AnalyzeRequest {

  conversation_id: string

  question: string

}


export interface AnalyzeResponse {

  success: boolean

  answer?: string

  message?: string

}


export const analyzeDashboard = async (

  question: string,

  conversationId: string

): Promise<AnalyzeResponse> => {

  const request: AnalyzeRequest = {

    conversation_id:
      conversationId,

    question

  }


  const response =
    await axios.post<AnalyzeResponse>(

      `${API_URL}/analyze`,

      request

    )


  return response.data
}