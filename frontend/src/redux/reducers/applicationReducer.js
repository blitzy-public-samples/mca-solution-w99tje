// Import action types
import {
  FETCH_APPLICATIONS,
  FETCH_APPLICATION_DETAILS,
  FETCH_APPLICATION_STATISTICS,
  UPDATE_APPLICATION_STATUS
} from '../types';

// Define initial state
const initialState = {
  applications: [],
  currentApplication: null,
  statistics: null,
  loading: false,
  error: null
};

// Reducer function for handling application-related actions
const applicationReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_APPLICATIONS:
      // Return a new state with updated applications and loading status
      return {
        ...state,
        applications: action.payload,
        loading: false
      };

    case FETCH_APPLICATION_DETAILS:
      // Return a new state with updated currentApplication and loading status
      return {
        ...state,
        currentApplication: action.payload,
        loading: false
      };

    case FETCH_APPLICATION_STATISTICS:
      // Return a new state with updated statistics and loading status
      return {
        ...state,
        statistics: action.payload,
        loading: false
      };

    case UPDATE_APPLICATION_STATUS:
      // Update the status of the specific application in the applications array
      const updatedApplications = state.applications.map(app =>
        app.id === action.payload.id ? { ...app, status: action.payload.status } : app
      );

      // If the updated application is the currentApplication, update it as well
      const updatedCurrentApplication = state.currentApplication && state.currentApplication.id === action.payload.id
        ? { ...state.currentApplication, status: action.payload.status }
        : state.currentApplication;

      // Return the new state with updated applications and currentApplication
      return {
        ...state,
        applications: updatedApplications,
        currentApplication: updatedCurrentApplication
      };

    default:
      // Return the current state unchanged
      return state;
  }
};

export default applicationReducer;