import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Grid, Paper, Typography } from '@material-ui/core';
import { TrendingUp, Description, Notifications } from '@material-ui/icons';
import { fetchApplicationStatistics } from '../redux/actions/applicationActions';
import ApplicationList from './ApplicationList';
import NotificationPanel from './NotificationPanel';
import QuickActions from './QuickActions';

const Dashboard = () => {
  // Initialize state for statistics using useState
  const [statistics, setStatistics] = useState({
    totalApplications: 0,
    pendingApplications: 0,
    approvedApplications: 0,
  });

  // Get the dispatch function using useDispatch
  const dispatch = useDispatch();

  // Use useSelector to get application statistics from Redux store
  const applicationStats = useSelector(state => state.applications.statistics);

  // Use useEffect to fetch application statistics on component mount
  useEffect(() => {
    dispatch(fetchApplicationStatistics());
  }, [dispatch]);

  // Update local state when Redux store changes
  useEffect(() => {
    if (applicationStats) {
      setStatistics(applicationStats);
    }
  }, [applicationStats]);

  // Render the dashboard layout using Material-UI Grid
  return (
    <Grid container spacing={3}>
      {/* Render statistics cards for total applications, pending applications, and approved applications */}
      <Grid item xs={12} sm={4}>
        <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
          <TrendingUp color="primary" style={{ fontSize: 40 }} />
          <Typography variant="h6">Total Applications</Typography>
          <Typography variant="h4">{statistics.totalApplications}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={4}>
        <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
          <Description color="secondary" style={{ fontSize: 40 }} />
          <Typography variant="h6">Pending Applications</Typography>
          <Typography variant="h4">{statistics.pendingApplications}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={4}>
        <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
          <Notifications color="primary" style={{ fontSize: 40 }} />
          <Typography variant="h6">Approved Applications</Typography>
          <Typography variant="h4">{statistics.approvedApplications}</Typography>
        </Paper>
      </Grid>

      {/* Render the ApplicationList component */}
      <Grid item xs={12} md={8}>
        <Paper elevation={3} style={{ padding: '20px' }}>
          <Typography variant="h5" gutterBottom>Recent Applications</Typography>
          <ApplicationList />
        </Paper>
      </Grid>

      {/* Render the NotificationPanel component */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '20px' }}>
          <Typography variant="h5" gutterBottom>Notifications</Typography>
          <NotificationPanel />
        </Paper>
      </Grid>

      {/* Render the QuickActions component */}
      <Grid item xs={12}>
        <Paper elevation={3} style={{ padding: '20px' }}>
          <Typography variant="h5" gutterBottom>Quick Actions</Typography>
          <QuickActions />
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard;