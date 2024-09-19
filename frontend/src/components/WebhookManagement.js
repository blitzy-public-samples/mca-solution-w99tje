import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@material-ui/core';
import { Add, Edit, Delete, PlayArrow } from '@material-ui/icons';
import {
  fetchWebhooks,
  createWebhook,
  updateWebhook,
  deleteWebhook,
  testWebhook
} from '../redux/actions/webhookActions';

const WebhookManagement = () => {
  // Initialize state for dialog open status, current webhook, and form data
  const [dialogOpen, setDialogOpen] = useState(false);
  const [currentWebhook, setCurrentWebhook] = useState(null);
  const [formData, setFormData] = useState({ url: '', eventType: '' });

  // Get the dispatch function
  const dispatch = useDispatch();

  // Get webhooks data from Redux store
  const webhooks = useSelector(state => state.webhooks.webhooks);

  // Fetch webhooks on component mount
  useEffect(() => {
    dispatch(fetchWebhooks());
  }, [dispatch]);

  // Function to open the webhook dialog
  const handleOpenDialog = (webhook = null) => {
    setCurrentWebhook(webhook);
    setFormData(webhook || { url: '', eventType: '' });
    setDialogOpen(true);
  };

  // Function to close the webhook dialog
  const handleCloseDialog = () => {
    setDialogOpen(false);
    setCurrentWebhook(null);
    setFormData({ url: '', eventType: '' });
  };

  // Function to update form data
  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Function to create or update webhooks
  const handleSubmit = () => {
    if (currentWebhook) {
      dispatch(updateWebhook(currentWebhook.id, formData));
    } else {
      dispatch(createWebhook(formData));
    }
    handleCloseDialog();
  };

  // Function to delete webhooks
  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this webhook?')) {
      dispatch(deleteWebhook(id));
    }
  };

  // Function to test webhooks
  const handleTest = (id) => {
    dispatch(testWebhook(id));
  };

  return (
    <div>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>URL</TableCell>
              <TableCell>Event Type</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {webhooks.map((webhook) => (
              <TableRow key={webhook.id}>
                <TableCell>{webhook.url}</TableCell>
                <TableCell>{webhook.eventType}</TableCell>
                <TableCell>
                  <Button startIcon={<Edit />} onClick={() => handleOpenDialog(webhook)}>
                    Edit
                  </Button>
                  <Button startIcon={<Delete />} onClick={() => handleDelete(webhook.id)}>
                    Delete
                  </Button>
                  <Button startIcon={<PlayArrow />} onClick={() => handleTest(webhook.id)}>
                    Test
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Button startIcon={<Add />} onClick={() => handleOpenDialog()}>
        Add Webhook
      </Button>

      <Dialog open={dialogOpen} onClose={handleCloseDialog}>
        <DialogTitle>{currentWebhook ? 'Edit Webhook' : 'Add Webhook'}</DialogTitle>
        <DialogContent>
          <TextField
            name="url"
            label="Webhook URL"
            fullWidth
            value={formData.url}
            onChange={handleInputChange}
            margin="normal"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Event Type</InputLabel>
            <Select
              name="eventType"
              value={formData.eventType}
              onChange={handleInputChange}
            >
              <MenuItem value="application_submitted">Application Submitted</MenuItem>
              <MenuItem value="application_approved">Application Approved</MenuItem>
              <MenuItem value="application_rejected">Application Rejected</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default WebhookManagement;