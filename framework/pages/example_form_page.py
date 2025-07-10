"""
Example form page object demonstrating advanced interactions.
Shows how to handle forms, dropdowns, checkboxes, and file uploads.
"""

from pathlib import Path
from typing import List, Optional

from selene import be, have
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from framework.core.base_page import BasePage
from framework.utils.helpers import DataGenerator
from framework.utils.logger import get_logger

logger = get_logger(__name__)


class ExampleFormPage(BasePage):
    """Example form page for demonstrating various form interactions."""

    def __init__(self):
        super().__init__(url_path="/form")

    # Form field locators
    FIRST_NAME_INPUT = '[name="firstName"]'
    LAST_NAME_INPUT = '[name="lastName"]'
    EMAIL_INPUT = '[name="email"]'
    PHONE_INPUT = '[name="phone"]'
    PASSWORD_INPUT = '[name="password"]'
    CONFIRM_PASSWORD_INPUT = '[name="confirmPassword"]'

    # Dropdown and selection elements
    COUNTRY_DROPDOWN = '[name="country"]'
    STATE_DROPDOWN = '[name="state"]'
    CITY_DROPDOWN = '[name="city"]'

    # Checkbox and radio elements
    GENDER_MALE_RADIO = '[name="gender"][value="male"]'
    GENDER_FEMALE_RADIO = '[name="gender"][value="female"]'
    TERMS_CHECKBOX = '[name="terms"]'
    NEWSLETTER_CHECKBOX = '[name="newsletter"]'

    # File upload
    FILE_UPLOAD = '[name="avatar"]'

    # Date picker
    DATE_OF_BIRTH = '[name="dateOfBirth"]'

    # Multi-select
    HOBBIES_SELECT = '[name="hobbies"]'

    # Buttons
    SUBMIT_BUTTON = '[type="submit"]'
    RESET_BUTTON = '[type="reset"]'
    CANCEL_BUTTON = ".cancel-btn"

    # Success/Error messages
    SUCCESS_MESSAGE = ".success-message"
    ERROR_MESSAGE = ".error-message"
    FIELD_ERRORS = ".field-error"

    def fill_personal_info(
        self, first_name: str, last_name: str, email: str, phone: str = ""
    ) -> "ExampleFormPage":
        """
        Fill personal information fields.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number (optional)

        Returns:
            Self for method chaining
        """
        logger.info("Filling personal information")

        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.EMAIL_INPUT, email)

        if phone:
            self.type_text(self.PHONE_INPUT, phone)

        return self

    def set_password(
        self, password: str, confirm_password: Optional[str] = None
    ) -> "ExampleFormPage":
        """
        Set password fields.

        Args:
            password: Password
            confirm_password: Confirmation password (defaults to same as password)

        Returns:
            Self for method chaining
        """
        logger.info("Setting password")

        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, confirm_password or password)

        return self

    def select_country(self, country: str) -> "ExampleFormPage":
        """
        Select country from dropdown.

        Args:
            country: Country name

        Returns:
            Self for method chaining
        """
        logger.info(f"Selecting country: {country}")
        self.select_dropdown_by_text(self.COUNTRY_DROPDOWN, country)
        return self

    def select_state(self, state: str) -> "ExampleFormPage":
        """
        Select state from dropdown.

        Args:
            state: State name

        Returns:
            Self for method chaining
        """
        logger.info(f"Selecting state: {state}")
        self.select_dropdown_by_text(self.STATE_DROPDOWN, state)
        return self

    def select_city(self, city: str) -> "ExampleFormPage":
        """
        Select city from dropdown.

        Args:
            city: City name

        Returns:
            Self for method chaining
        """
        logger.info(f"Selecting city: {city}")
        self.select_dropdown_by_text(self.CITY_DROPDOWN, city)
        return self

    def select_gender(self, gender: str) -> "ExampleFormPage":
        """
        Select gender radio button.

        Args:
            gender: Gender ('male' or 'female')

        Returns:
            Self for method chaining
        """
        logger.info(f"Selecting gender: {gender}")

        if gender.lower() == "male":
            self.click_element(self.GENDER_MALE_RADIO)
        elif gender.lower() == "female":
            self.click_element(self.GENDER_FEMALE_RADIO)
        else:
            raise ValueError(f"Invalid gender: {gender}. Must be 'male' or 'female'")

        return self

    def set_date_of_birth(self, date: str) -> "ExampleFormPage":
        """
        Set date of birth.

        Args:
            date: Date in format YYYY-MM-DD

        Returns:
            Self for method chaining
        """
        logger.info(f"Setting date of birth: {date}")
        self.type_text(self.DATE_OF_BIRTH, date)
        return self

    def check_terms_and_conditions(self, accept: bool = True) -> "ExampleFormPage":
        """
        Check or uncheck terms and conditions checkbox.

        Args:
            accept: Whether to accept terms

        Returns:
            Self for method chaining
        """
        logger.info(f"Setting terms acceptance: {accept}")

        checkbox = self.find_element(self.TERMS_CHECKBOX)
        is_checked = checkbox.is_selected()

        if accept and not is_checked:
            checkbox.click()
        elif not accept and is_checked:
            checkbox.click()

        return self

    def subscribe_to_newsletter(self, subscribe: bool = True) -> "ExampleFormPage":
        """
        Subscribe or unsubscribe to newsletter.

        Args:
            subscribe: Whether to subscribe

        Returns:
            Self for method chaining
        """
        logger.info(f"Setting newsletter subscription: {subscribe}")

        checkbox = self.find_element(self.NEWSLETTER_CHECKBOX)
        is_checked = checkbox.is_selected()

        if subscribe and not is_checked:
            checkbox.click()
        elif not subscribe and is_checked:
            checkbox.click()

        return self

    def select_hobbies(self, hobbies: List[str]) -> "ExampleFormPage":
        """
        Select multiple hobbies from multi-select dropdown.

        Args:
            hobbies: List of hobby names

        Returns:
            Self for method chaining
        """
        logger.info(f"Selecting hobbies: {hobbies}")

        select_element = Select(self.find_element(self.HOBBIES_SELECT).locate())

        # Clear existing selections
        select_element.deselect_all()

        # Select new hobbies
        for hobby in hobbies:
            select_element.select_by_visible_text(hobby)

        return self

    def upload_file(self, file_path: str) -> "ExampleFormPage":
        """
        Upload a file.

        Args:
            file_path: Path to file to upload

        Returns:
            Self for method chaining
        """
        logger.info(f"Uploading file: {file_path}")

        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_input = self.find_element(self.FILE_UPLOAD)
        file_input.send_keys(str(Path(file_path).absolute()))

        return self

    def submit_form(self) -> "ExampleFormPage":
        """
        Submit the form.

        Returns:
            Self for method chaining
        """
        logger.info("Submitting form")
        self.click_element(self.SUBMIT_BUTTON)
        return self

    def reset_form(self) -> "ExampleFormPage":
        """
        Reset the form.

        Returns:
            Self for method chaining
        """
        logger.info("Resetting form")
        self.click_element(self.RESET_BUTTON)
        return self

    def cancel_form(self) -> "ExampleFormPage":
        """
        Cancel form submission.

        Returns:
            Self for method chaining
        """
        logger.info("Cancelling form")
        self.click_element(self.CANCEL_BUTTON)
        return self

    def get_success_message(self) -> str:
        """
        Get success message text.

        Returns:
            Success message text
        """
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""

    def get_error_message(self) -> str:
        """
        Get error message text.

        Returns:
            Error message text
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""

    def get_field_errors(self) -> List[str]:
        """
        Get all field error messages.

        Returns:
            List of field error messages
        """
        error_elements = self.find_elements(self.FIELD_ERRORS)
        errors = []

        for element in error_elements:
            try:
                error_text = element.get_text()
                if error_text:
                    errors.append(error_text)
            except Exception as e:
                logger.debug(f"Could not get error text: {e}")

        return errors

    def is_form_submitted_successfully(self) -> bool:
        """
        Check if form was submitted successfully.

        Returns:
            True if form submission was successful
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def has_validation_errors(self) -> bool:
        """
        Check if form has validation errors.

        Returns:
            True if form has validation errors
        """
        return self.is_element_visible(self.ERROR_MESSAGE) or self.is_element_visible(
            self.FIELD_ERRORS
        )

    def fill_form_with_test_data(
        self, data_generator: Optional[DataGenerator] = None
    ) -> "ExampleFormPage":
        """
        Fill form with generated test data.

        Args:
            data_generator: Data generator instance (optional)

        Returns:
            Self for method chaining
        """
        if not data_generator:
            data_generator = DataGenerator()

        logger.info("Filling form with generated test data")

        # Generate test data
        name_data = data_generator.random_name()
        email = data_generator.random_email()
        phone = data_generator.random_phone()

        # Fill form
        self.fill_personal_info(
            first_name=name_data["first_name"],
            last_name=name_data["last_name"],
            email=email,
            phone=phone,
        )

        self.set_password("TestPassword123!")
        self.select_gender("male")
        self.check_terms_and_conditions(True)
        self.subscribe_to_newsletter(True)

        return self
