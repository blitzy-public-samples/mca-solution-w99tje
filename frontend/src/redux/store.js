// Import necessary dependencies from Redux
import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import { createLogger } from 'redux-logger';

// Import reducers
import applicationReducer from './reducers/applicationReducer';
import documentReducer from './reducers/documentReducer';
import userReducer from './reducers/userReducer';
import webhookReducer from './reducers/webhookReducer';

// Function to configure and create the Redux store
export function configureStore() {
  // Step 1: Combine reducers using combineReducers
  const rootReducer = combineReducers({
    application: applicationReducer,
    document: documentReducer,
    user: userReducer,
    webhook: webhookReducer
  });

  // Step 2: Create logger middleware using createLogger
  const logger = createLogger();

  // Step 3: Create an array of middlewares including thunk and logger
  const middlewares = [thunk, logger];

  // Step 4: Apply middleware to the store using applyMiddleware
  const middlewareEnhancer = applyMiddleware(...middlewares);

  // Step 5: Create the store using createStore with the root reducer and applied middleware
  const store = createStore(rootReducer, middlewareEnhancer);

  // Step 6: Return the configured store
  return store;
}