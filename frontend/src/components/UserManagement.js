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
import { Add, Edit, Delete } from '@material-ui/icons';
import { fetchUsers, createUser, updateUser, deleteUser } from '../redux/actions/userActions';

const UserManagement = () => {
  // Initialize state for dialog open status, current user, and form data
  const [dialogOpen, setDialogOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    fullName: '',
    role: '',
    password: ''
  });

  // Get the dispatch function
  const dispatch = useDispatch();

  // Get users data from Redux store
  const users = useSelector(state => state.users);

  // Fetch users on component mount
  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  // Function to open the user dialog
  const handleOpenDialog = (user = null) => {
    setCurrentUser(user);
    if (user) {
      setFormData({
        email: user.email,
        fullName: user.fullName,
        role: user.role,
        password: ''
      });
    } else {
      setFormData({
        email: '',
        fullName: '',
        role: '',
        password: ''
      });
    }
    setDialogOpen(true);
  };

  // Function to close the user dialog
  const handleCloseDialog = () => {
    setDialogOpen(false);
    setCurrentUser(null);
  };

  // Function to update form data
  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Function to create or update users
  const handleSubmit = () => {
    if (currentUser) {
      dispatch(updateUser(currentUser.id, formData));
    } else {
      dispatch(createUser(formData));
    }
    handleCloseDialog();
  };

  // Function to delete users
  const handleDelete = (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      dispatch(deleteUser(userId));
    }
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Email</TableCell>
              <TableCell>Full Name</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.fullName}</TableCell>
                <TableCell>{user.role}</TableCell>
                <TableCell>
                  <Button startIcon={<Edit />} onClick={() => handleOpenDialog(user)}>
                    Edit
                  </Button>
                  <Button startIcon={<Delete />} onClick={() => handleDelete(user.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Button
        startIcon={<Add />}
        variant="contained"
        color="primary"
        onClick={() => handleOpenDialog()}
        style={{ marginTop: '1rem' }}
      >
        Add User
      </Button>

      <Dialog open={dialogOpen} onClose={handleCloseDialog}>
        <DialogTitle>{currentUser ? 'Edit User' : 'Add User'}</DialogTitle>
        <DialogContent>
          <TextField
            name="email"
            label="Email"
            fullWidth
            value={formData.email}
            onChange={handleInputChange}
            margin="normal"
          />
          <TextField
            name="fullName"
            label="Full Name"
            fullWidth
            value={formData.fullName}
            onChange={handleInputChange}
            margin="normal"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Role</InputLabel>
            <Select
              name="role"
              value={formData.role}
              onChange={handleInputChange}
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="user">User</MenuItem>
            </Select>
          </FormControl>
          <TextField
            name="password"
            label="Password"
            type="password"
            fullWidth
            value={formData.password}
            onChange={handleInputChange}
            margin="normal"
          />
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
    </>
  );
};

export default UserManagement;