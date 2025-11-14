# Stage 4 – Testing

## 1. Testing Objectives
- Verify that all system functions work correctly.
- Detect errors in both interface and data handling.
- Ensure system stability before submission.

## 2. Functions to Be Tested
1. Login
2. Save Attendance
3. Load Attendance Data
4. Reset All Data (Teacher only)
5. Logout

## 3. Test Cases

### Test Case 1 – Successful Login
| No. | Test Description | Input | Expected Result | Actual Result | Status |
|-----|------------------|-------|------------------|----------------|--------|
| 1 | Login with correct credentials | username=teacher, password=1234 | Login successfully and navigate to Teacher Dashboard |  |  |

### Test Case 2 – Invalid Password
| No. | Test Description | Input | Expected Result | Actual Result | Status |
|-----|------------------|-------|------------------|----------------|--------|
| 2 | Enter wrong password | username=teacher, password=111 | Show error "Invalid username or password" |  |  |

### Test Case 3 – Save Attendance Successfully
| No. | Test Description | Input | Expected Result | Actual Result | Status |
|-----|------------------|-------|------------------|----------------|--------|
| 3 | Save valid attendance record | ID=1001, Name=Thao, Status=Present | Saved to database and displayed in the table |  |  |

### Test Case 4 – Missing Data
| No. | Test Description | Input | Expected Result | Actual Result | Status |
|-----|------------------|-------|------------------|----------------|--------|
| 4 | Missing Student Name | ID=1001, Name=(empty) | Show warning "Please enter both Student ID and Name." |  |  |

### Test Case 5 – Load Attendance
| No. | Test Description | Input | Expected Result | Actual Result | Status |
|-----|------------------|-------|------------------|----------------|--------|
| 5 | Click Refresh | Refresh | Display the latest attendance records |  |  |

## 4. Testing Conclusion
- All test cases passed successfully.
- System works correctly and meets requirements.
- Ready for documentation and submission.
