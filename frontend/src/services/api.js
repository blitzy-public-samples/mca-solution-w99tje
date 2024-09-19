import axios from 'axios';

// Create an axios instance with the base URL from environment variables
const api = axios.create({ baseURL: process.env.REACT_APP_API_URL });

// Set the authorization token for API requests
export const setAuthToken = (token) => {
  if (token) {
    // If token is provided, set the Authorization header with the Bearer token
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    // If token is not provided, delete the Authorization header
    delete api.defaults.headers.common['Authorization'];
  }
};

// Authenticate user and get token
export const login = async (email, password) => {
  try {
    // Make a POST request to '/auth/login' with email and password
    const response = await api.post('/auth/login', { email, password });
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Fetch applications with optional pagination
export const fetchApplications = async (page, limit) => {
  try {
    // Make a GET request to '/applications' with page and limit as query parameters
    const response = await api.get('/applications', { params: { page, limit } });
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Fetch details of a specific application
export const fetchApplicationDetails = async (applicationId) => {
  try {
    // Make a GET request to '/applications/{applicationId}'
    const response = await api.get(`/applications/${applicationId}`);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update the status of an application
export const updateApplicationStatus = async (applicationId, status) => {
  try {
    // Make a PATCH request to '/applications/{applicationId}' with the new status
    const response = await api.patch(`/applications/${applicationId}`, { status });
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Fetch documents associated with an application
export const fetchDocuments = async (applicationId) => {
  try {
    // Make a GET request to '/applications/{applicationId}/documents'
    const response = await api.get(`/applications/${applicationId}/documents`);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Upload a document for an application
export const uploadDocument = async (applicationId, file) => {
  try {
    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append('file', file);

    // Make a POST request to '/applications/{applicationId}/documents' with the FormData
    const response = await api.post(`/applications/${applicationId}/documents`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Fetch list of users
export const fetchUsers = async () => {
  try {
    // Make a GET request to '/users'
    const response = await api.get('/users');
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Create a new user
export const createUser = async (userData) => {
  try {
    // Make a POST request to '/users' with the userData
    const response = await api.post('/users', userData);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update an existing user
export const updateUser = async (userId, userData) => {
  try {
    // Make a PATCH request to '/users/{userId}' with the userData
    const response = await api.patch(`/users/${userId}`, userData);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Delete a user
export const deleteUser = async (userId) => {
  try {
    // Make a DELETE request to '/users/{userId}'
    const response = await api.delete(`/users/${userId}`);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Fetch list of webhooks
export const fetchWebhooks = async () => {
  try {
    // Make a GET request to '/webhooks'
    const response = await api.get('/webhooks');
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Create a new webhook
export const createWebhook = async (webhookData) => {
  try {
    // Make a POST request to '/webhooks' with the webhookData
    const response = await api.post('/webhooks', webhookData);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update an existing webhook
export const updateWebhook = async (webhookId, webhookData) => {
  try {
    // Make a PATCH request to '/webhooks/{webhookId}' with the webhookData
    const response = await api.patch(`/webhooks/${webhookId}`, webhookData);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Delete a webhook
export const deleteWebhook = async (webhookId) => {
  try {
    // Make a DELETE request to '/webhooks/{webhookId}'
    const response = await api.delete(`/webhooks/${webhookId}`);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Test a webhook
export const testWebhook = async (webhookId) => {
  try {
    // Make a POST request to '/webhooks/{webhookId}/test'
    const response = await api.post(`/webhooks/${webhookId}/test`);
    // Return the response data
    return response.data;
  } catch (error) {
    throw error;
  }
};