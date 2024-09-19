import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { CssBaseline, ThemeProvider } from '@material-ui/core';
import Dashboard from './components/Dashboard';
import ApplicationList from './components/ApplicationList';
import ApplicationDetails from './components/ApplicationDetails';
import WebhookManagement from './components/WebhookManagement';
import UserManagement from './components/UserManagement';
import Login from './components/Login';
import Header from './components/Header';
import theme from './theme';

function App() {
  return (
    // Wrap the entire app with ThemeProvider and pass the custom theme
    <ThemeProvider theme={theme}>
      {/* Include CssBaseline for consistent styling */}
      <CssBaseline />
      {/* Set up Router for handling navigation */}
      <Router>
        {/* Render Header component */}
        <Header />
        {/* Set up Switch for rendering different routes */}
        <Switch>
          {/* Define Route for Dashboard component */}
          <Route exact path="/" component={Dashboard} />
          {/* Define Route for ApplicationList component */}
          <Route exact path="/applications" component={ApplicationList} />
          {/* Define Route for ApplicationDetails component */}
          <Route path="/applications/:id" component={ApplicationDetails} />
          {/* Define Route for WebhookManagement component */}
          <Route path="/webhooks" component={WebhookManagement} />
          {/* Define Route for UserManagement component */}
          <Route path="/users" component={UserManagement} />
          {/* Define Route for Login component */}
          <Route path="/login" component={Login} />
        </Switch>
      </Router>
    </ThemeProvider>
  );
}

export default App;