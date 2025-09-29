# CI/CD Pipeline Template

## 🎯 Purpose
Generate comprehensive CI/CD pipeline configurations for fintech applications with security, compliance, and quality gates.

## 📝 Template

```
Act as a senior DevOps engineer specializing in fintech applications. Create a comprehensive CI/CD pipeline configuration with the following specifications:

**Application Context:**
- Application Type: [WEB_APP/MICROSERVICE/MOBILE_APP]
- Technology Stack: [LANGUAGES_AND_FRAMEWORKS]
- Target Environment: [AWS/AZURE/GCP/ON_PREMISE]
- Deployment Pattern: [BLUE_GREEN/CANARY/ROLLING]
- Compliance Requirements: [PCI_DSS/SOX/GDPR/etc]

**Pipeline Requirements:**
- Source Control: [GITHUB/GITLAB/BITBUCKET]
- Build Tool: [DOCKER/GRADLE/NPM/MAVEN]
- Test Types: [UNIT/INTEGRATION/E2E/SECURITY/PERFORMANCE]
- Artifact Storage: [REGISTRY_DETAILS]
- Deployment Targets: [DEV/STAGING/PRODUCTION]

**Security and Compliance:**
- Static Code Analysis: [SONARQUBE/CHECKMARX/VERACODE]
- Dependency Scanning: [SNYK/OWASP/WHITESOURCE]
- Container Scanning: [TWISTLOCK/AQUA/TRIVY]
- Secrets Management: [VAULT/AWS_SECRETS/AZURE_KEYVAULT]
- Compliance Scanning: [PCI/SOX/REGULATORY_CHECKS]

**Quality Gates:**
- Code Coverage: [MINIMUM_PERCENTAGE]
- Security Score: [MINIMUM_SCORE]
- Performance Benchmarks: [RESPONSE_TIME/THROUGHPUT]
- Compliance Checks: [REQUIRED_VALIDATIONS]

**Generate the following pipeline components:**

## 1. Pipeline Configuration File
Create a complete pipeline configuration file (GitHub Actions/Jenkins/GitLab CI) with:
- Trigger conditions (branch, tag, PR)
- Environment variables and secrets
- Build stages with proper dependencies
- Quality gates and approval processes
- Deployment strategies for each environment

## 2. Build Scripts
- Dockerfile with multi-stage builds
- Build automation scripts
- Dependency management
- Artifact creation and tagging

## 3. Test Automation
- Unit test execution with coverage
- Integration test suites
- End-to-end test automation
- Security testing integration
- Performance testing benchmarks

## 4. Security Scanning
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Dependency vulnerability scanning
- Container image security scanning
- Infrastructure security validation

## 5. Deployment Scripts
- Environment-specific deployment configurations
- Database migration scripts
- Configuration management
- Rollback procedures
- Health check validations

## 6. Monitoring and Alerting
- Application performance monitoring setup
- Log aggregation configuration
- Alert definitions and thresholds
- Dashboard configurations
- Incident response automation

## 7. Compliance Documentation
- Audit trail configuration
- Compliance report generation
- Change tracking and approval
- Risk assessment automation
- Regulatory requirement validation

**Best Practices to Include:**
- Immutable infrastructure principles
- Zero-downtime deployment strategies
- Automated rollback mechanisms
- Environment parity maintenance
- Security-first approach
- Comprehensive logging and monitoring
- Disaster recovery procedures

**Performance Requirements:**
- Build Time: [MAXIMUM_DURATION]
- Deployment Time: [MAXIMUM_DURATION]
- Recovery Time: [RTO_REQUIREMENT]
- Availability: [UPTIME_REQUIREMENT]
```

## 🔧 Usage Examples

### Example 1: Node.js Microservice Pipeline

```
Act as a senior DevOps engineer specializing in fintech applications. Create a comprehensive CI/CD pipeline configuration with the following specifications:

**Application Context:**
- Application Type: Microservice (Payment Processing API)
- Technology Stack: Node.js, Express, PostgreSQL, Redis
- Target Environment: AWS (EKS, RDS, ElastiCache)
- Deployment Pattern: Blue-Green with automated rollback
- Compliance Requirements: PCI DSS Level 1, SOX compliance

**Pipeline Requirements:**
- Source Control: GitHub with branch protection rules
- Build Tool: Docker with multi-stage builds
- Test Types: Unit (90% coverage), Integration, Contract, Security, Load testing
- Artifact Storage: AWS ECR with vulnerability scanning
- Deployment Targets: Dev, Staging, Production with approval gates

**Security and Compliance:**
- Static Code Analysis: SonarQube with custom PCI rules
- Dependency Scanning: Snyk with automated PR fixes
- Container Scanning: Trivy with critical vulnerability blocking
- Secrets Management: AWS Secrets Manager with rotation
- Compliance Scanning: Custom PCI DSS validation scripts

**Quality Gates:**
- Code Coverage: Minimum 90% with no regressions
- Security Score: A-grade required, no high/critical vulnerabilities
- Performance Benchmarks: <200ms P95 response time, >1000 TPS
- Compliance Checks: PCI DSS automated validation, SOX audit trail
```

### Example 2: React Frontend Pipeline

```
**Application Context:**
- Application Type: Single Page Application (Customer Dashboard)
- Technology Stack: React, TypeScript, Material-UI, Jest
- Target Environment: AWS (CloudFront, S3, API Gateway)
- Deployment Pattern: Rolling deployment with feature flags
- Compliance Requirements: GDPR, accessibility standards (WCAG 2.1)

**Pipeline Requirements:**
- Source Control: GitHub with semantic versioning
- Build Tool: npm with webpack optimization
- Test Types: Unit, Integration, E2E (Cypress), Accessibility, Visual regression
- Artifact Storage: S3 with CloudFront invalidation
- Deployment Targets: Feature branches, staging, production

**Quality Gates:**
- Code Coverage: Minimum 85%
- Bundle Size: Maximum 2MB gzipped
- Performance: Lighthouse score >90 for all metrics
- Accessibility: WCAG 2.1 AA compliance validation
```

## ✅ Expected Output Components

When using this template, AI should generate:

1. **Complete Pipeline Configuration** (YAML/JSON)
2. **Dockerfile** with security best practices
3. **Build Scripts** for automation
4. **Test Automation Scripts** for all test types
5. **Security Scanning Configuration** with quality gates
6. **Deployment Scripts** for each environment
7. **Monitoring Configuration** with alerts
8. **Documentation** for pipeline operations
9. **Troubleshooting Guide** for common issues
10. **Compliance Validation** scripts and reports

## 🎯 Validation Checklist

Before deploying the pipeline:

- [ ] All security scans are configured and passing
- [ ] Quality gates prevent deployment of poor-quality code
- [ ] Secrets are properly managed and not exposed
- [ ] Rollback procedures are tested and documented
- [ ] Monitoring and alerting are configured
- [ ] Compliance requirements are validated
- [ ] Performance benchmarks are met
- [ ] Environment parity is maintained
- [ ] Approval processes are properly configured
- [ ] Audit trails are comprehensive and automated

## 🔒 Security Best Practices

### Pipeline Security:
- Use least privilege access principles
- Scan all dependencies for vulnerabilities
- Implement secrets rotation
- Enable audit logging for all pipeline activities
- Use signed commits and verified builds
- Implement branch protection rules
- Scan container images before deployment

### Compliance Integration:
- Automated PCI DSS validation
- SOX audit trail generation
- GDPR data handling verification
- Regulatory change tracking
- Risk assessment automation
- Incident response procedures

## 📊 Pipeline Metrics

### Key Performance Indicators:
- **Build Success Rate**: Target >95%
- **Build Duration**: Target <10 minutes
- **Deployment Frequency**: Daily for non-critical, weekly for critical
- **Lead Time**: Feature to production <1 week
- **Mean Time to Recovery**: <1 hour for critical issues
- **Security Scan Coverage**: 100% of code and dependencies

## 🔄 Continuous Improvement

### Pipeline Optimization:
1. **Performance Monitoring**: Track build and deployment times
2. **Security Scanning**: Regular vulnerability assessment updates
3. **Quality Metrics**: Monitor code quality trends
4. **User Feedback**: Incorporate developer experience improvements
5. **Technology Updates**: Keep tools and dependencies current
6. **Process Refinement**: Regular retrospectives and improvements

## 📚 Related Templates

- [Infrastructure as Code](./infrastructure-as-code.md)
- [Monitoring and Alerting](./monitoring-alerting.md)
- [Security Configuration](./security-configuration.md)
- [Deployment Strategies](./deployment-strategies.md)
- [Disaster Recovery](./disaster-recovery.md)