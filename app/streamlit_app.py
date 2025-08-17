import streamlit as st
import requests
import json
import re
import sys
import os
from pathlib import Path

# Add parent directory to Python path so we can import utils
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from utils.env_loader import load_env

load_env(override=True)

def validate_phone_number(phone_number):
    """Basic phone number validation"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone_number)
    
    # Check if it's a valid length (10-15 digits)
    if len(digits_only) < 10 or len(digits_only) > 15:
        return False, "Phone number must be 10-15 digits long"
    
    # Add + prefix if not present
    if not phone_number.startswith('+'):
        if len(digits_only) == 10:
            # Assume US number
            formatted = f"+1{digits_only}"
        else:
            formatted = f"+{digits_only}"
    else:
        formatted = phone_number
    
    return True, formatted

def main():
    st.set_page_config(
        page_title="RealTime Voice Agent",
        page_icon="📞",
        layout="centered"
    )
    
    st.title("📞 RealTime Voice Agent")
    st.markdown("Enter your phone number to receive a call from our AI voice agent")
    
    # Phone number input
    phone_number = st.text_input(
        "Phone Number",
        placeholder="Enter your phone number (e.g., +1234567890)",
        help="Include country code (e.g., +1 for US numbers)"
    )
    
    # Call button
    if st.button("📞 Call Me", type="primary", use_container_width=True):
        if not phone_number:
            st.error("Please enter a phone number")
            return
        
        # Validate phone number
        is_valid, formatted_number = validate_phone_number(phone_number)
        
        if not is_valid:
            st.error(f"Invalid phone number: {formatted_number}")
            return
        
        # Show loading spinner
        with st.spinner("Initiating call..."):
            try:
                # Make API call to backend
                response = requests.post(
                    "http://localhost:8000/initiate-call",
                    json={"phone_number": formatted_number},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        st.success(f"Call initiated successfully! You should receive a call at {formatted_number} shortly.")
                        st.info("Call SID: " + data.get("call_sid", "Unknown"))
                    else:
                        st.error(f"Failed to initiate call: {data.get('error', 'Unknown error')}")
                else:
                    st.error(f"API request failed: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API server. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Instructions
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("""
    1. Enter your phone number in the format: +[country code][number]
    2. Click "Call Me" to initiate the call
    3. Answer the call and speak your query
    4. The AI will process your question and respond via voice
    5. Have a natural conversation with the AI assistant
    """)
    
    st.markdown("### Examples of phone number formats:")
    st.markdown("""
    - US: +12345678901
    - UK: +441234567890
    - India: +919876543210
    """)

if __name__ == "__main__":
    main()