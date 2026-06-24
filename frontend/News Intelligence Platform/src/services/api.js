import axios from 'axios'


const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})


export async function fetchArticles() {
  const response = await api.get('/articles')
  return response.data           
}


export async function askQuestion(question) {
  const response = await api.post('/ask', { question })
  return response.data
}