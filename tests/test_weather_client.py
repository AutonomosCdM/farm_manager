import os
from dotenv import load_dotenv
from src.weather_client import ChileanWeatherClient

def test_weather_client():
    # Load environment variables
    load_dotenv()
    
    # Check if AgroMonitoring API key is available
    agromonitoring_api_key = os.getenv('AGROMONITORING_API_KEY')
    if not agromonitoring_api_key:
        print("⚠️ AgroMonitoring API key not found. Skipping test.")
        return
    
    # Initialize the weather client
    client = ChileanWeatherClient()
    
    # Test regions to check
    test_regions = [
        "Metropolitana",  # Capital region
        "Biobío",         # Southern region
        "Antofagasta"     # Northern region
    ]
    
    print("🌦️ Chilean Weather Client Test 🌦️")
    print("===================================")
    
    for region in test_regions:
        print(f"\nTesting weather data for {region} region:")
        weather_data = client.get_weather_by_region(region)
        
        if weather_data:
            print("✅ Weather data retrieved successfully:")
            for key, value in weather_data.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Failed to retrieve weather data for {region}")
    
    # Test invalid region
    print("\nTesting invalid region:")
    invalid_region_result = client.get_weather_by_region("Invalid Region")
    assert invalid_region_result is None, "Invalid region should return None"
    print("✅ Invalid region handling works correctly")

if __name__ == "__main__":
    test_weather_client()
