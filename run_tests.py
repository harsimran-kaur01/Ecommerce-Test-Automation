#!/usr/bin/env python
"""
Script to run the test suite
"""

import subprocess
import sys
import os


def run_tests():
    """Run all tests with coverage and reporting"""

    print("\n" + "=" * 60)
    print("🚀 Starting E-Commerce Test Automation Framework")
    print("=" * 60 + "\n")

    # Run pytest with options
    cmd = [
        "pytest",
        "-v",
        "--html=reports/test_report.html",
        "--self-contained-html",
        "tests/",
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("📊 Report generated at: reports/test_report.html")
        print("=" * 60 + "\n")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("❌ Some tests failed. Check the report for details.")
        print("📊 Report generated at: reports/test_report.html")
        print("=" * 60 + "\n")
        return e.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
