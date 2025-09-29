# Test Case Generation Template

## 🎯 Purpose
Generate comprehensive test cases and scenarios for fintech applications with focus on functionality, security, and compliance.

## 📝 Template

```
Act as a senior QA engineer specializing in fintech applications. Generate comprehensive test cases for the following specification:

**Application Under Test:**
- Feature/Module: [FEATURE_NAME]
- Application Type: [WEB/MOBILE/API/DESKTOP]
- User Roles: [ROLES_AND_PERMISSIONS]
- Business Rules: [SPECIFIC_BUSINESS_LOGIC]
- Compliance Requirements: [REGULATORY_STANDARDS]

**Functional Requirements:**
[DETAILED_FUNCTIONAL_REQUIREMENTS]

**Non-Functional Requirements:**
- Performance: [RESPONSE_TIME/THROUGHPUT_REQUIREMENTS]
- Security: [AUTHENTICATION/AUTHORIZATION/ENCRYPTION]
- Usability: [USER_EXPERIENCE_REQUIREMENTS]
- Compatibility: [BROWSER/DEVICE/OS_SUPPORT]
- Scalability: [CONCURRENT_USER_LIMITS]

**Test Environment:**
- Test Data: [DATA_REQUIREMENTS]
- Integration Points: [EXTERNAL_SYSTEMS]
- Mock Services: [SERVICES_TO_MOCK]
- Test Databases: [DATABASE_SETUP]

**Generate test cases covering:**

## 1. Functional Test Cases
For each test case, provide:
- **Test Case ID**: [Unique identifier]
- **Test Case Title**: [Descriptive title]
- **Test Category**: [Smoke/Regression/Integration/etc]
- **Priority**: [High/Medium/Low]
- **Preconditions**: [Setup requirements]
- **Test Steps**: [Detailed step-by-step instructions]
- **Expected Results**: [Expected outcomes]
- **Test Data**: [Required test data]
- **Dependencies**: [Other test cases or systems]

## 2. Negative Test Cases
- Invalid input validation
- Boundary value testing
- Error handling scenarios
- Exception flow testing
- Security breach attempts

## 3. Edge Cases and Boundary Testing
- Minimum and maximum values
- Empty/null data handling
- Special characters and Unicode
- Large dataset processing
- Concurrent user scenarios

## 4. Security Test Cases
- Authentication bypass attempts
- Authorization validation
- Input sanitization testing
- SQL injection prevention
- Cross-site scripting (XSS) prevention
- Data encryption validation
- Session management testing

## 5. Performance Test Cases
- Response time validation
- Load testing scenarios
- Stress testing conditions
- Volume testing with large datasets
- Memory and resource usage

## 6. Compliance Test Cases
- PCI DSS validation (if applicable)
- GDPR data handling compliance
- Audit trail verification
- Data retention policy testing
- Privacy controls validation

## 7. Integration Test Cases
- API integration testing
- Database connectivity
- Third-party service integration
- File upload/download testing
- Email/SMS notification validation

## 8. User Experience Test Cases
- Navigation flow testing
- Responsive design validation
- Accessibility compliance (WCAG)
- Cross-browser compatibility
- Mobile responsiveness

**Test Case Format:**
Use a structured format with clear sections:
- Objective and scope
- Test environment setup
- Detailed test steps
- Expected vs actual results
- Pass/fail criteria
- Notes and observations

**Include test automation recommendations:**
- Which test cases are good candidates for automation
- Suggested automation tools and frameworks
- Test data management strategies
- Maintenance considerations
```

## 🔧 Usage Examples

### Example 1: Payment Processing Feature

```
Act as a senior QA engineer specializing in fintech applications. Generate comprehensive test cases for the following specification:

**Application Under Test:**
- Feature/Module: Credit Card Payment Processing
- Application Type: Web Application with API backend
- User Roles: Customer, Merchant, Admin, Support Agent
- Business Rules: $0.50 minimum, $10,000 maximum per transaction, fraud detection, PCI compliance
- Compliance Requirements: PCI DSS Level 1, PSD2, GDPR

**Functional Requirements:**
- Accept major credit cards (Visa, MasterCard, Amex, Discover)
- Real-time payment processing with Stripe integration
- Automatic fraud detection and prevention
- Transaction confirmation and receipt generation
- Refund processing capability
- Multi-currency support (USD, EUR, GBP)

**Non-Functional Requirements:**
- Performance: <3 seconds payment processing, 1000 TPS capacity
- Security: TLS 1.3 encryption, tokenization, no card data storage
- Usability: Mobile-responsive, accessible (WCAG 2.1 AA)
- Compatibility: Chrome 90+, Firefox 88+, Safari 14+, iOS 14+, Android 10+
- Scalability: Support 100,000 concurrent users during peak hours

**Test Environment:**
- Test Data: Valid/invalid card numbers, expired cards, declined cards
- Integration Points: Stripe API, fraud detection service, email service
- Mock Services: Bank simulator, fraud detection service
- Test Databases: PostgreSQL with test transaction data
```

### Example 2: User Registration and KYC

```
**Application Under Test:**
- Feature/Module: User Registration with KYC Verification
- Application Type: Mobile App (iOS/Android) with web portal
- User Roles: New User, Existing User, KYC Officer, Compliance Officer
- Business Rules: 18+ years old, government ID required, address verification, risk scoring
- Compliance Requirements: KYC/AML regulations, GDPR, data localization

**Functional Requirements:**
- Multi-step registration process
- Document upload and verification (ID, proof of address)
- Biometric verification (selfie with ID)
- Real-time identity verification with third-party service
- Risk assessment and scoring
- Manual review workflow for edge cases
- Account activation upon KYC completion

**Non-Functional Requirements:**
- Performance: <30 seconds for identity verification
- Security: Document encryption, biometric data protection
- Usability: Intuitive mobile experience, accessibility support
- Compatibility: iOS 13+, Android 9+, mobile web browsers
```

## ✅ Expected Output Components

When using this template, AI should generate:

1. **Comprehensive Test Suite** with 50-100+ test cases
2. **Functional Test Cases** covering all requirements
3. **Negative Test Scenarios** for error handling
4. **Security Test Cases** for vulnerability assessment
5. **Performance Test Cases** with benchmarks
6. **Compliance Test Cases** for regulatory requirements
7. **Integration Test Cases** for system interactions
8. **User Experience Test Cases** for usability
9. **Test Data Requirements** with sample data
10. **Automation Recommendations** with priorities

## 🎯 Test Case Categories

### Priority Levels:
- **P0 (Critical)**: Core functionality, security, compliance
- **P1 (High)**: Important features, error handling
- **P2 (Medium)**: Enhanced features, edge cases
- **P3 (Low)**: Nice-to-have features, cosmetic issues

### Test Types:
- **Smoke Tests**: Basic functionality validation
- **Regression Tests**: Existing functionality preservation
- **Integration Tests**: System component interactions
- **End-to-End Tests**: Complete user workflows
- **API Tests**: Backend service validation
- **Security Tests**: Vulnerability assessment
- **Performance Tests**: Load and stress testing

## 🔄 Test Case Management

### Best Practices:
1. **Clear and Concise**: Write clear, unambiguous test steps
2. **Maintainable**: Keep test cases updated with feature changes
3. **Traceable**: Link test cases to requirements
4. **Reusable**: Create modular test components
5. **Data-Driven**: Separate test logic from test data
6. **Risk-Based**: Prioritize based on business risk

### Test Execution Strategy:
- **Daily Smoke Tests**: Automated after each deployment
- **Sprint Regression**: Full regression before release
- **Performance Testing**: Weekly capacity validation
- **Security Testing**: Monthly vulnerability scans
- **Compliance Testing**: Quarterly regulatory validation

## 📊 Test Metrics and Reporting

### Key Metrics:
- **Test Coverage**: Percentage of requirements covered
- **Pass Rate**: Percentage of tests passing
- **Defect Density**: Defects per test case
- **Test Execution Time**: Duration for full test suite
- **Automation Coverage**: Percentage of automated tests

### Reporting:
- Daily test execution reports
- Weekly test coverage analysis
- Monthly quality metrics dashboard
- Quarterly compliance audit reports

## 🔒 Security Testing Focus

### Fintech-Specific Security Tests:
- **Payment Card Data**: PCI DSS validation
- **Authentication**: Multi-factor authentication testing
- **Authorization**: Role-based access control
- **Data Encryption**: At rest and in transit
- **API Security**: Rate limiting, input validation
- **Session Management**: Timeout and security
- **Fraud Detection**: Pattern recognition testing

## 📚 Related Templates

- [Automation Framework](./automation-framework.md)
- [Performance Testing](./performance-testing.md)
- [Security Testing](./security-testing.md)
- [API Testing](./api-testing.md)
- [Mobile Testing](./mobile-testing.md)