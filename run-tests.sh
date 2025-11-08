#!/bin/bash
# ====================================
# Google Forms System - Run All Tests
# ====================================

echo ""
echo "========================================"
echo "  Running Backend Unit Tests"
echo "========================================"
echo ""

cd backend

# Check if pytest is installed
if ! pip3 show pytest &> /dev/null; then
    echo "[WARNING] pytest not found, installing..."
    pip3 install pytest pytest-asyncio requests
    echo ""
fi

echo "Running test suite..."
echo ""

pytest test_surveys.py -v --tb=short --color=yes

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  Tests Failed! ❌"
    echo "========================================"
    echo ""
    exit 1
else
    echo ""
    echo "========================================"
    echo "  All Tests Passed! ✅"
    echo "========================================"
    echo ""
fi

cd ..

echo ""
echo "Test execution complete."
echo ""
