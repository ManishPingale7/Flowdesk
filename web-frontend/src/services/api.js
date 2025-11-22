import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://flowdesk-production.up.railway.app/api'

const getAuthHeader = () => {
  const auth = localStorage.getItem('auth')
  if (auth) {
    return {
      headers: {
        'Authorization': `Basic ${auth}`
      }
    }
  }
  return {}
}

export const register = async (username, email, password) => {
  const response = await axios.post(
    `${API_BASE_URL}/register/`,
    {
      username,
      email,
      password,
      password_confirm: password
    }
  )
  return response.data
}

export const login = async (username, password) => {
  const auth = btoa(`${username}:${password}`)
  const response = await axios.get(
    `${API_BASE_URL}/history/`,
    {
      headers: {
        'Authorization': `Basic ${auth}`
      }
    }
  )
  return response.data
}

export const uploadCSV = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(
    `${API_BASE_URL}/upload/`,
    formData,
    {
      ...getAuthHeader(),
      'Content-Type': 'multipart/form-data'
    }
  )
  return response.data
}

export const getSummary = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/summary/`,
    getAuthHeader()
  )
  return response.data
}

export const getHistory = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/history/`,
    getAuthHeader()
  )
  return response.data
}

export const downloadPDF = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/report/pdf/`,
    {
      ...getAuthHeader(),
      responseType: 'blob'
    }
  )
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'equipment_report.pdf')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

