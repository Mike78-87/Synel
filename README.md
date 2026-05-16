# E-Sign Feature – Automated Tests

This repository contains automated UI tests for the E-Sign feature (https://test-env-slim.synel-saas.com).  
The tests are written in Python using Selenium and Pytest, and run on every push via GitHub Actions.

## Test Cases

- `test_positive_submission` – Valid PDF, valid email, existing recipient. Should pass.
- `test_no_file_selected_bug` – Submitting without a file. Expected to fail (Bug #2).
- `test_non_pdf_file_bug` – Uploading .txt file. Expected to fail (Bug #3).
- `test_invalid_email_bug` – Email without "@". Expected to fail (Bug #6).

## How to Run Locally

1. Clone the repository.
2. Install dependencies: `pip install -r tests/requirements.txt`
3. Ensure `tests/test_files/valid.pdf` exists (any small PDF) and `invalid.txt` exists.
4. Run: `pytest tests/test_esign.py -v`

## GitHub Actions

The workflow is defined in `.github/workflows/run-tests.yml`.  
Latest run results can be seen in the **Actions** tab of this repository.
