import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.controllers.application_controller import create_application, get_application, get_applications, update_application
from src.api.models.application import Application
from src.api.schemas.application_schema import ApplicationCreate, ApplicationUpdate
from src.api.models.user import User

@pytest.mark.asyncio
async def test_create_application(db_session: Session, mock_user: User):
    # Create a mock ApplicationCreate object
    mock_application_create = ApplicationCreate(
        user_id=mock_user.id,
        loan_amount=10000,
        loan_purpose="Home Improvement",
        credit_score=750
    )

    # Call create_application with the mock object
    created_application = await create_application(db_session, mock_application_create)

    # Assert that the returned application has the correct attributes
    assert created_application.user_id == mock_user.id
    assert created_application.loan_amount == 10000
    assert created_application.loan_purpose == "Home Improvement"
    assert created_application.credit_score == 750

    # Verify that the application was added to the database session
    db_session.refresh(created_application)
    assert db_session.query(Application).filter(Application.id == created_application.id).first() is not None

@pytest.mark.asyncio
async def test_get_application(db_session: Session, mock_user: User):
    # Create a mock Application object and add it to the database session
    mock_application = Application(
        user_id=mock_user.id,
        loan_amount=15000,
        loan_purpose="Debt Consolidation",
        credit_score=700
    )
    db_session.add(mock_application)
    db_session.commit()

    # Call get_application with the mock application's ID
    retrieved_application = await get_application(db_session, mock_application.id)

    # Assert that the returned application matches the mock application
    assert retrieved_application.id == mock_application.id
    assert retrieved_application.user_id == mock_application.user_id
    assert retrieved_application.loan_amount == mock_application.loan_amount
    assert retrieved_application.loan_purpose == mock_application.loan_purpose
    assert retrieved_application.credit_score == mock_application.credit_score

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await get_application(db_session, 9999)

@pytest.mark.asyncio
async def test_get_applications(db_session: Session, mock_user: User):
    # Create multiple mock Application objects and add them to the database session
    mock_applications = [
        Application(user_id=mock_user.id, loan_amount=5000, loan_purpose="Car Loan", credit_score=680),
        Application(user_id=mock_user.id, loan_amount=20000, loan_purpose="Business Loan", credit_score=720),
        Application(user_id=mock_user.id, loan_amount=8000, loan_purpose="Vacation", credit_score=690)
    ]
    db_session.add_all(mock_applications)
    db_session.commit()

    # Call get_applications with various skip and limit parameters
    all_applications = await get_applications(db_session, skip=0, limit=100)
    assert len(all_applications) == 3

    first_two_applications = await get_applications(db_session, skip=0, limit=2)
    assert len(first_two_applications) == 2
    assert first_two_applications[0].id == mock_applications[0].id
    assert first_two_applications[1].id == mock_applications[1].id

    last_application = await get_applications(db_session, skip=2, limit=1)
    assert len(last_application) == 1
    assert last_application[0].id == mock_applications[2].id

    # Test pagination by verifying that different subsets of applications are returned with different skip/limit values
    second_application = await get_applications(db_session, skip=1, limit=1)
    assert len(second_application) == 1
    assert second_application[0].id == mock_applications[1].id

@pytest.mark.asyncio
async def test_update_application(db_session: Session, mock_user: User):
    # Create a mock Application object and add it to the database session
    mock_application = Application(
        user_id=mock_user.id,
        loan_amount=12000,
        loan_purpose="Education",
        credit_score=710
    )
    db_session.add(mock_application)
    db_session.commit()

    # Create a mock ApplicationUpdate object with updated values
    mock_application_update = ApplicationUpdate(
        loan_amount=15000,
        loan_purpose="Higher Education",
        credit_score=720
    )

    # Call update_application with the mock application's ID and the update object
    updated_application = await update_application(db_session, mock_application.id, mock_application_update)

    # Assert that the returned application has the updated attributes
    assert updated_application.id == mock_application.id
    assert updated_application.user_id == mock_application.user_id
    assert updated_application.loan_amount == 15000
    assert updated_application.loan_purpose == "Higher Education"
    assert updated_application.credit_score == 720

    # Verify that the application in the database session was updated
    db_session.refresh(updated_application)
    assert db_session.query(Application).filter(Application.id == updated_application.id).first().loan_amount == 15000

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await update_application(db_session, 9999, mock_application_update)