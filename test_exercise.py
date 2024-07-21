from playwright.sync_api import sync_playwright, expect
import re

def test_exercise():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        expect(page).to_have_title(re.compile("Swag Labs"))
        # to fill texts in boxes
        page.fill("//input[@id='user-name']", "standard_user")
        page.fill("//input[@id='password']", "secret_sauce")
        #to click on the login button
        page.click("//input[@id='login-button']")
        # to click on the backpack button
        expect(page.locator("//button[@id='add-to-cart-sauce-labs-backpack']")).to_have_text('Add to cart')
        page.click("//button[@id='add-to-cart-sauce-labs-backpack']")
        
        #to click on the bike button
        expect(page.locator("//button[@id='add-to-cart-sauce-labs-bike-light']")).to_have_text('Add to cart')
        page.click("//button[@id='add-to-cart-sauce-labs-bike-light']")

        #to click on the tshirt button
        
        expect(page.locator("//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")).to_have_text('Add to cart')
        page.click("//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")
        # We remove the backpack by verifying before that it says Remove on the button
        
        expect(page.locator("//button[@id='remove-sauce-labs-backpack']")).to_have_text('Remove')
        page.click("//button[@id='remove-sauce-labs-backpack']")
        # We verify that it says add to cart again
        expect(page.locator("//button[@id='add-to-cart-sauce-labs-backpack']")).to_have_text('Add to cart')
       
        #click on the shopping cart
        cart_selector = "[data-test='shopping-cart-link']"
        page.click(cart_selector)
        #We verify that the cart page is correct
        expect(page).to_have_url("https://www.saucedemo.com/cart.html")
        
        #We click on checkout
        page.click("//button[@id='checkout']")
        
        #We click on continue (empty)
        continue_button_selector = "//input[@id='continue']"
        page.click(continue_button_selector) 
        
        #We verify that the error message appears with the correct text
        error_message_selector = 'h3[data-test="error"]'
        error_message_text = "Error: First Name is required"

        # we check that the error message is visible
        error_message_locator = page.locator(error_message_selector)
        expect(error_message_locator).to_be_visible()
        
        # Verify that the error message contains the expected text        
        expect(error_message_locator).to_have_text(error_message_text)

        # Fill in personal information 
        page.fill("//input[@id='first-name']", "Periquito")
        page.fill("//input[@id='last-name']", "Palote")
        page.fill("//input[@id='postal-code']", "47574")

        #We click on continue (it is filled)
        continue_button_selector = "//input[@id='continue']"
        page.click(continue_button_selector)
        
        # We calculate the price of the ticket
        subtotal_selector = 'div[data-test="subtotal-label"]'
        tax_selector = 'div[data-test="tax-label"]'
        total_selector = 'div[data-test="total-label"]'

        subtotal_text = page.locator(subtotal_selector).text_content()
        tax_text = page.locator(tax_selector).text_content()
        total_text = page.locator(total_selector).text_content()

        def extract_amount(text):
            match = re.search(r'\$([0-9,.]+)', text)
            if match:
                return float(match.group(1).replace(',', ''))
            return 0.0

        subtotal_amount = extract_amount(subtotal_text)
        tax_amount = extract_amount(tax_text)
        total_amount = extract_amount(total_text)

        expected_total = subtotal_amount + tax_amount

        assert abs(total_amount - expected_total) < 0.01, f"Expected total: {expected_total}, but got: {total_amount}"
        
        #We press the Finish button
        page.click("//button[@id='finish']")

        # confirm that the message is "Thank you for your order!"
        confirmation_message_selector = 'h2.complete-header[data-test="complete-header"]'
        expect(page.locator(confirmation_message_selector)).to_have_text("Thank you for your order!")

        #We press the button to return
        page.click("//button[@id='back-to-products']")
        #click on the menu
        page.click("//button[@id='react-burger-menu-btn']")
        # Click the logout button
        logout_selector = "[data-test='logout-sidebar-link']"
        page.click(logout_selector)
        
        # Verify that user fields are visible
        username_selector = 'input[data-test="username"]'
        password_selector = 'input[data-test="password"]'
        
        expect(page.locator(username_selector)).to_be_visible()
        expect(page.locator(password_selector)).to_be_visible()
        
        #Change time value (seconds) for debugging purposes.
        time.sleep(500)
