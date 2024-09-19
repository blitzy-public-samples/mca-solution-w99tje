import axios from 'axios';
import { FETCH_WEBHOOKS, CREATE_WEBHOOK, UPDATE_WEBHOOK, DELETE_WEBHOOK, TEST_WEBHOOK } from '../types';

// Action creator for fetching a list of webhooks
export const fetchWebhooks = () => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch webhooks
      const response = await axios.get('/api/webhooks');
      
      // Dispatch FETCH_WEBHOOKS action with the received data
      dispatch({
        type: FETCH_WEBHOOKS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching webhooks:', error);
    }
  };
};

// Action creator for creating a new webhook
export const createWebhook = (webhookData) => {
  return async (dispatch) => {
    try {
      // Make an API call to create a new webhook with the provided webhookData
      const response = await axios.post('/api/webhooks', webhookData);
      
      // Dispatch CREATE_WEBHOOK action with the received data
      dispatch({
        type: CREATE_WEBHOOK,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error creating webhook:', error);
    }
  };
};

// Action creator for updating an existing webhook
export const updateWebhook = (webhookId, webhookData) => {
  return async (dispatch) => {
    try {
      // Make an API call to update the webhook with the provided webhookId and webhookData
      const response = await axios.put(`/api/webhooks/${webhookId}`, webhookData);
      
      // Dispatch UPDATE_WEBHOOK action with the received data
      dispatch({
        type: UPDATE_WEBHOOK,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error updating webhook:', error);
    }
  };
};

// Action creator for deleting a webhook
export const deleteWebhook = (webhookId) => {
  return async (dispatch) => {
    try {
      // Make an API call to delete the webhook with the provided webhookId
      await axios.delete(`/api/webhooks/${webhookId}`);
      
      // Dispatch DELETE_WEBHOOK action with the webhookId
      dispatch({
        type: DELETE_WEBHOOK,
        payload: webhookId
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error deleting webhook:', error);
    }
  };
};

// Action creator for testing a webhook
export const testWebhook = (webhookId) => {
  return async (dispatch) => {
    try {
      // Make an API call to test the webhook with the provided webhookId
      const response = await axios.post(`/api/webhooks/${webhookId}/test`);
      
      // Dispatch TEST_WEBHOOK action with the test result
      dispatch({
        type: TEST_WEBHOOK,
        payload: {
          webhookId,
          testResult: response.data
        }
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error testing webhook:', error);
    }
  };
};