// Import action types
import { FETCH_WEBHOOKS, CREATE_WEBHOOK, UPDATE_WEBHOOK, DELETE_WEBHOOK, TEST_WEBHOOK } from '../types';

// Define initial state
const initialState = {
  webhooks: [],
  loading: false,
  error: null,
  testResult: null
};

// Webhook reducer function
const webhookReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_WEBHOOKS:
      // Update webhooks and loading status
      return {
        ...state,
        webhooks: action.payload,
        loading: false
      };

    case CREATE_WEBHOOK:
      // Add new webhook to the array
      return {
        ...state,
        webhooks: [...state.webhooks, action.payload],
        loading: false
      };

    case UPDATE_WEBHOOK:
      // Update specific webhook in the array
      return {
        ...state,
        webhooks: state.webhooks.map(webhook =>
          webhook.id === action.payload.id ? action.payload : webhook
        )
      };

    case DELETE_WEBHOOK:
      // Remove specific webhook from the array
      return {
        ...state,
        webhooks: state.webhooks.filter(webhook => webhook.id !== action.payload)
      };

    case TEST_WEBHOOK:
      // Update testResult with action payload
      return {
        ...state,
        testResult: action.payload
      };

    default:
      // Return current state unchanged for unknown action types
      return state;
  }
};

export default webhookReducer;