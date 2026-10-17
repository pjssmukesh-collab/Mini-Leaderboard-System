import pytest
from pages.upload_flow_page import UploadFlowPage
from config import Config

@pytest.mark.ui
@pytest.mark.upload
class TestResultsUpload:
    """Test suite for match results file upload, data validation, and processing pipeline."""

    def test_upload_page_loads_correctly(self, authenticated_creator):
        """Verify results upload dropzone and file input render properly."""
        upload_page = UploadFlowPage(authenticated_creator)
        upload_page.open_upload_page(event_id=1)
        
        assert upload_page.is_page_loaded(), "Results upload page failed to load for event 1."
        assert upload_page.is_visible(upload_page.FILE_INPUT), "File input element is missing."
        assert upload_page.is_visible(upload_page.UPLOAD_PARSE_BUTTON), "Upload button is missing."

    def test_upload_valid_csv_file_and_verify_validation(self, authenticated_creator):
        """Verify uploading valid results CSV triggers validation report with record counts."""
        upload_page = UploadFlowPage(authenticated_creator)
        upload_page.open_upload_page(event_id=1)
        
        valid_fixture = Config.FIXTURES_DIR / "valid_results.csv"
        assert valid_fixture.exists(), f"Fixture file not found: {valid_fixture}"
        
        upload_page.select_file(valid_fixture)
        upload_page.click_upload()
        
        # Step 2: Validate Data
        assert upload_page.is_validation_report_displayed(timeout=10), (
            "Validation report did not display after valid CSV upload."
        )

    def test_upload_invalid_csv_file_shows_error(self, authenticated_creator):
        """Verify uploading invalid results CSV triggers error message."""
        upload_page = UploadFlowPage(authenticated_creator)
        upload_page.open_upload_page(event_id=1)
        
        invalid_fixture = Config.FIXTURES_DIR / "invalid_results.csv"
        assert invalid_fixture.exists(), f"Fixture file not found: {invalid_fixture}"
        
        upload_page.select_file(invalid_fixture)
        upload_page.click_upload()
        
        # Should display extraction error fallback or alert
        assert upload_page.is_extraction_error_displayed(timeout=8) or upload_page.is_visible(upload_page.ERROR_ALERT), (
            "Extraction error was not displayed for invalid CSV missing player identifier."
        )
