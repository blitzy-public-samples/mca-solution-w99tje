// Import action types
import { FETCH_USERS, CREATE_USER, UPDATE_USER, DELETE_USER } from '../types';

// Define initial state
const initialState = {
  users: [],
  loading: false,
  error: null
};

// Reducer function for handling user-related actions
const userReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USERS:
      // Return a new state with updated users and loading status
      return {
        ...state,
        users: action.payload,
        loading: false,
        error: null
      };

    case CREATE_USER:
      // Add the new user to the users array
      return {
        ...state,
        users: [...state.users, action.payload],
        loading: false,
        error: null
      };

    case UPDATE_USER:
      // Update the specific user in the users array
      return {
        ...state,
        users: state.users.map(user =>
          user.id === action.payload.id ? action.payload : user
        ),
        loading: false,
        error: null
      };

    case DELETE_USER:
      // Remove the specific user from the users array
      return {
        ...state,
        users: state.users.filter(user => user.id !== action.payload),
        loading: false,
        error: null
      };

    default:
      // Return the current state unchanged
      return state;
  }
};

export default userReducer;