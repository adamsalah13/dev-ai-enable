# User Story Generation Template

## 🎯 Purpose
Generate comprehensive user stories with acceptance criteria, priorities, and estimates for fintech applications.

## 📝 Template

```
Act as an experienced Product Owner specializing in fintech applications. Based on the following requirements, generate comprehensive user stories:

**Project Context:**
- Application: [APPLICATION_NAME]
- Feature/Epic: [FEATURE_DESCRIPTION]
- Target Users: [USER_PERSONAS]
- Business Goals: [OBJECTIVES]
- Technical Constraints: [LIMITATIONS]

**User Personas:**
1. [PERSONA_1]: [DESCRIPTION, NEEDS, PAIN POINTS]
2. [PERSONA_2]: [DESCRIPTION, NEEDS, PAIN POINTS]
3. [PERSONA_3]: [DESCRIPTION, NEEDS, PAIN POINTS]

**Epic Requirements:**
[DETAILED_FEATURE_REQUIREMENTS]

**For each user story, provide:**

## Story Format:
**As a** [user persona]
**I want** [functionality]
**So that** [business value/benefit]

## Acceptance Criteria (Given/When/Then format):
- **Given** [initial context/preconditions]
- **When** [action or event trigger]
- **Then** [expected outcome]

## Additional Details:
- **Story ID**: [Unique identifier]
- **Priority**: [High/Medium/Low] with justification
- **Story Points**: [1, 2, 3, 5, 8, 13] with estimation rationale
- **Dependencies**: [Other stories this depends on]
- **Definition of Done**: [Specific completion criteria]
- **Notes**: [Edge cases, special considerations, technical notes]

**Generate user stories covering:**
1. Happy path scenarios
2. Error handling and edge cases
3. Security and compliance requirements
4. Performance and scalability needs
5. User experience and accessibility
6. Integration with external systems
7. Reporting and analytics features
8. Administrative and maintenance tasks

**Organize stories into logical groups and provide a backlog prioritization recommendation.**
```

## 🔧 Usage Examples

### Example 1: Digital Wallet Feature

```
Act as an experienced Product Owner specializing in fintech applications. Based on the following requirements, generate comprehensive user stories:

**Project Context:**
- Application: PayFlow Digital Wallet
- Feature/Epic: Peer-to-peer money transfer functionality
- Target Users: Individual consumers, small business owners, teenagers with parental oversight
- Business Goals: Enable instant money transfers, reduce transaction costs, increase user engagement
- Technical Constraints: PCI DSS compliance, $10,000 daily transfer limit, support iOS/Android

**User Personas:**
1. Sarah (Working Professional): Needs to split bills with friends, pay for services, values security and speed
2. Mike (Small Business Owner): Needs to pay contractors quickly, receive payments from customers, requires transaction records
3. Emma (Teen with Parent): Wants to receive allowance, pay friends, parents need oversight and controls

**Epic Requirements:**
- Send money to contacts using phone number or email
- Receive money with instant notifications
- View transaction history and receipts
- Set up spending limits and parental controls
- Integration with bank accounts and debit cards
- Real-time fraud detection and security alerts
```

### Example 2: Loan Application System

```
**Project Context:**
- Application: LendTech Personal Loans
- Feature/Epic: Automated loan application and approval process
- Target Users: Working adults aged 25-55, credit scores 600-850
- Business Goals: Reduce approval time to 24 hours, achieve 70% approval rate, ensure compliance
- Technical Constraints: Integration with credit bureaus, automated decision engine, KYC/AML compliance

**User Personas:**
1. John (First-time Borrower): Needs $15K for home improvement, unfamiliar with loan process, values guidance and transparency
2. Lisa (Returning Customer): Seeking $8K for debt consolidation, wants quick approval, expects personalized rates
3. David (High-credit Customer): Needs $25K for business investment, expects premium service and competitive rates

**Epic Requirements:**
- Online application with document upload
- Real-time credit check and income verification
- Automated underwriting with manual review option
- Digital loan agreement and e-signature
- Automated fund disbursement
- Customer portal for loan management
```

## ✅ Expected Output Components

When using this template, AI should generate:

1. **Complete User Stories** with proper format and structure
2. **Detailed Acceptance Criteria** in Given/When/Then format
3. **Story Prioritization** with business justification
4. **Effort Estimation** with story points and rationale
5. **Dependency Mapping** showing story relationships
6. **Definition of Done** with specific completion criteria
7. **Edge Cases and Error Scenarios** comprehensively covered
8. **Compliance and Security Stories** for fintech requirements
9. **Performance and Scalability Stories** for system quality
10. **Epic Organization** with logical story grouping

## 🎯 Validation Checklist

Before finalizing user stories:

- [ ] Stories follow INVEST criteria (Independent, Negotiable, Valuable, Estimatable, Small, Testable)
- [ ] Acceptance criteria are specific and testable
- [ ] All user personas are represented
- [ ] Security and compliance requirements are included
- [ ] Error handling scenarios are covered
- [ ] Performance requirements are specified
- [ ] Integration points are addressed
- [ ] User experience is prioritized
- [ ] Business value is clearly articulated
- [ ] Dependencies are identified and documented

## 📊 Story Prioritization Framework

### Priority Levels:
- **High**: Core functionality, regulatory requirements, security features
- **Medium**: Enhanced user experience, performance improvements, nice-to-have features
- **Low**: Future enhancements, advanced features, optimization

### Story Point Scale:
- **1 point**: Simple configuration or small UI changes
- **2 points**: Basic CRUD operations with validation
- **3 points**: Complex business logic or integration
- **5 points**: Major feature with multiple components
- **8 points**: Complex feature requiring significant research
- **13 points**: Large feature that should be broken down

## 🔄 Iterative Refinement

### Story Refinement Process:
1. **Initial Generation**: Create stories from requirements
2. **Stakeholder Review**: Validate with business stakeholders
3. **Technical Review**: Assess feasibility with development team
4. **User Validation**: Test assumptions with target users
5. **Story Splitting**: Break down large stories into smaller ones
6. **Acceptance Criteria Enhancement**: Add missing scenarios
7. **Priority Adjustment**: Refine based on business value and risk

### Backlog Grooming:
- **Weekly Reviews**: Update priorities based on business changes
- **Sprint Planning**: Select stories for upcoming iteration
- **Retrospective Feedback**: Incorporate lessons learned
- **Continuous Refinement**: Keep stories current and actionable

## 📚 Related Templates

- [Requirements Analysis](./requirements-analysis.md)
- [Process Flow Documentation](./process-flow-documentation.md)
- [Stakeholder Analysis](./stakeholder-analysis.md)
- [Risk Assessment](./risk-assessment.md)
- [Compliance Requirements](./compliance-requirements.md)