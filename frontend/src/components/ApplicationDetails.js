import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Grid,
  Divider
} from '@material-ui/core';
import { fetchApplicationDetails, updateApplicationStatus } from '../redux/actions/applicationActions';
import DocumentViewer from './DocumentViewer';

const ApplicationDetails = ({ applicationId, onClose }) => {
  // Initialize state for application details
  const [application, setApplication] = useState(null);

  // Get the dispatch function
  const dispatch = useDispatch();

  // Get application details from Redux store
  const applicationDetails = useSelector(state => state.applications.currentApplication);

  // Fetch application details when applicationId changes
  useEffect(() => {
    if (applicationId) {
      dispatch(fetchApplicationDetails(applicationId));
    }
  }, [applicationId, dispatch]);

  // Update local state when Redux store changes
  useEffect(() => {
    if (applicationDetails) {
      setApplication(applicationDetails);
    }
  }, [applicationDetails]);

  // Handle approve action
  const handleApprove = () => {
    dispatch(updateApplicationStatus(applicationId, 'APPROVED'));
    onClose();
  };

  // Handle reject action
  const handleReject = () => {
    dispatch(updateApplicationStatus(applicationId, 'REJECTED'));
    onClose();
  };

  if (!application) {
    return null;
  }

  return (
    <Dialog open={true} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Application Details</DialogTitle>
      <DialogContent>
        <Grid container spacing={3}>
          {/* Applicant Information */}
          <Grid item xs={12}>
            <Typography variant="h6">Applicant Information</Typography>
            <Divider />
            <Typography>Name: {application.applicantName}</Typography>
            <Typography>Email: {application.applicantEmail}</Typography>
            <Typography>Phone: {application.applicantPhone}</Typography>
          </Grid>

          {/* Business Details */}
          <Grid item xs={12}>
            <Typography variant="h6">Business Details</Typography>
            <Divider />
            <Typography>Business Name: {application.businessName}</Typography>
            <Typography>Business Type: {application.businessType}</Typography>
            <Typography>Years in Operation: {application.yearsInOperation}</Typography>
          </Grid>

          {/* Funding Request */}
          <Grid item xs={12}>
            <Typography variant="h6">Funding Request</Typography>
            <Divider />
            <Typography>Amount Requested: ${application.amountRequested}</Typography>
            <Typography>Purpose: {application.fundingPurpose}</Typography>
          </Grid>

          {/* Documents */}
          <Grid item xs={12}>
            <Typography variant="h6">Documents</Typography>
            <Divider />
            {application.documents.map((doc, index) => (
              <DocumentViewer key={index} document={doc} />
            ))}
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleApprove} color="primary">
          Approve
        </Button>
        <Button onClick={handleReject} color="secondary">
          Reject
        </Button>
        <Button onClick={onClose}>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ApplicationDetails;