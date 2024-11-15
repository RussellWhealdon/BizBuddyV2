import streamlit as st
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Initialize the Google Ads client using st.secrets
def initialize_client():
    # Load credentials from Streamlit secrets
    credentials_info = st.secrets["google_ads"]

    # Create Google Ads Client Configuration in memory
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    
    client = GoogleAdsClient.load_from_dict({
        "developer_token": credentials_info["developer_token"],
        "login_customer_id": credentials_info["login_customer_id"],
        "use_proto_plus": True,
        "path_to_private_key_file": credentials_info["private_key_path"],  # Optional
    }, credentials=credentials)
    
    return client

# Test query to fetch Google Ads account information
def test_google_ads_connection(client, customer_id):
    query = """
        SELECT
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.tracking_url_template
        FROM customer
        LIMIT 1
    """
    
    try:
        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search(customer_id=customer_id, query=query)
        
        # Display the response in the Streamlit app
        for row in response:
            st.write(f"Customer ID: {row.customer.id}")
            st.write(f"Descriptive Name: {row.customer.descriptive_name}")
            st.write(f"Currency Code: {row.customer.currency_code}")
            st.write(f"Time Zone: {row.customer.time_zone}")
            st.write(f"Tracking URL Template: {row.customer.tracking_url_template}")
    except GoogleAdsException as ex:
        st.error(f"Request failed due to Google Ads API exception: {ex.message}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app
def main():
    st.title("Google Ads API Test Connection")
    
    # Input for Customer ID
    customer_id = st.text_input("Enter Customer ID", placeholder="e.g., 1234567890")
    
    if st.button("Test Connection"):
        if not customer_id:
            st.error("Please enter a valid Customer ID.")
        else:
            st.info("Initializing Google Ads Client...")
            client = initialize_client()
            
            st.info("Testing connection to Google Ads API...")
            test_google_ads_connection(client, customer_id)

if __name__ == "__main__":
    main()
