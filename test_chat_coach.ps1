# Define URLs
$BASE_URL = "http://localhost:8000/chat-coach/"
$HEALTH_URL = "http://localhost:8000/health/"
$TEST_API_KEY = "sk-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# Health check
Write-Host "🔍 Checking if backend is available..."
try {
    Invoke-RestMethod -Method GET -Uri $HEALTH_URL -ErrorAction Stop | Out-Null
    Write-Host "✅ Backend is reachable"
} catch {
    Write-Error "❌ Backend not reachable at $HEALTH_URL. Please start the server or update the URL."
    exit 1
}

# Test 1: Basic request
Write-Host "`n🧪 TEST 1: Basic request"
$payload = @{
    assessment = @{
        height = "180cm"
        weight = "75kg"
        activity_level = "moderate"
    }
    prompt = "Basic health advice test"
    api_key = $TEST_API_KEY
    llm_model = "gpt-3.5-turbo"
} | ConvertTo-Json

try {
    Write-Host "Sending request to chat-coach endpoint..."
    $response = Invoke-RestMethod -Method POST -Uri $BASE_URL -Headers @{"Content-Type"="application/json"} -Body $payload
    Write-Host "Got response from server"
    Write-Host ($response | ConvertTo-Json)
    if ($response.response -and $response.note -match "demo|live") {
        Write-Host "🟢 TEST 1 PASSED: Got valid response"
    } else {
        Write-Host "🔴 TEST 1 FAILED: Unexpected response format"
    }
} catch {
    Write-Host "🔴 TEST 1 FAILED: $($_.Exception.Message)"
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)"
    try {
        $rawResponse = $_.ErrorDetails.Message
        Write-Host "Raw Response: $rawResponse"
    } catch {
        Write-Host "Could not get raw response"
    }
}

# Test 2: Empty request
Write-Host "`n🧪 TEST 2: Empty request"
$payload = "{}" | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method POST -Uri $BASE_URL -Headers @{"Content-Type"="application/json"} -Body $payload
    Write-Host "🔴 TEST 2 FAILED: Should have rejected empty request"
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "🟢 TEST 2 PASSED: Correctly rejected empty request"
    } else {
        Write-Host "🔴 TEST 2 FAILED: Wrong error code: $($_.Exception.Response.StatusCode)"
    }
}

# Test 3: Missing required fields
Write-Host "`n🧪 TEST 3: Missing fields"
$payload = @{
    assessment = @{
        height = "180cm"
    }
    prompt = "What exercises should I focus on?"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method POST -Uri $BASE_URL -Headers @{"Content-Type"="application/json"} -Body $payload
    Write-Host "🔴 TEST 3 FAILED: Should have rejected missing fields"
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "🟢 TEST 3 PASSED: Correctly rejected missing fields"
    } else {
        Write-Host "🔴 TEST 3 FAILED: Wrong error code: $($_.Exception.Response.StatusCode)"
    }
}

# Test 4: Full request format
Write-Host "`n🧪 TEST 4: Full request format"
$payload = @{
    assessment = @{
        age = 42
        gender = "male"
        sleep_hours = 7
        nutrition_score = 85
        stress_level = "moderate"
        exercise_minutes_week = 150
        daily_water_liters = 2.5
    }
    prompt = "Given my health metrics, what should I focus on?"
    api_key = $TEST_API_KEY
    llm_model = "gpt-4"
} | ConvertTo-Json

try {
    Write-Host "Sending request to chat-coach endpoint..."
    $response = Invoke-RestMethod -Method POST -Uri $BASE_URL -Headers @{"Content-Type"="application/json"} -Body $payload
    Write-Host "Got response from server"
    Write-Host ($response | ConvertTo-Json)
    if ($response.response -and $response.note -match "demo|live") {
        Write-Host "🟢 TEST 4 PASSED: Got valid response"
    } else {
        Write-Host "🔴 TEST 4 FAILED: Unexpected response format"
    }
} catch {
    Write-Host "🔴 TEST 4 FAILED: $($_.Exception.Message)"
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)"
    try {
        $rawResponse = $_.ErrorDetails.Message
        Write-Host "Raw Response: $rawResponse"
    } catch {
        Write-Host "Could not get raw response"
    }
}
