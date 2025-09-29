# API Documentation Template

## 🎯 Purpose
Generate comprehensive API documentation for fintech applications with examples, security details, and compliance information.

## 📝 Template

```
Act as an experienced technical writer specializing in fintech API documentation. Create comprehensive API documentation for the following specification:

**API Context:**
- API Name: [API_NAME]
- Version: [VERSION_NUMBER]
- Base URL: [BASE_URL]
- Authentication: [AUTH_METHOD]
- API Type: [REST/GraphQL/SOAP]
- Target Audience: [DEVELOPERS/PARTNERS/INTERNAL]

**Business Context:**
- Purpose: [API_PURPOSE_AND_GOALS]
- Use Cases: [PRIMARY_USE_CASES]
- Industry: [FINTECH_DOMAIN_SPECIFIC]
- Compliance: [REGULATORY_REQUIREMENTS]

**Technical Specifications:**
- Request/Response Format: [JSON/XML/etc]
- Rate Limiting: [LIMITS_AND_QUOTAS]
- Error Handling: [ERROR_CODE_STRUCTURE]
- Pagination: [PAGINATION_METHOD]
- Versioning Strategy: [VERSION_MANAGEMENT]

**Security Requirements:**
- Authentication Methods: [OAUTH2/JWT/API_KEY]
- Authorization Scopes: [PERMISSION_LEVELS]
- Data Encryption: [ENCRYPTION_STANDARDS]
- Compliance Standards: [PCI_DSS/GDPR/etc]

**Generate comprehensive API documentation including:**

## 1. API Overview
- Clear description of API purpose and capabilities
- Target audience and use cases
- Getting started guide with quick examples
- Authentication and authorization overview
- Rate limiting and quotas explanation

## 2. Authentication and Security
- Detailed authentication flow with examples
- API key management and best practices
- OAuth 2.0 implementation (if applicable)
- JWT token usage and validation
- Security headers and requirements
- IP whitelisting and restrictions

## 3. Endpoint Documentation
For each endpoint, provide:
- **HTTP Method and URL**
- **Description and purpose**
- **Authentication requirements**
- **Request parameters** (path, query, headers, body)
- **Request examples** with sample data
- **Response format** with schema
- **Response examples** (success and error cases)
- **HTTP status codes** and meanings
- **Error responses** with troubleshooting

## 4. Data Models and Schemas
- Complete object definitions
- Field descriptions and constraints
- Data types and formats
- Validation rules and requirements
- Enum values and their meanings
- Nested object structures

## 5. Code Examples and SDKs
- cURL examples for all endpoints
- JavaScript/Node.js examples
- Python examples
- Java examples
- Error handling examples
- SDK integration guides (if available)

## 6. Testing and Sandbox
- Sandbox environment details
- Test data and scenarios
- Postman collection export
- Testing best practices
- Mock server information

## 7. Error Handling
- Standard error format
- Complete error code reference
- Troubleshooting guide
- Common error scenarios
- Resolution steps

## 8. Rate Limiting and Quotas
- Rate limit details and thresholds
- Headers for rate limit information
- Best practices for handling limits
- Upgrading limits and quotas
- Monitoring usage

## 9. Webhooks (if applicable)
- Webhook event types
- Payload structures
- Security and verification
- Retry logic and failure handling
- Testing webhook endpoints

## 10. Compliance and Regulatory
- PCI DSS compliance notes
- GDPR data handling
- Financial regulation compliance
- Audit logging requirements
- Data retention policies

**Documentation Standards:**
- Use clear, concise language
- Include practical examples
- Provide complete code samples
- Explain business context
- Include security considerations
- Add troubleshooting information
- Maintain consistency in formatting
- Include version change notes

**Interactive Elements:**
- Try-it-now functionality
- Interactive examples
- Parameter validation
- Real-time testing interface
- Copy-to-clipboard code blocks
```

## 🔧 Usage Examples

### Example 1: Payment Processing API

```
Act as an experienced technical writer specializing in fintech API documentation. Create comprehensive API documentation for the following specification:

**API Context:**
- API Name: PayFlow Payment Processing API
- Version: v2.1
- Base URL: https://api.payflow.com/v2
- Authentication: OAuth 2.0 with JWT tokens
- API Type: RESTful API
- Target Audience: Third-party developers, merchant integrators, fintech partners

**Business Context:**
- Purpose: Enable secure payment processing for e-commerce and mobile applications
- Use Cases: Online checkout, recurring billing, refund processing, payment status tracking
- Industry: Digital payments, e-commerce, subscription services
- Compliance: PCI DSS Level 1, PSD2, GDPR

**Technical Specifications:**
- Request/Response Format: JSON with UTF-8 encoding
- Rate Limiting: 1000 requests per minute per API key
- Error Handling: Structured JSON error responses with error codes
- Pagination: Cursor-based pagination for list endpoints
- Versioning Strategy: URL path versioning with backward compatibility

**Security Requirements:**
- Authentication Methods: OAuth 2.0 with PKCE, API key for server-to-server
- Authorization Scopes: payment:read, payment:write, refund:process, reporting:read
- Data Encryption: TLS 1.3 for transport, AES-256 for data at rest
- Compliance Standards: PCI DSS Level 1, tokenization for card data
```

### Example 2: Account Management API

```
**API Context:**
- API Name: FinTech Account Management API
- Version: v1.3
- Base URL: https://api.fintech-platform.com/accounts/v1
- Authentication: API Key with HMAC signature
- API Type: RESTful API
- Target Audience: Internal applications, partner banks, regulatory systems

**Business Context:**
- Purpose: Manage customer accounts, KYC verification, and compliance reporting
- Use Cases: Account creation, KYC document processing, balance inquiries, transaction history
- Industry: Digital banking, lending, wealth management
- Compliance: KYC/AML regulations, GDPR, Basel III reporting

**Security Requirements:**
- Authentication Methods: HMAC-SHA256 signed requests with API keys
- Authorization Scopes: account:read, account:write, kyc:process, reporting:generate
- Data Encryption: End-to-end encryption for PII, field-level encryption in database
- Compliance Standards: KYC/AML compliance, GDPR data subject rights, audit logging
```

## ✅ Expected Output Components

When using this template, AI should generate:

1. **Complete API Reference** with all endpoints documented
2. **Authentication Guide** with implementation examples
3. **Data Model Documentation** with schemas and validation rules
4. **Code Examples** in multiple programming languages
5. **Error Handling Guide** with troubleshooting steps
6. **Security Documentation** with compliance details
7. **Testing Guide** with sandbox and mock data
8. **Integration Tutorials** with step-by-step instructions
9. **Rate Limiting Documentation** with best practices
10. **Changelog and Versioning** information

## 🎯 Documentation Quality Standards

### Writing Guidelines:
- **Clarity**: Use simple, direct language
- **Completeness**: Cover all endpoints and use cases
- **Accuracy**: Ensure all examples work correctly
- **Consistency**: Maintain uniform formatting and style
- **User-Focused**: Write from the developer's perspective
- **Searchable**: Use clear headings and keywords

### Technical Standards:
- **Valid Examples**: All code samples must be tested
- **Schema Validation**: API schemas must be accurate
- **Security Focus**: Emphasize security best practices
- **Error Coverage**: Document all possible error conditions
- **Performance**: Include performance considerations
- **Compliance**: Address regulatory requirements

## 📊 Documentation Metrics

### Success Indicators:
- **Adoption Rate**: API usage after documentation release
- **Support Tickets**: Reduction in API-related support requests
- **Time to Integration**: Average time for developers to integrate
- **User Satisfaction**: Developer feedback and ratings
- **Documentation Usage**: Page views and engagement metrics

### Quality Metrics:
- **Completeness**: Percentage of API coverage
- **Accuracy**: Number of reported documentation errors
- **Freshness**: Time since last update
- **Accessibility**: Compliance with accessibility standards

## 🔄 Maintenance and Updates

### Regular Updates:
1. **API Changes**: Update documentation with each API release
2. **User Feedback**: Incorporate developer feedback and questions
3. **Security Updates**: Refresh security examples and best practices
4. **Compliance Changes**: Update for new regulatory requirements
5. **Performance Improvements**: Add new optimization recommendations

### Documentation Testing:
- **Code Validation**: Test all code examples regularly
- **Link Checking**: Verify all internal and external links
- **Schema Validation**: Ensure API schemas match implementation
- **User Testing**: Gather feedback from new API users

## 🔒 Security Documentation Focus

### Fintech-Specific Security:
- **PCI Compliance**: Card data handling requirements
- **Financial Regulations**: KYC/AML documentation
- **Data Protection**: GDPR and privacy law compliance
- **Audit Requirements**: Logging and monitoring documentation
- **Fraud Prevention**: Security feature documentation
- **Encryption Standards**: Data protection implementation

## 📚 Related Templates

- [User Guide](./user-guide.md)
- [Technical Specification](./technical-specification.md)
- [Compliance Documentation](./compliance-documentation.md)
- [Troubleshooting Guide](./troubleshooting-guide.md)
- [Onboarding Guide](./onboarding-guide.md)