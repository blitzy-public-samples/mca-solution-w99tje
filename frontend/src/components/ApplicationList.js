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
  TablePagination,
  IconButton
} from '@material-ui/core';
import { Visibility, Edit } from '@material-ui/icons';
import { fetchApplications } from '../redux/actions/applicationActions';
import ApplicationDetails from './ApplicationDetails';

const ApplicationList = () => {
  // Initialize state for pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // Initialize state for selected application
  const [selectedApplication, setSelectedApplication] = useState(null);

  // Get the dispatch function
  const dispatch = useDispatch();

  // Get applications data from Redux store
  const applications = useSelector(state => state.applications.list);

  // Fetch applications on component mount and when pagination changes
  useEffect(() => {
    dispatch(fetchApplications(page, rowsPerPage));
  }, [dispatch, page, rowsPerPage]);

  // Handle page change
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  // Handle rows per page change
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Handle view application
  const handleViewApplication = (application) => {
    setSelectedApplication(application);
  };

  // Handle edit application
  const handleEditApplication = (applicationId) => {
    // TODO: Implement edit functionality
    console.log('Edit application:', applicationId);
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Applicant Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Submission Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {applications.map((application) => (
              <TableRow key={application.id}>
                <TableCell>{application.id}</TableCell>
                <TableCell>{application.applicantName}</TableCell>
                <TableCell>{application.status}</TableCell>
                <TableCell>{new Date(application.submissionDate).toLocaleDateString()}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleViewApplication(application)}>
                    <Visibility />
                  </IconButton>
                  <IconButton onClick={() => handleEditApplication(application.id)}>
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={applications.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
      {selectedApplication && (
        <ApplicationDetails
          application={selectedApplication}
          onClose={() => setSelectedApplication(null)}
        />
      )}
    </>
  );
};

export default ApplicationList;