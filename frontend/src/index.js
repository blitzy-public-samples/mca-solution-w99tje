// Import necessary dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './App';
import configureStore from './redux/store';
import './index.css';

// Configure the Redux store
const store = configureStore();

// Render function to mount the React application
function render() {
  // Wrap the App component with the Redux Provider
  // Pass the configured store to the Provider
  const wrappedApp = (
    <Provider store={store}>
      <App />
    </Provider>
  );

  // Use ReactDOM.render to render the wrapped App component
  // Mount the application to the DOM element with id 'root'
  ReactDOM.render(wrappedApp, document.getElementById('root'));
}

// Call the render function to start the application
render();