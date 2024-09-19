import axios from 'axios';
import { FETCH_DOCUMENTS, UPLOAD_DOCUMENT, DOWNLOAD_DOCUMENT } from '../types';

// Action creator for fetching documents associated with an application
export const fetchDocuments = (applicationId) => {
  return async (dispatch) => {
    try {
      // Make an API call to fetch documents for the given application ID
      const response = await axios.get(`/api/documents/${applicationId}`);
      
      // Dispatch FETCH_DOCUMENTS action with the received data
      dispatch({
        type: FETCH_DOCUMENTS,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error fetching documents:', error);
    }
  };
};

// Action creator for uploading a new document
export const uploadDocument = (applicationId, file) => {
  return async (dispatch) => {
    try {
      // Create a FormData object and append the file and application ID
      const formData = new FormData();
      formData.append('file', file);
      formData.append('applicationId', applicationId);

      // Make an API call to upload the document
      const response = await axios.post('/api/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Dispatch UPLOAD_DOCUMENT action with the received data
      dispatch({
        type: UPLOAD_DOCUMENT,
        payload: response.data
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error uploading document:', error);
    }
  };
};

// Action creator for downloading a document
export const downloadDocument = (documentId) => {
  return async (dispatch) => {
    try {
      // Make an API call to download the document
      const response = await axios.get(`/api/documents/download/${documentId}`, {
        responseType: 'blob'
      });

      // Create a Blob from the response data
      const blob = new Blob([response.data], { type: response.headers['content-type'] });

      // Create a temporary URL for the Blob
      const url = window.URL.createObjectURL(blob);

      // Create a temporary anchor element and trigger the download
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `document_${documentId}`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      // Dispatch DOWNLOAD_DOCUMENT action with the document ID
      dispatch({
        type: DOWNLOAD_DOCUMENT,
        payload: documentId
      });
    } catch (error) {
      // Handle any errors and log them
      console.error('Error downloading document:', error);
    }
  };
};