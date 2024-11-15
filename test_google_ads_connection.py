import streamlit as st
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Initialize the Google Ads client using st.secrets
def initialize_client():
    credentials_info = st.secrets["google_ads"]
    
    client = GoogleAdsClient.load_from_dict({
        "developer_token": credentials_info["developer_token"],
        "login_customer_id": credentials_info["login_customer_id"],
        "use_proto_plus": True
    })
    return client

def test_google_ads_connection(client):
    customer_id = st.secrets["google_ads"]["customer_id"]  # Fetch Customer ID from secrets
    query = """
        SELECT
            customer.id,
            customer.descriptive_name
        FROM customer
        LIMIT 1
    """
    try:
        service = client.get_service("GoogleAdsService")
        response = service.search(customer_id=customer_id, query=query)
        for row in response:
            st.write(f"Customer ID: {row.customer.id}")
            st.write(f"Descriptive Name: {row.customer.descriptive_name}")
    except GoogleAdsException as ex:
        st.error(f"Google Ads API Exception: {ex.message}")

def main():
    st.title("Google Ads API Test Connection")
    st.info("Testing API Connection...")
    client = initialize_client()
    test_google_ads_connection(client)

if __name__ == "__main__":
    main()
