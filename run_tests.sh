#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file with template values..."
    cat > .env << EOF
# Datadis API credentials
DATADIS_USERNAME=your_nif_here
DATADIS_PASSWORD=your_password_here

# Test data (optional, for integration tests)
# If not provided, the tests will attempt to auto-discover a CUPS from your account
TEST_CUPS=ES0021000000000000XXXX
TEST_DISTRIBUTOR_CODE=0000
TEST_POINT_TYPE=5

# Test date ranges (optional)
TEST_START_DATE=2023/01  # Format: YYYY/MM
TEST_END_DATE=2023/02    # Format: YYYY/MM
EOF
    echo "Please edit the .env file with your actual credentials before running integration tests."
    echo "Integration tests REQUIRE valid Datadis credentials."
    echo ""
fi

# Prompt user before running integration tests
echo ""
echo "Do you want to run integration tests? These REQUIRE valid Datadis credentials in the .env file."
echo "If you haven't already, please edit the .env file with your actual credentials."
echo -n "Run integration tests? (y/n): "
read answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    # Check if credentials are still the defaults
    if grep -q "your_nif_here" .env || grep -q "your_password_here" .env; then
        echo "Warning: It appears you haven't updated the credentials in the .env file."
        echo -n "Are you sure you want to continue? (y/n): "
        read continue_answer
        if [ "$continue_answer" != "y" ] && [ "$continue_answer" != "Y" ]; then
            echo "Integration tests skipped. Please update the .env file and try again."
            exit 0
        fi
    fi
    
    echo "Running integration tests..."
    python -m pytest tests/test_integration.py -v
else
    echo "Integration tests skipped."
fi 