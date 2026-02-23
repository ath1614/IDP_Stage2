#!/usr/bin/env python3
"""
Test NFRA VM Endpoints (OCR + LLM)
Complete test script with sample requests
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# VM Configuration
OCR_URL = "http://34.14.176.182:8000"
LLM_URL = "http://34.47.203.146:8000"

def create_sample_image():
    """Create a sample image with text for OCR testing"""
    # Create image with text
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add sample financial text
    text = """
    TECHCORP FINANCIAL SOLUTIONS LIMITED
    ANNUAL REPORT 2025-26
    
    Revenue: ₹450.5 Crores
    Net Profit: ₹78.45 Crores
    Total Assets: ₹1,245.8 Crores
    
    Auditor: Deloitte Haskins & Sells LLP
    Opinion: Unqualified
    """
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), text, fill='black', font=font)
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_b64

def test_ocr_health():
    """Test OCR health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: OCR Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{OCR_URL}/api/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ocr_single():
    """Test OCR with single image"""
    print("\n" + "="*60)
    print("TEST 2: OCR Single Image")
    print("="*60)
    
    try:
        # Create sample image
        print("Creating sample image...")
        image_b64 = create_sample_image()
        print(f"Image size: {len(image_b64)} bytes (base64)")
        
        # Send to OCR
        print("Sending to OCR service...")
        payload = {"image": image_b64}
        response = requests.post(
            f"{OCR_URL}/api/ocr",
            json=payload,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ OCR Success!")
            print(f"Extracted Text Length: {len(result.get('text', ''))}")
            print(f"Confidence: {result.get('confidence', 0)}")
            print(f"Processing Time: {result.get('processing_time_ms', 0)}ms")
            print(f"\nExtracted Text:")
            print("-" * 60)
            print(result.get('text', ''))
            print("-" * 60)
            return True
        else:
            print(f"❌ OCR Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llm_health():
    """Test LLM health endpoint"""
    print("\n" + "="*60)
    print("TEST 3: LLM Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{LLM_URL}/api/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llm_extract():
    """Test LLM extraction endpoint"""
    print("\n" + "="*60)
    print("TEST 4: LLM Financial Data Extraction")
    print("="*60)
    
    try:
        # Sample financial text
        text = """
        TechCorp Financial Solutions Limited reported strong performance for FY 2025-26.
        The company achieved revenue of 450.5 Crores, representing 15% year-over-year growth.
        Net profit stood at 78.45 Crores with a healthy margin of 17.4%.
        Total assets reached 1,245.8 Crores as of March 31, 2026.
        The financial statements were audited by Deloitte Haskins & Sells LLP,
        who issued an unqualified opinion confirming the accuracy of the statements.
        """
        
        schema = """
        Extract the following information in JSON format:
        - company_name: Full company name
        - fiscal_year: Fiscal year
        - revenue: Revenue amount with unit
        - profit: Net profit amount with unit
        - assets: Total assets with unit
        - auditor_name: Name of auditing firm
        - audit_opinion: Type of audit opinion
        """
        
        print("Input Text:")
        print("-" * 60)
        print(text.strip())
        print("-" * 60)
        
        print("\nSending to LLM service...")
        payload = {
            "text": text,
            "schema": schema
        }
        
        response = requests.post(
            f"{LLM_URL}/api/extract",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ LLM Extraction Success!")
            print(f"\nExtracted Data:")
            print("-" * 60)
            print(json.dumps(result.get('result', {}), indent=2))
            print("-" * 60)
            print(f"\nToken Usage:")
            print(f"  Input Tokens: {result.get('usage', {}).get('input_tokens', 0)}")
            print(f"  Output Tokens: {result.get('usage', {}).get('output_tokens', 0)}")
            return True
        else:
            print(f"❌ LLM Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llm_generate():
    """Test LLM text generation endpoint"""
    print("\n" + "="*60)
    print("TEST 5: LLM Text Generation")
    print("="*60)
    
    try:
        prompt = """
        Explain why a company with the following metrics is financially healthy:
        - Revenue: 450.5 Crores (15% YoY growth)
        - Net Profit: 78.45 Crores (17.4% margin)
        - Total Assets: 1,245.8 Crores
        
        Provide a 2-3 sentence explanation.
        """
        
        print("Prompt:")
        print("-" * 60)
        print(prompt.strip())
        print("-" * 60)
        
        print("\nSending to LLM service...")
        payload = {
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{LLM_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ LLM Generation Success!")
            print(f"\nGenerated Text:")
            print("-" * 60)
            print(result.get('text', ''))
            print("-" * 60)
            print(f"\nToken Usage:")
            print(f"  Input Tokens: {result.get('usage', {}).get('input_tokens', 0)}")
            print(f"  Output Tokens: {result.get('usage', {}).get('output_tokens', 0)}")
            return True
        else:
            print(f"❌ LLM Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("NFRA VM ENDPOINT TESTING")
    print("="*60)
    print(f"OCR VM: {OCR_URL}")
    print(f"LLM VM: {LLM_URL}")
    
    results = {
        "OCR Health": test_ocr_health(),
        "OCR Single Image": test_ocr_single(),
        "LLM Health": test_llm_health(),
        "LLM Extract": test_llm_extract(),
        "LLM Generate": test_llm_generate()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! VMs are working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check VM status.")

if __name__ == "__main__":
    run_all_tests()
