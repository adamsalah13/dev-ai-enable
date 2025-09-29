# API Endpoint Generation Template

## 🎯 Purpose
Generate comprehensive API endpoints with proper error handling, validation, documentation, and tests for fintech applications.

## 📝 Template

```
Create a RESTful API endpoint for a fintech application with the following specifications:

**Endpoint Details:**
- Resource: [RESOURCE_NAME] (e.g., payments, transactions, users)
- HTTP Method: [GET/POST/PUT/DELETE]
- Path: [API_PATH] (e.g., /api/v1/payments)
- Description: [ENDPOINT_DESCRIPTION]

**Request Requirements:**
- Authentication: [JWT/API_KEY/OAuth2]
- Request Body Schema: [JSON_SCHEMA]
- Query Parameters: [PARAMETER_LIST]
- Headers: [REQUIRED_HEADERS]

**Response Requirements:**
- Success Response (200/201): [RESPONSE_SCHEMA]
- Error Responses: [ERROR_CODES_AND_MESSAGES]
- Pagination (if applicable): [PAGINATION_DETAILS]

**Business Logic:**
- [DETAILED_BUSINESS_REQUIREMENTS]
- [VALIDATION_RULES]
- [SECURITY_CONSIDERATIONS]

**Technical Requirements:**
- Framework: Express.js with TypeScript
- Database: PostgreSQL with Knex.js
- Validation: Joi schema validation
- Logging: Winston logger
- Rate Limiting: Express rate limit
- Error Handling: Centralized error middleware

**Compliance Requirements:**
- PCI DSS Level 1 compliance (if handling payment data)
- GDPR compliance for personal data
- Audit logging for all operations
- Input sanitization and XSS prevention

**Generate the following components:**

1. **Route Handler Function**
   - Proper async/await error handling
   - Input validation with detailed error messages
   - Business logic implementation
   - Database operations with transactions
   - Response formatting

2. **TypeScript Interfaces**
   - Request/Response type definitions
   - Database model interfaces
   - Error response types

3. **Joi Validation Schemas**
   - Request body validation
   - Query parameter validation
   - Custom validation rules

4. **Unit Tests**
   - Happy path scenarios
   - Validation error cases
   - Authentication/authorization tests
   - Database error handling
   - Mock external dependencies

5. **Integration Tests**
   - End-to-end API testing
   - Database integration
   - Error response validation

6. **OpenAPI Documentation**
   - Complete endpoint documentation
   - Request/response examples
   - Error code documentation
   - Authentication requirements

7. **Security Implementation**
   - Input sanitization
   - SQL injection prevention
   - Rate limiting configuration
   - Audit logging

**Code Style Requirements:**
- Clean code principles
- SOLID design patterns
- Comprehensive error handling
- Detailed logging
- Performance optimization
- Security best practices

**Example Context:**
This endpoint will be used by [FRONTEND_APP/MOBILE_APP/THIRD_PARTY] to [USE_CASE_DESCRIPTION]. Expected load is [EXPECTED_TPS] requests per second with [AVAILABILITY_REQUIREMENT] uptime requirement.
```

## 🔧 Usage Examples

### Example 1: Payment Processing Endpoint

```
Create a RESTful API endpoint for a fintech application with the following specifications:

**Endpoint Details:**
- Resource: payments
- HTTP Method: POST
- Path: /api/v1/payments
- Description: Process credit card payments with fraud detection

**Request Requirements:**
- Authentication: JWT Bearer token
- Request Body Schema: {
    amount: number (cents),
    currency: string (ISO 4217),
    paymentMethod: {
      type: "card",
      card: {
        number: string,
        expMonth: number,
        expYear: number,
        cvc: string
      }
    },
    customer: {
      id: string,
      email: string
    },
    metadata?: object
  }
- Headers: Content-Type: application/json, Authorization: Bearer {token}

**Business Logic:**
- Validate payment amount (minimum $0.50, maximum $10,000)
- Perform KYC validation for customers
- Run fraud detection algorithms
- Process payment with Stripe
- Store transaction record
- Send confirmation email
- Update customer payment history

**Technical Requirements:**
- Framework: Express.js with TypeScript
- Database: PostgreSQL with Knex.js
- Payment Processor: Stripe API
- Email Service: SendGrid
- Fraud Detection: Custom rules + ML model

**Compliance Requirements:**
- PCI DSS Level 1 compliance
- Never store raw card data
- Encrypt sensitive information
- Audit all payment operations
- GDPR compliance for EU customers
```

### Example 2: User Account Endpoint

```
Create a RESTful API endpoint for a fintech application with the following specifications:

**Endpoint Details:**
- Resource: users
- HTTP Method: GET
- Path: /api/v1/users/{userId}
- Description: Retrieve user account information with privacy controls

**Request Requirements:**
- Authentication: JWT Bearer token with user:read scope
- Path Parameters: userId (UUID)
- Query Parameters: include (profile,transactions,preferences)

**Business Logic:**
- Verify user owns account or has admin privileges
- Apply data privacy filters based on user consent
- Include related data based on include parameter
- Mask sensitive information for non-owners
- Track data access for audit purposes

**Compliance Requirements:**
- GDPR Article 15 (Right of Access)
- PII data masking for unauthorized access
- Audit logging for all data access
- Consent-based data inclusion
```

## ✅ Expected Output Components

When using this template, the AI should generate:

1. **Complete TypeScript route handler**
2. **Database models and migrations**  
3. **Validation schemas (Joi)**
4. **Comprehensive test suites**
5. **OpenAPI/Swagger documentation**
6. **Error handling middleware**
7. **Security configurations**
8. **Audit logging implementation**

## 🎯 Validation Checklist

Before using the generated code:

- [ ] All error cases are handled
- [ ] Input validation covers edge cases
- [ ] Authentication/authorization is implemented
- [ ] Database transactions are used appropriately
- [ ] Sensitive data is properly encrypted/masked
- [ ] Audit logging captures required events
- [ ] Rate limiting is configured
- [ ] Tests cover happy path and error scenarios
- [ ] OpenAPI documentation is complete
- [ ] Security best practices are followed

## 🔄 Iterative Refinement

After initial generation:

1. **Review and Test**: Run the generated code and tests
2. **Refine Requirements**: Add missing business rules or edge cases
3. **Enhance Security**: Add additional security measures if needed
4. **Optimize Performance**: Review for potential bottlenecks
5. **Update Documentation**: Ensure all changes are documented

## 📚 Related Templates

- [Database Schema Generation](./database-schema.md)
- [Test Suite Generation](./test-generation.md)
- [Error Handling Patterns](./error-handling.md)
- [Security Implementation](./security-patterns.md)