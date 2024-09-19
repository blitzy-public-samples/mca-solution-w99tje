// Import action types
import { FETCH_DOCUMENTS, UPLOAD_DOCUMENT, DOWNLOAD_DOCUMENT } from '../types';

// Define initial state
const initialState = {
  documents: [],
  loading: false,
  error: null
};

// Reducer function for handling document-related actions
const documentReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_DOCUMENTS:
      // Return a new state with updated documents and loading status
      return {
        ...state,
        documents: action.payload,
        loading: false,
        error: null
      };

    case UPLOAD_DOCUMENT:
      // Add the new document to the documents array
      return {
        ...state,
        documents: [...state.documents, action.payload],
        loading: false,
        error: null
      };

    case DOWNLOAD_DOCUMENT:
      // Update the download status of the specific document in the documents array
      return {
        ...state,
        documents: state.documents.map(doc =>
          doc.id === action.payload.id
            ? { ...doc, downloadStatus: action.payload.downloadStatus }
            : doc
        )
      };

    default:
      // Return the current state unchanged
      return state;
  }
};

export default documentReducer;