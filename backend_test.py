import requests
import sys
import base64
import io
from datetime import datetime
from PIL import Image
import json

class WeaponDetectionTester:
    def __init__(self, base_url="https://easy-weapon-scan.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            response_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text

            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response_data}")

            self.test_results.append({
                "test_name": name,
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response": response_data
            })

            return success, response_data

        except requests.RequestException as e:
            print(f"❌ Failed - Request Error: {str(e)}")
            self.test_results.append({
                "test_name": name,
                "success": False,
                "error": str(e)
            })
            return False, {}

    def create_test_image(self):
        """Create a simple test image in base64 format"""
        # Create a simple 100x100 RGB image with some content
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test(
            "API Root Endpoint",
            "GET", 
            "api/",
            200
        )

    def test_stats_endpoint(self):
        """Test stats endpoint"""
        success, response = self.run_test(
            "System Stats Endpoint",
            "GET",
            "api/stats",
            200
        )
        
        if success:
            required_fields = ['total_detections', 'gun_count', 'knife_count', 'phone_count', 'uptime']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"⚠️  Warning: Missing fields in stats response: {missing_fields}")
            else:
                print("✅ All required stats fields present")
                
        return success

    def test_detect_endpoint(self):
        """Test detection endpoint with base64 image"""
        test_image = self.create_test_image()
        
        success, response = self.run_test(
            "Detection Endpoint",
            "POST",
            "api/detect",
            200,
            data={"image": test_image},
            timeout=60  # Detection might take longer
        )
        
        if success:
            required_fields = ['detections', 'total_count', 'has_weapon', 'timestamp']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"⚠️  Warning: Missing fields in detection response: {missing_fields}")
            else:
                print("✅ All required detection fields present")
                print(f"   Detections found: {response.get('total_count', 0)}")
                print(f"   Has weapon: {response.get('has_weapon', False)}")
                
        return success

    def test_recent_detections_endpoint(self):
        """Test recent detections endpoint"""
        success, response = self.run_test(
            "Recent Detections Endpoint",
            "GET",
            "api/recent-detections",
            200
        )
        
        if success:
            if 'detections' in response:
                print(f"✅ Recent detections returned: {len(response['detections'])} items")
            else:
                print("⚠️  Warning: No 'detections' field in response")
                
        return success

def main():
    print("🎯 Starting Weapon Detection API Tests")
    print("=" * 50)
    
    tester = WeaponDetectionTester()

    # Test all endpoints
    print("\n📡 Testing API Endpoints...")
    tester.test_root_endpoint()
    tester.test_stats_endpoint()
    tester.test_recent_detections_endpoint()
    tester.test_detect_endpoint()

    # Print overall results
    print("\n" + "=" * 50)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {tester.tests_run - tester.tests_passed} tests failed")
        
        # Print failed tests
        print("\n❌ Failed tests:")
        for result in tester.test_results:
            if not result['success']:
                print(f"   - {result['test_name']}")
                if 'error' in result:
                    print(f"     Error: {result['error']}")
                elif 'status_code' in result:
                    print(f"     Status: {result['status_code']} (expected {result['expected_status']})")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())