import axios from 'axios';
import { FETCH_USERS, CREATE_USER, UPDATE_USER, DELETE_USER } from '../types';

// Action creator for fetching a list of users
export const fetchUsers = () => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch users
      const response = await axios.get('/api/users');
      
      // Dispatch FETCH_USERS action with the received data
      dispatch({
        type: FETCH_USERS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching users:', error);
    }
  };
};

// Action creator for creating a new user
export const createUser = (userData) => {
  return async (dispatch) => {
    try {
      // Make an API call to create a new user with the provided userData
      const response = await axios.post('/api/users', userData);
      
      // Dispatch CREATE_USER action with the received data
      dispatch({
        type: CREATE_USER,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error creating user:', error);
    }
  };
};

// Action creator for updating an existing user
export const updateUser = (userId, userData) => {
  return async (dispatch) => {
    try {
      // Make an API call to update the user with the provided userId and userData
      const response = await axios.put(`/api/users/${userId}`, userData);
      
      // Dispatch UPDATE_USER action with the received data
      dispatch({
        type: UPDATE_USER,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error updating user:', error);
    }
  };
};

// Action creator for deleting a user
export const deleteUser = (userId) => {
  return async (dispatch) => {
    try {
      // Make an API call to delete the user with the provided userId
      await axios.delete(`/api/users/${userId}`);
      
      // Dispatch DELETE_USER action with the userId
      dispatch({
        type: DELETE_USER,
        payload: userId
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error deleting user:', error);
    }
  };
};