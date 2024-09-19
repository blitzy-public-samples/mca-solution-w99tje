import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent
} from '@material-ui/core';
import { Visibility, GetApp } from '@material-ui/icons';
import { fetchDocuments, downloadDocument } from '../redux/actions/documentActions';

const DocumentViewer = ({ applicationId }) => {
  // Initialize state for selected document and viewer open status
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [isViewerOpen, setIsViewerOpen] = useState(false);

  // Get the dispatch function
  const dispatch = useDispatch();

  // Get documents data from Redux store
  const documents = useSelector(state => state.documents.items);

  // Fetch documents when applicationId changes
  useEffect(() => {
    if (applicationId) {
      dispatch(fetchDocuments(applicationId));
    }
  }, [applicationId, dispatch]);

  // Function to open document viewer
  const handleViewDocument = (document) => {
    setSelectedDocument(document);
    setIsViewerOpen(true);
  };

  // Function to close document viewer
  const handleCloseViewer = () => {
    setIsViewerOpen(false);
    setSelectedDocument(null);
  };

  // Function to trigger document download
  const handleDownloadDocument = (documentId) => {
    dispatch(downloadDocument(documentId));
  };

  return (
    <>
      <Typography variant="h6">Documents</Typography>
      <List>
        {documents.map((document) => (
          <ListItem key={document.id}>
            <ListItemText primary={document.name} secondary={document.type} />
            <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="view" onClick={() => handleViewDocument(document)}>
                <Visibility />
              </IconButton>
              <IconButton edge="end" aria-label="download" onClick={() => handleDownloadDocument(document.id)}>
                <GetApp />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>

      {/* Document viewer dialog */}
      <Dialog open={isViewerOpen} onClose={handleCloseViewer} maxWidth="md" fullWidth>
        <DialogTitle>{selectedDocument?.name}</DialogTitle>
        <DialogContent>
          {selectedDocument?.content ? (
            <div dangerouslySetInnerHTML={{ __html: selectedDocument.content }} />
          ) : (
            <Typography>No content available for this document.</Typography>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
};

export default DocumentViewer;