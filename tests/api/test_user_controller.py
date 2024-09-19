import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.controllers.user_controller import create_user, get_user, get_users, update_user, delete_user
from src.api.models.user import User, UserRole
from src.api.schemas.user_schema import UserCreate, UserUpdate
from src.core.security import get_password_hash, verify_password

@pytest.mark.asyncio
async def test_create_user(db_session: Session, mock_admin_user: User):
    # Create a mock UserCreate object
    user_create = UserCreate(
        email="test@example.com",
        password="testpassword",
        full_name="Test User",
        role=UserRole.USER
    )

    # Call create_user with the mock object and admin user
    created_user = await create_user(db_session, user_create, mock_admin_user)

    # Assert that the returned user has the correct attributes
    assert created_user.email == user_create.email
    assert created_user.full_name == user_create.full_name
    assert created_user.role == user_create.role

    # Verify that the user was added to the database session
    db_user = db_session.query(User).filter(User.email == user_create.email).first()
    assert db_user is not None

    # Check that the password was properly hashed
    assert verify_password(user_create.password, db_user.hashed_password)

    # Test creating a user with non-admin privileges and assert it raises an HTTPException
    non_admin_user = User(role=UserRole.USER)
    with pytest.raises(HTTPException):
        await create_user(db_session, user_create, non_admin_user)

@pytest.mark.asyncio
async def test_get_user(db_session: Session, mock_admin_user: User):
    # Create a mock User object and add it to the database session
    mock_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        role=UserRole.USER
    )
    db_session.add(mock_user)
    db_session.commit()

    # Call get_user with the mock user's ID and admin user
    retrieved_user = await get_user(db_session, mock_user.id, mock_admin_user)

    # Assert that the returned user matches the mock user
    assert retrieved_user.id == mock_user.id
    assert retrieved_user.email == mock_user.email
    assert retrieved_user.full_name == mock_user.full_name
    assert retrieved_user.role == mock_user.role

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await get_user(db_session, 9999, mock_admin_user)

    # Test retrieving a user with non-admin privileges and assert it raises an HTTPException if it's not the current user
    non_admin_user = User(id=2, role=UserRole.USER)
    with pytest.raises(HTTPException):
        await get_user(db_session, mock_user.id, non_admin_user)

@pytest.mark.asyncio
async def test_get_users(db_session: Session, mock_admin_user: User):
    # Create multiple mock User objects and add them to the database session
    mock_users = [
        User(email=f"user{i}@example.com", hashed_password=get_password_hash(f"password{i}"), full_name=f"User {i}", role=UserRole.USER)
        for i in range(10)
    ]
    db_session.add_all(mock_users)
    db_session.commit()

    # Call get_users with various skip and limit parameters
    users = await get_users(db_session, skip=0, limit=5, current_user=mock_admin_user)
    assert len(users) == 5

    users = await get_users(db_session, skip=5, limit=5, current_user=mock_admin_user)
    assert len(users) == 5

    users = await get_users(db_session, skip=0, limit=100, current_user=mock_admin_user)
    assert len(users) == 10

    # Test pagination by verifying that different subsets of users are returned with different skip/limit values
    first_page = await get_users(db_session, skip=0, limit=3, current_user=mock_admin_user)
    second_page = await get_users(db_session, skip=3, limit=3, current_user=mock_admin_user)
    assert first_page != second_page

    # Test retrieving users with non-admin privileges and assert it raises an HTTPException
    non_admin_user = User(role=UserRole.USER)
    with pytest.raises(HTTPException):
        await get_users(db_session, skip=0, limit=10, current_user=non_admin_user)

@pytest.mark.asyncio
async def test_update_user(db_session: Session, mock_admin_user: User):
    # Create a mock User object and add it to the database session
    mock_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        role=UserRole.USER
    )
    db_session.add(mock_user)
    db_session.commit()

    # Create a mock UserUpdate object with updated values
    user_update = UserUpdate(
        email="updated@example.com",
        full_name="Updated User",
        password="newpassword"
    )

    # Call update_user with the mock user's ID, update object, and admin user
    updated_user = await update_user(db_session, mock_user.id, user_update, mock_admin_user)

    # Assert that the returned user has the updated attributes
    assert updated_user.email == user_update.email
    assert updated_user.full_name == user_update.full_name

    # Verify that the user in the database session was updated
    db_user = db_session.query(User).filter(User.id == mock_user.id).first()
    assert db_user.email == user_update.email
    assert db_user.full_name == user_update.full_name

    # Test updating a user's password and verify it was properly hashed
    assert verify_password(user_update.password, db_user.hashed_password)

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await update_user(db_session, 9999, user_update, mock_admin_user)

    # Test updating a user with non-admin privileges and assert it raises an HTTPException if it's not the current user
    non_admin_user = User(id=2, role=UserRole.USER)
    with pytest.raises(HTTPException):
        await update_user(db_session, mock_user.id, user_update, non_admin_user)

@pytest.mark.asyncio
async def test_delete_user(db_session: Session, mock_admin_user: User):
    # Create a mock User object and add it to the database session
    mock_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        role=UserRole.USER
    )
    db_session.add(mock_user)
    db_session.commit()

    # Call delete_user with the mock user's ID and admin user
    await delete_user(db_session, mock_user.id, mock_admin_user)

    # Assert that the user was removed from the database session
    deleted_user = db_session.query(User).filter(User.id == mock_user.id).first()
    assert deleted_user is None

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await delete_user(db_session, 9999, mock_admin_user)

    # Test deleting a user with non-admin privileges and assert it raises an HTTPException
    non_admin_user = User(role=UserRole.USER)
    with pytest.raises(HTTPException):
        await delete_user(db_session, mock_user.id, non_admin_user)