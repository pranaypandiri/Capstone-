@echo off
REM Customer Communicator Agent - Flask API Testing Commands

echo.
echo ======================================================================
echo CUSTOMER COMMUNICATOR AGENT - FLASK API TEST COMMANDS
echo ======================================================================
echo.
echo Server must be running at http://127.0.0.1:5000
echo.

:menu
echo.
echo Select a test:
echo   1 - Health Check
echo   2 - Agent Status
echo   3 - Generate Single Message
echo   4 - Batch Generate (2 messages)
echo   5 - Validate Message
echo   Q - Quit
echo.
set /p choice="Enter choice [1-5, Q]: "

if /i "%choice%"=="1" goto health
if /i "%choice%"=="2" goto status
if /i "%choice%"=="3" goto single
if /i "%choice%"=="4" goto batch
if /i "%choice%"=="5" goto validate
if /i "%choice%"=="Q" goto end
echo Invalid choice. Please try again.
goto menu

:health
echo.
echo [Test 1] Health Check
echo GET http://127.0.0.1:5000/health
echo.
curl -X GET http://127.0.0.1:5000/health
echo.
echo.
goto menu

:status
echo.
echo [Test 2] Agent Status
echo GET http://127.0.0.1:5000/api/v1/status
echo.
curl -X GET http://127.0.0.1:5000/api/v1/status
echo.
echo.
goto menu

:single
echo.
echo [Test 3] Generate Single Message
echo POST http://127.0.0.1:5000/api/v1/generate-message
echo.
curl -X POST http://127.0.0.1:5000/api/v1/generate-message ^
  -H "Content-Type: application/json" ^
  -d "{\"customer_profile\": {\"KNA1\": {\"customer_id\": \"100034\", \"name\": \"Acme\", \"email\": \"anita.rao@acmeretail.example\", \"phone\": \"+91-80-5555-1100\"}, \"KNVV\": {\"currency\": \"INR\"}}, \"resolution_plan\": {\"complaint_id\": \"CMP-2025-00089\", \"category\": \"Delivery Delay\", \"description\": \"Order delayed in transit\", \"actions\": [{\"action_type\": \"Expedite\", \"carrier\": \"BlueDart\", \"delivery_date\": \"2025-11-28\"}]}, \"credit_confirmation\": {\"approval_status\": \"approved\", \"goodwill_credit\": {\"amount\": 2299.50, \"currency\": \"INR\"}}}"
echo.
echo.
goto menu

:batch
echo.
echo [Test 4] Batch Generate (2 messages)
echo POST http://127.0.0.1:5000/api/v1/batch-generate
echo.
echo This will process 2 customer messages...
echo Check terminal for detailed logs
echo.
curl -X POST http://127.0.0.1:5000/api/v1/batch-generate ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\": [{\"customer_profile\": {\"KNA1\": {\"customer_id\": \"100034\", \"name\": \"Acme\", \"email\": \"anita.rao@acmeretail.example\", \"phone\": \"+91-80-5555-1100\"}, \"KNVV\": {\"currency\": \"INR\"}}, \"resolution_plan\": {\"complaint_id\": \"CMP-2025-00089\", \"category\": \"Delivery Delay\", \"actions\": [{\"action_type\": \"Expedite\", \"carrier\": \"BlueDart\", \"delivery_date\": \"2025-11-28\"}]}, \"credit_confirmation\": {\"approval_status\": \"approved\", \"goodwill_credit\": {\"amount\": 2299.50, \"currency\": \"INR\"}}}, {\"customer_profile\": {\"KNA1\": {\"customer_id\": \"100035\", \"name\": \"Beta Corp\", \"email\": \"contact@betacorp.example\", \"phone\": \"+91-80-5555-1101\"}, \"KNVV\": {\"currency\": \"INR\"}}, \"resolution_plan\": {\"complaint_id\": \"CMP-2025-00090\", \"category\": \"Quality Issue\", \"actions\": [{\"action_type\": \"Replace\", \"quantity\": 5}]}, \"credit_confirmation\": {\"approval_status\": \"approved\", \"goodwill_credit\": {\"amount\": 1500.00, \"currency\": \"INR\"}}}]}"
echo.
echo.
goto menu

:validate
echo.
echo [Test 5] Validate Message
echo POST http://127.0.0.1:5000/api/v1/validate
echo.
curl -X POST http://127.0.0.1:5000/api/v1/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Dear Acme,\nWe sincerely apologize for the delay in delivering your order with Complaint ID CMP-2025-00089. We understand how important timely delivery is for your organization, and we regret the inconvenience this may have caused.\n\nWe have been in touch with our carrier partner, BlueDart, and your shipment is now scheduled to reach you by 2025-11-28. To express our commitment to your satisfaction, we have issued a goodwill credit of 2,299.50 INR to your account.\n\nThank you for your patience and understanding.\", \"context\": {\"customer_id\": \"100034\", \"complaint_id\": \"CMP-2025-00089\", \"category\": \"Delivery Delay\"}}"
echo.
echo.
goto menu

:end
echo.
echo Exiting...
echo.
exit /b
