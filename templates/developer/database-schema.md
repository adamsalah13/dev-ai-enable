# Database Schema Generation Template

## 🎯 Purpose
Generate comprehensive database schemas for fintech applications with security, compliance, and performance considerations.

## 📝 Template

```
Act as a senior database architect specializing in fintech applications. Design a comprehensive database schema with the following specifications:

**Application Context:**
- Application Name: [APPLICATION_NAME]
- Database Type: [POSTGRESQL/MYSQL/MONGODB]
- Expected Scale: [USER_COUNT/TRANSACTION_VOLUME]
- Compliance Requirements: [PCI_DSS/GDPR/SOX/etc]
- Geographic Distribution: [SINGLE_REGION/MULTI_REGION]

**Business Requirements:**
- Core Entities: [USER_ACCOUNTS/PAYMENTS/TRANSACTIONS/etc]
- Data Relationships: [ENTITY_RELATIONSHIPS]
- Business Rules: [CONSTRAINTS_AND_VALIDATIONS]
- Audit Requirements: [AUDIT_TRAIL_NEEDS]
- Retention Policies: [DATA_RETENTION_REQUIREMENTS]

**Technical Requirements:**
- Performance Targets: [QPS/RESPONSE_TIME]
- Concurrency: [CONCURRENT_USERS]
- Data Volume: [EXPECTED_DATA_SIZE]
- Backup/Recovery: [RTO/RPO_REQUIREMENTS]
- Encryption: [DATA_ENCRYPTION_REQUIREMENTS]

**Compliance and Security:**
- PII Handling: [PERSONAL_DATA_REQUIREMENTS]
- Financial Data: [PAYMENT_DATA_SECURITY]
- Regulatory Reporting: [COMPLIANCE_REPORTING]
- Data Classification: [SENSITIVITY_LEVELS]

**Generate the following database components:**

## 1. Complete Schema Definition
- Table structures with all columns
- Data types optimized for fintech use cases
- Primary and foreign key relationships
- Check constraints and validations
- Custom types and enums where appropriate

## 2. Security Implementation
- Row-level security policies
- Column-level encryption for sensitive data
- User roles and permissions
- Database-level audit logging
- Connection security configurations

## 3. Performance Optimization
- Strategic indexing for query performance
- Partitioning strategies for large tables
- Materialized views for reporting
- Query optimization recommendations
- Connection pooling configurations

## 4. Data Integrity and Compliance
- Foreign key constraints
- Check constraints for business rules
- Triggers for audit logging
- Data validation functions
- Stored procedures for complex operations

## 5. Migration Scripts
- Initial schema creation scripts
- Sample data insertion scripts
- Version upgrade/downgrade scripts
- Data migration procedures
- Rollback strategies

## 6. Backup and Recovery
- Backup strategy recommendations
- Point-in-time recovery configuration
- Disaster recovery procedures
- Data archival strategies
- Cross-region replication setup

## 7. Monitoring and Maintenance
- Performance monitoring queries
- Health check procedures
- Maintenance scripts
- Capacity planning guidelines
- Alert configurations

**Best Practices to Include:**
- ACID compliance for financial transactions
- Eventual consistency handling for distributed systems
- Idempotency for payment operations
- Soft deletes for audit compliance
- Temporal data handling
- Multi-tenancy considerations
- Zero-downtime deployment strategies

**Documentation Requirements:**
- Entity-relationship diagrams
- Data dictionary with field descriptions
- Business rule documentation
- Performance benchmarks
- Security implementation notes
- Compliance mapping documentation
```

## 🔧 Usage Examples

### Example 1: Payment Processing Schema

```
Act as a senior database architect specializing in fintech applications. Design a comprehensive database schema with the following specifications:

**Application Context:**
- Application Name: PayFlow Payment Processing Platform
- Database Type: PostgreSQL 14+
- Expected Scale: 1M users, 10M transactions/month
- Compliance Requirements: PCI DSS Level 1, SOX, GDPR
- Geographic Distribution: Multi-region (US, EU)

**Business Requirements:**
- Core Entities: Users, Payment Methods, Transactions, Payments, Refunds, Disputes
- Data Relationships: User has multiple payment methods, payments link to transactions
- Business Rules: Minimum $0.50 payments, maximum $50,000 per transaction
- Audit Requirements: Complete audit trail for all financial operations
- Retention Policies: Transaction data 7 years, audit logs 10 years

**Technical Requirements:**
- Performance Targets: <100ms for payment lookups, 1000 TPS capacity
- Concurrency: 10,000 concurrent users during peak hours
- Data Volume: 100GB initial, growing 20GB/month
- Backup/Recovery: RPO 15 minutes, RTO 1 hour
- Encryption: AES-256 for PII, tokenization for payment data

**Compliance and Security:**
- PII Handling: GDPR right to erasure, data minimization
- Financial Data: PCI DSS compliant storage, no raw card data
- Regulatory Reporting: Real-time fraud detection, AML screening
- Data Classification: Public, Internal, Confidential, Restricted levels
```

### Example 2: Lending Platform Schema

```
**Application Context:**
- Application Name: LendTech Personal Loan Platform
- Database Type: PostgreSQL with TimescaleDB for time-series data
- Expected Scale: 500K users, 100K loan applications/month
- Compliance Requirements: Fair Credit Reporting Act (FCRA), Equal Credit Opportunity Act (ECOA)
- Geographic Distribution: US-only with state-specific regulations

**Business Requirements:**
- Core Entities: Borrowers, Loan Applications, Credit Reports, Loans, Payments, Collections
- Data Relationships: Complex scoring models, payment histories, risk assessments
- Business Rules: $1,000-$50,000 loan amounts, 12-60 month terms, credit score minimums
- Audit Requirements: Decision audit trails, model versioning, regulatory reporting
- Retention Policies: Application data 5 years, credit decisions permanent archive
```

## ✅ Expected Output Components

When using this template, AI should generate:

1. **Complete DDL Scripts** with all table definitions
2. **Security Configuration** with encryption and access controls
3. **Performance Indexes** optimized for query patterns
4. **Constraint Definitions** enforcing business rules
5. **Audit Logging Setup** for compliance requirements
6. **Migration Scripts** for version management
7. **Sample Data Scripts** for development and testing
8. **Monitoring Scripts** for performance tracking
9. **Backup/Recovery Procedures** with automation
10. **Documentation** with ERD and data dictionary

## 🔒 Security Best Practices

### Data Protection:
- **Encryption at Rest**: AES-256 for sensitive columns
- **Encryption in Transit**: TLS 1.3 for all connections
- **Tokenization**: Replace sensitive data with non-sensitive tokens
- **Hashing**: Irreversible hashing for passwords and secrets
- **Key Management**: Secure key rotation and storage

### Access Control:
- **Role-Based Access**: Principle of least privilege
- **Row-Level Security**: User can only access own data
- **Column-Level Security**: Restrict access to sensitive fields
- **API Security**: Rate limiting and input validation
- **Audit Logging**: Track all data access and modifications

## 📊 Performance Optimization

### Indexing Strategy:
- **Primary Keys**: Clustered indexes on UUID/BIGINT
- **Foreign Keys**: Indexes on all foreign key columns
- **Query Patterns**: Indexes optimized for common queries
- **Composite Indexes**: Multi-column indexes for complex queries
- **Partial Indexes**: Conditional indexes for filtered queries

### Partitioning:
- **Range Partitioning**: By date for time-series data
- **Hash Partitioning**: For even data distribution
- **List Partitioning**: By category or status
- **Partition Pruning**: Optimize queries with partition elimination

### Query Optimization:
- **Query Plans**: Analyze and optimize execution plans
- **Statistics**: Keep table statistics current
- **Connection Pooling**: Optimize connection management
- **Caching**: Strategic use of materialized views and cache layers

## 🔄 Migration and Versioning

### Schema Evolution:
1. **Backward Compatible Changes**: Add columns with defaults
2. **Breaking Changes**: Multi-step migration process
3. **Data Migrations**: Safe data transformation procedures
4. **Rollback Plans**: Always have rollback procedures ready
5. **Testing**: Comprehensive testing on production-like data

### Version Control:
- **Migration Scripts**: Sequential, numbered migration files
- **Environment Consistency**: Ensure all environments match
- **Documentation**: Document all schema changes
- **Change Reviews**: Peer review for all schema modifications

## 📚 Related Templates

- [API Endpoint Generation](./api-endpoint-generation.md)
- [Test Generation](./test-generation.md)
- [Security Implementation](./security-patterns.md)
- [Performance Optimization](./performance-optimization.md)