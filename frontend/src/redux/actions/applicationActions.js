import axios from 'axios';
import {
  FETCH_APPLICATIONS,
  FETCH_APPLICATION_DETAILS,
  FETCH_APPLICATION_STATISTICS,
  UPDATE_APPLICATION_STATUS
} from '../types';

// Action creator for fetching a list of applications
export const fetchApplications = (page, limit) => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch applications with pagination parameters
      const response = await axios.get(`/api/applications?page=${page}&limit=${limit}`);
      
      // Dispatch FETCH_APPLICATIONS action with the received data
      dispatch({
        type: FETCH_APPLICATIONS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching applications:', error);
    }
  };
};

// Action creator for fetching details of a specific application
export const fetchApplicationDetails = (applicationId) => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch application details by ID
      const response = await axios.get(`/api/applications/${applicationId}`);
      
      // Dispatch FETCH_APPLICATION_DETAILS action with the received data
      dispatch({
        type: FETCH_APPLICATION_DETAILS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching application details:', error);
    }
  };
};

// Action creator for fetching application statistics
export const fetchApplicationStatistics = () => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch application statistics
      const response = await axios.get('/api/applications/statistics');
      
      // Dispatch FETCH_APPLICATION_STATISTICS action with the received data
      dispatch({
        type: FETCH_APPLICATION_STATISTICS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching application statistics:', error);
    }
  };
};

// Action creator for updating the status of an application
export const updateApplicationStatus = (applicationId, newStatus) => {
  return async (dispatch) => {
    try {
      // Make an API call to update the application status
      const response = await axios.put(`/api/applications/${applicationId}/status`, { status: newStatus });
      
      // Dispatch UPDATE_APPLICATION_STATUS action with the updated data
      dispatch({
        type: UPDATE_APPLICATION_STATUS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error updating application status:', error);
    }
  };
};