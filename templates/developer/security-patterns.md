# Security Implementation Patterns for AI-Assisted Development

## 🛡️ Overview

This template provides comprehensive security patterns and AI prompts for implementing secure fintech applications. Use these patterns with GitHub Copilot, Cursor AI, or ChatGPT to generate secure, compliant code that follows industry best practices.

## 🔐 Authentication and Authorization Patterns

### JWT Authentication Implementation

```
You are a senior security engineer implementing JWT authentication for a fintech application.

SECURITY REQUIREMENTS:
- PCI DSS Level 1 compliance
- Strong token security with rotation
- Multi-factor authentication support
- Session management and timeout
- Audit logging for all authentication events

GENERATE SECURE JWT IMPLEMENTATION:

1. **JWT Token Service**
   - Token generation with strong secrets
   - Token validation and verification
   - Token refresh mechanism
   - Token blacklisting for logout
   - Secure token storage patterns

2. **Authentication Middleware**
   - Request authentication validation
   - Authorization header parsing
   - Token expiration handling
   - Rate limiting integration
   - Security header enforcement

3. **Security Controls**
   - Secret key rotation mechanism
   - Token lifetime management
   - Brute force protection
   - Concurrent session handling
   - Audit trail generation

IMPLEMENTATION REQUIREMENTS:
- Use RS256 or ES256 algorithms (not HS256)
- Implement proper token claims validation
- Include security headers (HSTS, CSP, etc.)
- Add comprehensive error handling
- Ensure PII data is never in tokens

INCLUDE:
- TypeScript interfaces for type safety
- Unit tests with security test cases
- Integration with rate limiting
- Logging for security monitoring
- Documentation with security considerations

Generate production-ready JWT authentication service with middleware and security controls.
```

### Role-Based Access Control (RBAC) Pattern

```
Implement a comprehensive Role-Based Access Control system for a fintech application.

RBAC REQUIREMENTS:
- Hierarchical role structure
- Dynamic permission assignment
- Resource-level access control
- Audit trail for all access decisions
- Integration with authentication system

RBAC COMPONENTS TO IMPLEMENT:

1. **Role Management System**
   - Role definition and hierarchy
   - Permission assignment and inheritance
   - Dynamic role updates
   - Role conflict resolution
   - Audit logging for role changes

2. **Permission Engine**
   - Resource-based permissions
   - Action-specific access control
   - Context-aware authorization
   - Policy evaluation engine
   - Performance optimization

3. **Access Control Middleware**
   - Request authorization validation
   - Resource access verification
   - Action permission checking
   - Audit trail generation
   - Error handling and responses

SECURITY PATTERNS:
- Principle of least privilege
- Segregation of duties
- Defense in depth
- Fail-safe defaults
- Complete mediation

FINTECH-SPECIFIC ROLES:
- Customer (read own data, initiate transactions)
- Support Agent (read customer data, limited updates)
- Loan Officer (access credit data, approve loans)
- Compliance Officer (audit access, generate reports)
- Admin (system configuration, user management)

IMPLEMENTATION DETAILS:
- Database schema for roles and permissions
- Caching strategy for performance
- API endpoints for role management
- Integration with existing authentication
- Migration scripts for role setup

Create comprehensive RBAC system with hierarchical roles, dynamic permissions, and audit capabilities.
```

## 🔒 Data Protection Patterns

### Encryption at Rest Pattern

```
Implement comprehensive data encryption at rest for sensitive financial data.

ENCRYPTION REQUIREMENTS:
- AES-256-GCM for symmetric encryption
- RSA-4096 or ECC P-384 for asymmetric encryption
- Proper key management and rotation
- Field-level encryption for PII
- Database encryption integration

ENCRYPTION IMPLEMENTATION:

1. **Symmetric Encryption Service**
   - AES-256-GCM implementation
   - Initialization vector (IV) generation
   - Authentication tag verification
   - Key derivation functions
   - Secure random number generation

2. **Key Management System**
   - Master key generation and storage
   - Key rotation policies
   - Key versioning and history
   - Hardware Security Module (HSM) integration
   - Key backup and recovery

3. **Field-Level Encryption**
   - Selective field encryption
   - Searchable encryption for queries
   - Format-preserving encryption
   - Database integration patterns
   - Performance optimization

SENSITIVE DATA CATEGORIES:
- Personal Identifiable Information (PII)
- Financial account numbers
- Social Security Numbers
- Credit card information
- Banking credentials

SECURITY CONTROLS:
- Secure key storage (never in code)
- Key access logging and monitoring
- Encryption key rotation schedule
- Data classification and handling
- Compliance validation

IMPLEMENTATION REQUIREMENTS:
- Integration with AWS KMS, Azure Key Vault, or HSM
- Database-level encryption support
- Application-level encryption for APIs
- Backup encryption procedures
- Performance benchmarking

Generate production-ready encryption service with key management, field-level encryption, and compliance features.
```

### Data Masking and Tokenization Pattern

```
Implement data masking and tokenization for PCI DSS compliance and data protection.

TOKENIZATION REQUIREMENTS:
- Format-preserving tokenization for card numbers
- Irreversible tokenization for non-essential data
- Token vault with secure storage
- Token lifecycle management
- Integration with payment processors

TOKENIZATION IMPLEMENTATION:

1. **Tokenization Service**
   - Token generation algorithms
   - Format-preserving tokenization
   - Token-to-data mapping storage
   - Token validation and verification
   - Batch tokenization support

2. **Data Masking Engine**
   - Dynamic data masking for displays
   - Static data masking for testing
   - Pattern-based masking rules
   - Conditional masking logic
   - Performance optimization

3. **Token Vault Management**
   - Secure token storage
   - Access control and auditing
   - Token lifecycle management
   - High availability configuration
   - Backup and recovery procedures

MASKING PATTERNS:
- Credit card numbers: ****-****-****-1234
- SSN: ***-**-1234
- Email: j***@example.com
- Phone: (***) ***-1234
- Account numbers: ****1234

DATA CATEGORIES:
- Payment card data (PAN, CVV, expiry)
- Personal identifiers (SSN, DL, Passport)
- Financial account information
- Biometric data
- Authentication credentials

COMPLIANCE FEATURES:
- PCI DSS tokenization requirements
- GDPR pseudonymization support
- SOX data protection controls
- Audit trail and logging
- Data retention policies

Create comprehensive tokenization and masking system with format preservation, secure vaults, and compliance features.
```

## 🌐 API Security Patterns

### API Authentication and Rate Limiting

```
Implement secure API authentication with comprehensive rate limiting for a fintech API.

API SECURITY REQUIREMENTS:
- OAuth 2.0 + PKCE for public clients
- Client credentials flow for server-to-server
- JWT tokens with proper validation
- Rate limiting with different tiers
- API key management for partners

API SECURITY IMPLEMENTATION:

1. **OAuth 2.0 Server**
   - Authorization server setup
   - Client registration and validation
   - PKCE implementation for mobile apps
   - Scope-based access control
   - Refresh token rotation

2. **Rate Limiting Engine**
   - Token bucket algorithm
   - Sliding window rate limiting
   - Per-user and per-endpoint limits
   - Dynamic rate limiting based on behavior
   - Rate limit headers and responses

3. **API Key Management**
   - API key generation and rotation
   - Key-based authentication
   - Usage analytics and monitoring
   - Key revocation and lifecycle
   - Partner integration support

RATE LIMITING TIERS:
- Anonymous: 100 requests/hour
- Authenticated User: 1000 requests/hour
- Premium User: 5000 requests/hour
- Partner API: 10000 requests/hour
- Internal Services: Unlimited

SECURITY CONTROLS:
- Request signing for sensitive operations
- IP whitelisting for partner APIs
- Geo-blocking for restricted regions
- DDoS protection and mitigation
- Security headers enforcement

API ENDPOINTS PROTECTION:
- Public endpoints: Rate limiting only
- Authentication endpoints: Strong rate limiting + CAPTCHA
- Payment endpoints: Authentication + signing + rate limiting
- Admin endpoints: Strong authentication + IP restrictions

MONITORING AND ALERTING:
- Real-time rate limit monitoring
- Suspicious activity detection
- API abuse pattern recognition
- Security incident alerting
- Performance impact analysis

Generate secure API authentication system with OAuth 2.0, rate limiting, and comprehensive monitoring.
```

### Input Validation and Sanitization Pattern

```
Implement comprehensive input validation and sanitization for fintech applications.

VALIDATION REQUIREMENTS:
- SQL injection prevention
- XSS attack mitigation
- Command injection protection
- Path traversal prevention
- Business logic validation

INPUT VALIDATION FRAMEWORK:

1. **Schema Validation**
   - JSON schema validation
   - Request payload validation
   - Type checking and coercion
   - Range and length validation
   - Format validation (email, phone, etc.)

2. **Sanitization Engine**
   - HTML entity encoding
   - SQL parameter binding
   - Command parameter escaping
   - Path canonicalization
   - Content Security Policy enforcement

3. **Business Rule Validation**
   - Financial amount validation
   - Account number format checking
   - Transaction limit enforcement
   - Regulatory compliance validation
   - Custom business logic rules

VALIDATION PATTERNS:

1. **Financial Data Validation**
   - Currency amount validation (precision, range)
   - Account number format validation
   - Routing number validation (checksum)
   - IBAN validation for international transfers
   - Credit card number validation (Luhn algorithm)

2. **Personal Data Validation**
   - Email format and domain validation
   - Phone number format and region validation
   - SSN format and checksum validation
   - Date of birth range validation
   - Address format validation

3. **Security Data Validation**
   - Password strength validation
   - Token format validation
   - API key format validation
   - Signature validation
   - Timestamp validation for replay protection

SANITIZATION TECHNIQUES:
- Parameterized queries for SQL
- Context-aware output encoding
- File path validation and sanitization
- Regular expression validation
- Whitelist-based validation

ERROR HANDLING:
- Detailed validation error messages
- Security-focused error responses
- Audit logging for validation failures
- Rate limiting on validation errors
- User-friendly error formatting

PERFORMANCE OPTIMIZATION:
- Validation caching for repeated patterns
- Asynchronous validation for non-critical fields
- Batch validation for multiple inputs
- Early validation failure detection
- Validation pipeline optimization

Create comprehensive input validation framework with sanitization, business rules, and security controls.
```

## 🔍 Security Monitoring Patterns

### Audit Logging and Security Monitoring

```
Implement comprehensive audit logging and security monitoring for fintech applications.

AUDIT REQUIREMENTS:
- Complete audit trail for all transactions
- Tamper-evident logging system
- Real-time security monitoring
- Compliance reporting capabilities
- Long-term log retention and archival

AUDIT LOGGING SYSTEM:

1. **Structured Logging Framework**
   - JSON-based log format
   - Consistent log schema
   - Contextual information inclusion
   - Performance-optimized logging
   - Log level management

2. **Security Event Detection**
   - Authentication failure monitoring
   - Authorization violation detection
   - Suspicious activity pattern recognition
   - Fraud indicator identification
   - Compliance violation alerts

3. **Log Processing Pipeline**
   - Real-time log streaming
   - Log aggregation and correlation
   - Anomaly detection algorithms
   - Alert generation and routing
   - Dashboard and visualization

AUDIT EVENT CATEGORIES:

1. **Authentication Events**
   - Login attempts (success/failure)
   - Password changes
   - Account lockouts
   - Multi-factor authentication events
   - Session management activities

2. **Authorization Events**
   - Access control decisions
   - Permission changes
   - Role assignments
   - Resource access attempts
   - Administrative actions

3. **Transaction Events**
   - Payment processing activities
   - Account balance changes
   - Transfer operations
   - Fraud detection triggers
   - Refund and reversal operations

4. **System Events**
   - Configuration changes
   - Software deployments
   - Database schema changes
   - API endpoint modifications
   - Security control updates

LOG SECURITY MEASURES:
- Log integrity protection (digital signatures)
- Encrypted log transmission
- Secure log storage
- Access control for log data
- Log retention policies

MONITORING AND ALERTING:
- Real-time security dashboards
- Automated alert generation
- Incident response integration
- Compliance reporting automation
- Forensic analysis capabilities

COMPLIANCE FEATURES:
- SOX audit trail requirements
- PCI DSS logging standards
- GDPR audit log requirements
- Regulatory reporting support
- Evidence preservation

Generate comprehensive audit logging system with security monitoring, compliance features, and real-time alerting.
```

### Fraud Detection Pattern

```
Implement AI-powered fraud detection system with real-time monitoring and machine learning.

FRAUD DETECTION REQUIREMENTS:
- Real-time transaction scoring
- Machine learning model integration
- Rule-based detection engines
- Behavioral analysis
- Multi-layered fraud prevention

FRAUD DETECTION ARCHITECTURE:

1. **Rule-Based Detection Engine**
   - Velocity checks (transaction frequency)
   - Amount-based rules (unusual amounts)
   - Geographic analysis (location anomalies)
   - Time-based patterns (unusual timing)
   - Account behavior analysis

2. **Machine Learning Pipeline**
   - Feature engineering for transactions
   - Real-time model scoring
   - Model training and retraining
   - A/B testing for model performance
   - Explainable AI for decision transparency

3. **Behavioral Analytics**
   - User behavior profiling
   - Device fingerprinting
   - Session analysis
   - Spending pattern recognition
   - Social network analysis

FRAUD DETECTION RULES:

1. **Transaction-Level Rules**
   - High-value transaction alerts
   - Rapid successive transactions
   - Round-number transaction patterns
   - Cross-border transaction monitoring
   - Merchant category restrictions

2. **Account-Level Rules**
   - New account monitoring
   - Dormant account activity
   - Account takeover indicators
   - Identity verification failures
   - Credit limit breaches

3. **Network-Level Rules**
   - IP address reputation checking
   - Proxy and VPN detection
   - Geolocation inconsistencies
   - Device spoofing detection
   - Bot activity identification

MACHINE LEARNING FEATURES:
- Transaction amount and frequency
- Merchant category and location
- Time of day and day of week
- Device and browser fingerprints
- Historical user behavior
- Network and geolocation data

FRAUD RESPONSE ACTIONS:
- Real-time transaction blocking
- Step-up authentication requirements
- Account restrictions and holds
- Manual review queue assignment
- Customer notification and verification

PERFORMANCE REQUIREMENTS:
- Sub-100ms scoring latency
- 99.99% system availability
- Minimal false positive rates
- Scalable to millions of transactions
- Real-time model updates

Create AI-powered fraud detection system with rule engines, machine learning, and real-time response capabilities.
```

## 🛠️ Secure Development Patterns

### Secure Configuration Management

```
Implement secure configuration management for fintech applications with environment separation and secret management.

CONFIGURATION SECURITY REQUIREMENTS:
- Environment-specific configurations
- Secret management integration
- Configuration validation
- Audit trail for changes
- Runtime configuration updates

SECURE CONFIGURATION SYSTEM:

1. **Configuration Service**
   - Hierarchical configuration structure
   - Environment-based overrides
   - Type-safe configuration loading
   - Configuration validation rules
   - Default value management

2. **Secret Management Integration**
   - External secret store integration (Vault, AWS Secrets Manager)
   - Secret rotation capabilities
   - Encryption key management
   - Secret access auditing
   - Secure secret distribution

3. **Configuration Validation**
   - Schema-based validation
   - Business rule validation
   - Security constraint checking
   - Performance impact analysis
   - Compliance requirement validation

CONFIGURATION CATEGORIES:

1. **Application Configuration**
   - Server settings (ports, timeouts)
   - Database connection parameters
   - API endpoint configurations
   - Feature flags and toggles
   - Performance tuning parameters

2. **Security Configuration**
   - Authentication settings
   - Encryption parameters
   - Rate limiting configuration
   - CORS and security headers
   - Certificate and key settings

3. **Integration Configuration**
   - Third-party service endpoints
   - API keys and credentials
   - Webhook configurations
   - Message queue settings
   - Cache configuration

ENVIRONMENT MANAGEMENT:
- Development environment settings
- Testing environment isolation
- Staging environment configuration
- Production security hardening
- Disaster recovery configuration

SECURITY CONTROLS:
- Configuration encryption at rest
- Access control for configuration changes
- Audit logging for all modifications
- Configuration drift detection
- Automated security scanning

DEPLOYMENT PATTERNS:
- Immutable configuration deployment
- Blue-green configuration updates
- Canary configuration rollouts
- Rollback capabilities
- Configuration validation gates

Generate secure configuration management system with secret integration, validation, and audit capabilities.
```

### Secure Error Handling Pattern

```
Implement secure error handling that prevents information disclosure while maintaining usability.

ERROR HANDLING REQUIREMENTS:
- Information disclosure prevention
- User-friendly error messages
- Comprehensive error logging
- Security incident detection
- Graceful degradation

SECURE ERROR HANDLING SYSTEM:

1. **Error Classification Framework**
   - Business logic errors
   - Validation errors
   - System errors
   - Security errors
   - External service errors

2. **Error Response Engine**
   - Safe error message generation
   - Error code standardization
   - Context-appropriate responses
   - Localization support
   - Rate limiting for error responses

3. **Error Logging and Monitoring**
   - Structured error logging
   - Error correlation and analysis
   - Security incident detection
   - Performance impact monitoring
   - Error trend analysis

ERROR HANDLING PATTERNS:

1. **Client-Safe Error Responses**
   - Generic error messages for security issues
   - Specific messages for validation errors
   - User-actionable error information
   - No system internals disclosure
   - Consistent error format

2. **Internal Error Logging**
   - Detailed error information capture
   - Full stack trace logging
   - Request context preservation
   - User and session information
   - Performance metrics inclusion

3. **Security Error Detection**
   - Authentication failure patterns
   - Authorization violation attempts
   - Input validation bypass attempts
   - SQL injection attempt detection
   - Brute force attack indicators

ERROR RESPONSE EXAMPLES:

```typescript
// ❌ Bad - Information disclosure
{
  "error": "Database connection failed: Connection timeout to postgres://user:pass@db:5432/fintech",
  "stack": "Error at line 42 in DatabaseService.js..."
}

// ✅ Good - Secure error response
{
  "error": "Service temporarily unavailable",
  "code": "SERVICE_UNAVAILABLE",
  "message": "Please try again later or contact support",
  "requestId": "req_abc123"
}
```

SECURITY CONSIDERATIONS:
- No sensitive data in error responses
- Rate limiting on error endpoints
- Error response monitoring
- Security team alerting for suspicious patterns
- Automated incident response

GRACEFUL DEGRADATION:
- Fallback service responses
- Partial functionality maintenance
- User experience preservation
- Service health indicators
- Recovery procedure automation

Create secure error handling system with safe responses, comprehensive logging, and security monitoring.
```

## 📋 Security Testing Patterns

### Security Test Implementation

```
Generate comprehensive security tests for fintech applications covering authentication, authorization, and data protection.

SECURITY TESTING REQUIREMENTS:
- Authentication bypass testing
- Authorization control validation
- Input validation security tests
- Data encryption verification
- API security testing

SECURITY TEST CATEGORIES:

1. **Authentication Security Tests**
   - Password brute force protection
   - Account lockout mechanisms
   - Multi-factor authentication bypass
   - Session management security
   - Token manipulation resistance

2. **Authorization Security Tests**
   - Privilege escalation attempts
   - Horizontal access control bypass
   - Vertical access control bypass
   - Resource-level access validation
   - API endpoint authorization

3. **Input Security Tests**
   - SQL injection prevention
   - Cross-site scripting (XSS) protection
   - Command injection resistance
   - Path traversal prevention
   - File upload security

4. **Data Protection Tests**
   - Encryption at rest validation
   - Transmission encryption verification
   - Data masking effectiveness
   - Key management security
   - Backup encryption validation

AUTOMATED SECURITY TESTING:
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Interactive Application Security Testing (IAST)
- Software Composition Analysis (SCA)
- Container security scanning

PENETRATION TESTING SCENARIOS:
- External network penetration testing
- Web application security testing
- API security assessment
- Mobile application testing
- Social engineering simulations

COMPLIANCE TESTING:
- PCI DSS security validation
- SOX IT controls testing
- GDPR privacy control verification
- Regulatory requirement validation
- Industry standard compliance

Generate comprehensive security test suite with automated testing, manual scenarios, and compliance validation.
```

## 🚀 Implementation Guidelines

### Security Implementation Checklist

```
SECURITY IMPLEMENTATION CHECKLIST:

□ **Authentication & Authorization**
  □ Strong password policies implemented
  □ Multi-factor authentication enabled
  □ JWT tokens properly secured
  □ Role-based access control configured
  □ Session management implemented

□ **Data Protection**
  □ Encryption at rest enabled
  □ Transmission encryption configured
  □ Field-level encryption for PII
  □ Key management system integrated
  □ Data masking/tokenization implemented

□ **API Security**
  □ Rate limiting configured
  □ Input validation implemented
  □ Output encoding applied
  □ CORS policies configured
  □ Security headers enforced

□ **Monitoring & Logging**
  □ Audit logging implemented
  □ Security monitoring configured
  □ Fraud detection enabled
  □ Incident response automated
  □ Compliance reporting setup

□ **Infrastructure Security**
  □ Network security configured
  □ Container security hardened
  □ Database security enabled
  □ Backup encryption implemented
  □ Disaster recovery tested

AI SECURITY IMPLEMENTATION SUPPORT:
Use these prompts to generate secure implementations:

"Generate [SECURITY_COMPONENT] with [COMPLIANCE_REQUIREMENTS] including comprehensive tests and documentation"

"Implement [SECURITY_PATTERN] for fintech application with error handling, logging, and monitoring"

"Create security configuration for [ENVIRONMENT] with hardening, monitoring, and compliance features"
```

---

*This template is part of the comprehensive AI-driven development course. For API development patterns, see the [API Endpoint Generation Template](./api-endpoint-generation.md).*