#!/bin/bash

# Global variables
DB_NAME="mca_application_db"
DB_USER="mca_admin"
DB_PASSWORD="your_secure_password"

# Function to create the PostgreSQL database
create_database() {
    # Check if the database already exists
    if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo "Database $DB_NAME already exists."
    else
        # Create the database using psql command
        if psql -c "CREATE DATABASE $DB_NAME;"; then
            echo "Database $DB_NAME created successfully."
        else
            echo "Failed to create database $DB_NAME."
            exit 1
        fi
    fi
}

# Function to create the PostgreSQL user
create_user() {
    # Check if the user already exists
    if psql -t -c "SELECT 1 FROM pg_user WHERE usename = '$DB_USER';" | grep -q 1; then
        echo "User $DB_USER already exists."
    else
        # Create the user using psql command
        if psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"; then
            echo "User $DB_USER created successfully."
            
            # Grant necessary privileges to the user
            psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
            echo "Privileges granted to $DB_USER."
        else
            echo "Failed to create user $DB_USER."
            exit 1
        fi
    fi
}

# Function to run database migrations
run_migrations() {
    # Change to the directory containing Alembic configuration
    cd /path/to/alembic/directory || exit

    # Run Alembic upgrade command to apply all migrations
    if alembic upgrade head; then
        echo "Database migrations applied successfully."
    else
        echo "Failed to apply database migrations."
        exit 1
    fi
}

# Main function to orchestrate database setup
main() {
    # Call create_database function
    create_database

    # Call create_user function
    create_user

    # Call run_migrations function
    run_migrations

    # Print overall success message
    echo "Database setup completed successfully."
}

# Execute the main function
main