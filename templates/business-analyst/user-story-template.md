# User Story Generation Template for AI-Assisted Business Analysis

## 🎯 Overview

This template provides structured prompts and frameworks for generating high-quality user stories using AI tools. Perfect for business analysts working on fintech applications who want to leverage GitHub Copilot, Cursor AI, or ChatGPT for efficient user story creation.

## 📝 Core User Story Templates

### Basic User Story Generation Prompt

```
You are a senior business analyst creating user stories for a fintech application.

CONTEXT:
- Product: [PRODUCT_NAME] - [BRIEF_DESCRIPTION]
- User Persona: [PERSONA_NAME] - [PERSONA_DESCRIPTION]
- Epic: [EPIC_NAME] - [EPIC_DESCRIPTION]
- Sprint Goal: [SPRINT_OBJECTIVE]

GENERATE USER STORIES using this format:
"As a [persona], I want [functionality] so that [business value]"

INCLUDE FOR EACH STORY:
1. **Acceptance Criteria** (Given-When-Then format)
2. **Story Points** (Fibonacci scale: 1, 2, 3, 5, 8, 13)
3. **Priority** (Must have, Should have, Could have, Won't have)
4. **Dependencies** (technical or business)
5. **Definition of Done** (completion criteria)

REQUIREMENTS:
- Focus on user value and business outcomes
- Keep stories testable and deliverable in one sprint
- Include both happy path and edge cases
- Consider security, compliance, and performance aspects
- Ensure stories are independent and negotiable

Generate [NUMBER] user stories for [FEATURE_AREA].
```

### Persona-Specific Story Templates

#### Retail Banking Customer Stories

```
Generate user stories for retail banking customers using our digital banking platform.

CUSTOMER PERSONA: Sarah Chen
- Age: 32, Marketing Manager
- Tech-savvy, mobile-first user
- Goals: Convenient banking, financial insights, saving money
- Pain Points: Long wait times, complex processes, hidden fees
- Preferred Channels: Mobile app, online banking

BANKING FEATURES TO COVER:
- Account management
- Money transfers and payments
- Budgeting and financial planning
- Customer support
- Security and authentication

USER STORY FORMAT:
As Sarah, a busy professional,
I want [specific functionality]
So that [business value/outcome]

ACCEPTANCE CRITERIA MUST INCLUDE:
- Mobile-responsive design requirements
- Security and authentication steps
- Performance expectations (load times < 3 seconds)
- Error handling and recovery scenarios
- Accessibility compliance (WCAG 2.1 AA)

COMPLIANCE CONSIDERATIONS:
- Data privacy (GDPR, CCPA)
- Financial regulations (PCI DSS, SOX)
- Audit trail requirements
- Consumer protection laws

Generate 10 user stories covering the complete customer journey from onboarding to advanced features.
```

#### Small Business Owner Stories

```
Create user stories for small business owners using our fintech payment processing platform.

BUSINESS OWNER PERSONA: Marcus Rodriguez
- Business: Local restaurant with 15 employees
- Experience: Limited tech background, busy schedule
- Goals: Streamline payments, reduce costs, improve cash flow
- Pain Points: Complex setup, high fees, poor customer support
- Usage Context: Point-of-sale, online orders, mobile payments

PAYMENT PROCESSING FEATURES:
- Account setup and onboarding
- Payment acceptance (cards, digital wallets, ACH)
- Transaction management and reporting
- Invoicing and billing
- Integration with accounting systems

USER STORY STRUCTURE:
As Marcus, a small business owner,
I want [payment functionality]
So that [business benefit]

BUSINESS REQUIREMENTS:
- Quick setup and easy configuration
- Transparent pricing and fee structure
- Real-time reporting and analytics
- Multi-channel payment acceptance
- Integration capabilities

ACCEPTANCE CRITERIA MUST ADDRESS:
- PCI DSS compliance requirements
- Multi-device compatibility
- Transaction limits and security controls
- Dispute and chargeback handling
- Customer support accessibility

Generate comprehensive user stories for the complete business payment lifecycle.
```

#### Loan Officer Stories

```
Develop user stories for loan officers using our digital lending platform.

LOAN OFFICER PERSONA: Jennifer Park
- Role: Senior Loan Officer at regional bank
- Experience: 8 years in lending, moderate tech skills
- Goals: Efficient application processing, risk assessment, customer service
- Pain Points: Manual processes, incomplete applications, regulatory compliance
- Daily Tasks: Application review, credit analysis, customer communication

LENDING PLATFORM FEATURES:
- Application intake and management
- Credit scoring and risk assessment
- Document collection and verification
- Loan approval workflows
- Customer communication tools

USER STORY TEMPLATE:
As Jennifer, a loan officer,
I want [lending functionality]
So that [operational efficiency/customer outcome]

REGULATORY REQUIREMENTS:
- Fair Credit Reporting Act (FCRA) compliance
- Equal Credit Opportunity Act (ECOA) adherence
- Truth in Lending Act (TILA) disclosures
- Anti-discrimination measures
- Audit trail and documentation

ACCEPTANCE CRITERIA FRAMEWORK:
- Workflow efficiency improvements
- Compliance validation checkpoints
- Integration with credit bureaus
- Customer communication touchpoints
- Risk management controls

Create user stories covering the entire loan origination process from application to closing.
```

## 🏗️ Epic-Level Story Templates

### Account Opening Epic

```
Generate a comprehensive set of user stories for the "Digital Account Opening" epic.

EPIC OVERVIEW:
- Epic Name: Digital Account Opening
- Business Value: Reduce onboarding time from 30 minutes to 5 minutes
- Success Metrics: 80% completion rate, 90% customer satisfaction
- Compliance: KYC, AML, BSA, Patriot Act requirements

USER PERSONAS INVOLVED:
1. First-time customer (tech-savvy)
2. Existing customer (adding accounts)
3. Senior customer (needs assistance)
4. Business customer (complex requirements)

ACCOUNT TYPES:
- Checking accounts
- Savings accounts
- Money market accounts
- Certificate of deposit
- Business accounts

STORY CATEGORIES:
1. **Identity Verification Stories**
   - Document upload and verification
   - Biometric authentication
   - Knowledge-based authentication
   - Identity fraud prevention

2. **Account Configuration Stories**
   - Account type selection
   - Feature customization
   - Beneficiary designation
   - Service preferences

3. **Funding Stories**
   - Initial deposit methods
   - ACH setup and verification
   - Debit card requests
   - Check ordering

4. **Onboarding Completion Stories**
   - Welcome sequence
   - Feature tutorials
   - Customer support access
   - Account activation confirmation

STORY REQUIREMENTS:
- Each story must be completable in one sprint
- Include mobile and web versions
- Address accessibility requirements
- Consider regulatory compliance
- Include analytics and tracking

Generate detailed user stories with acceptance criteria for each category.
```

### Payment Processing Epic

```
Create user stories for the "Multi-Channel Payment Processing" epic.

EPIC CONTEXT:
- Epic Name: Multi-Channel Payment Processing
- Objective: Support all major payment methods across all channels
- Target: Process 10,000+ transactions daily with 99.9% uptime
- Compliance: PCI DSS Level 1, regional payment regulations

PAYMENT CHANNELS:
- Point of Sale (POS) systems
- E-commerce websites
- Mobile applications
- Phone/call center
- Recurring billing systems

PAYMENT METHODS:
- Credit and debit cards
- Digital wallets (Apple Pay, Google Pay, PayPal)
- Bank transfers (ACH, wire)
- Buy now, pay later (BNPL)
- Cryptocurrency (where applicable)

STORY THEMES:
1. **Payment Acceptance Stories**
   - Payment method selection
   - Card data capture and tokenization
   - Authentication and authorization
   - Real-time fraud screening

2. **Transaction Processing Stories**
   - Authorization requests
   - Settlement and clearing
   - Currency conversion
   - Partial payments and installments

3. **Customer Experience Stories**
   - Checkout optimization
   - Payment status updates
   - Receipt and confirmation
   - Payment method management

4. **Merchant Management Stories**
   - Transaction monitoring
   - Dispute management
   - Reporting and analytics
   - Payout processing

TECHNICAL REQUIREMENTS:
- API-first architecture
- Real-time processing
- Comprehensive logging
- Webhook notifications
- Multi-tenant security

Generate user stories that cover the complete payment ecosystem from customer initiation to merchant settlement.
```

## 📊 Specialized Fintech Story Templates

### Compliance and Risk Management Stories

```
Generate user stories for compliance officers and risk managers in a fintech environment.

COMPLIANCE OFFICER PERSONA: David Kim
- Role: Chief Compliance Officer
- Responsibilities: Regulatory adherence, risk monitoring, audit management
- Goals: Maintain compliance, minimize regulatory risk, efficient reporting
- Challenges: Evolving regulations, complex reporting requirements, audit preparation

RISK MANAGER PERSONA: Lisa Thompson
- Role: Senior Risk Manager
- Focus Areas: Credit risk, operational risk, fraud prevention
- Objectives: Risk mitigation, early detection, regulatory compliance
- Daily Tasks: Risk assessment, monitoring dashboards, incident response

COMPLIANCE AND RISK STORIES:

1. **Regulatory Monitoring Stories**
   As David, a compliance officer,
   I want automated regulatory change tracking
   So that I can ensure our policies remain current and compliant

2. **Risk Assessment Stories**
   As Lisa, a risk manager,
   I want real-time risk scoring for all transactions
   So that I can identify and mitigate potential losses immediately

3. **Audit Preparation Stories**
   As David, a compliance officer,
   I want comprehensive audit trails for all customer interactions
   So that I can demonstrate compliance during regulatory examinations

4. **Incident Management Stories**
   As Lisa, a risk manager,
   I want automated incident detection and escalation
   So that I can respond to risk events within regulatory timeframes

COMPLIANCE REQUIREMENTS:
- SOX controls and documentation
- AML monitoring and reporting
- Consumer protection compliance
- Data privacy regulations
- Operational risk management

ACCEPTANCE CRITERIA FOCUS:
- Regulatory deadline adherence
- Audit trail completeness
- Real-time monitoring capabilities
- Escalation and notification systems
- Documentation and reporting quality

Create detailed stories covering the complete compliance and risk management lifecycle.
```

### Customer Support Stories

```
Develop user stories for customer support representatives in a fintech support center.

SUPPORT REPRESENTATIVE PERSONA: Amanda Foster
- Role: Senior Customer Support Specialist
- Experience: 5 years in fintech customer service
- Goals: Quick issue resolution, high customer satisfaction, efficient workflows
- Tools: CRM system, knowledge base, screen sharing, ticket management
- Metrics: First call resolution, customer satisfaction scores, average handle time

SUPPORT SCENARIOS:
- Account access issues
- Transaction disputes
- Payment problems
- Account setup assistance
- Fraud reporting
- Feature explanations

CUSTOMER SUPPORT STORIES:

1. **Issue Resolution Stories**
   As Amanda, a support representative,
   I want comprehensive customer context when handling calls
   So that I can resolve issues quickly without asking customers to repeat information

2. **Knowledge Management Stories**
   As Amanda, a support representative,
   I want AI-powered solution suggestions based on customer issues
   So that I can provide accurate answers and reduce resolution time

3. **Escalation Stories**
   As Amanda, a support representative,
   I want clear escalation paths for complex issues
   So that customers receive expert help when needed

4. **Customer Communication Stories**
   As Amanda, a support representative,
   I want multi-channel communication tools
   So that I can assist customers through their preferred contact method

SUPPORT REQUIREMENTS:
- Omnichannel support capabilities
- Real-time customer data access
- Integrated knowledge management
- Case tracking and escalation
- Performance analytics and reporting

ACCEPTANCE CRITERIA ELEMENTS:
- Response time requirements
- Data privacy and security controls
- System integration capabilities
- Customer satisfaction measurements
- Compliance with support regulations

Generate stories that cover the complete customer support journey from initial contact to issue resolution.
```

## 🎨 Advanced Story Techniques

### Story Splitting Templates

```
LARGE STORY SPLITTING TECHNIQUE:

Original Large Story:
"As a customer, I want to apply for a loan online so that I can get quick access to funding"

SPLIT INTO SMALLER STORIES:

1. **Application Initiation**
   As a customer, I want to start a loan application with basic information
   So that I can begin the funding process quickly

2. **Document Upload**
   As a customer, I want to upload required documents during my application
   So that I can complete the verification process efficiently

3. **Credit Check Authorization**
   As a customer, I want to authorize credit checks during my application
   So that the lender can assess my creditworthiness

4. **Application Review Status**
   As a customer, I want to check my application status in real-time
   So that I know where my application stands in the process

5. **Decision Notification**
   As a customer, I want to receive immediate notification of loan decisions
   So that I can proceed with next steps quickly

SPLITTING CRITERIA:
- Each story delivers independent value
- Stories are testable individually
- Each fits within a single sprint
- Dependencies are clearly identified
- Acceptance criteria are specific and measurable

AI PROMPT FOR STORY SPLITTING:
"Split this large user story into smaller, independent stories that each deliver value and can be completed in one sprint: [LARGE_STORY]"
```

### Story Refinement Template

```
STORY REFINEMENT PROCESS:

STEP 1: Story Analysis
Analyze this user story for improvement opportunities:
[STORY_TEXT]

STEP 2: INVEST Criteria Check
Evaluate the story against INVEST criteria:
- Independent: Can it be developed independently?
- Negotiable: Is the implementation approach flexible?
- Valuable: Does it deliver clear business value?
- Estimable: Can the team estimate effort accurately?
- Small: Can it be completed in one sprint?
- Testable: Are acceptance criteria verifiable?

STEP 3: Story Enhancement
Improve the story by:
- Clarifying user persona and context
- Sharpening the business value proposition
- Adding specific acceptance criteria
- Including edge cases and error scenarios
- Considering non-functional requirements

STEP 4: Dependency Identification
Identify and document:
- Technical dependencies
- Business dependencies
- External service dependencies
- Data dependencies
- Resource dependencies

AI REFINEMENT PROMPT:
"Refine this user story by applying INVEST criteria and adding comprehensive acceptance criteria: [STORY_TEXT]"
```

### Story Estimation Template

```
STORY POINT ESTIMATION GUIDE:

STORY COMPLEXITY FACTORS:
1. **Technical Complexity**
   - New technology or framework
   - Complex algorithms or logic
   - Integration requirements
   - Performance considerations

2. **Business Complexity**
   - Regulatory requirements
   - Multiple user personas
   - Complex business rules
   - External stakeholder involvement

3. **Uncertainty and Risk**
   - Unknown technical challenges
   - Unclear requirements
   - Dependency on external teams
   - New team member involvement

ESTIMATION SCALE:
- 1 Point: Simple, well-understood tasks (< 4 hours)
- 2 Points: Minor complexity, clear requirements (4-8 hours)
- 3 Points: Moderate complexity, some unknowns (1-2 days)
- 5 Points: Significant complexity, multiple components (2-3 days)
- 8 Points: High complexity, significant unknowns (3-5 days)
- 13 Points: Very complex, requires splitting (> 5 days)

REFERENCE STORIES:
Maintain a catalog of previously estimated stories as reference points for consistent estimation.

AI ESTIMATION PROMPT:
"Estimate story points for this user story considering technical complexity, business rules, and risk factors: [STORY_TEXT]"
```

## 📋 Quality Assurance Templates

### Story Review Checklist

```
USER STORY QUALITY CHECKLIST:

FORMAT AND STRUCTURE:
□ Follows "As a [persona], I want [functionality], so that [business value]" format
□ Persona is specific and well-defined
□ Functionality is clear and actionable
□ Business value is explicit and measurable

ACCEPTANCE CRITERIA:
□ Written in Given-When-Then format
□ Covers happy path scenarios
□ Includes edge cases and error conditions
□ Addresses non-functional requirements
□ Specifies measurable outcomes

COMPLETENESS:
□ All necessary information included
□ Dependencies clearly identified
□ Story points estimated
□ Priority assigned (MoSCoW)
□ Definition of Done specified

QUALITY ATTRIBUTES:
□ Independent of other stories
□ Negotiable implementation approach
□ Valuable to business and users
□ Estimable by development team
□ Small enough for one sprint
□ Testable with clear verification criteria

COMPLIANCE AND SECURITY:
□ Regulatory requirements addressed
□ Security considerations included
□ Privacy and data protection covered
□ Audit and logging requirements specified
□ Risk mitigation measures defined

AI REVIEW PROMPT:
"Review this user story for completeness, clarity, and quality using the INVEST criteria: [STORY_TEXT]"
```

### Story Testing Template

```
USER STORY TESTING FRAMEWORK:

ACCEPTANCE TESTING APPROACH:
1. **Scenario-Based Testing**
   - Create test scenarios from acceptance criteria
   - Cover both positive and negative cases
   - Include boundary value testing
   - Test error handling and recovery

2. **User Experience Testing**
   - Validate user workflow completion
   - Test across different devices and browsers
   - Verify accessibility compliance
   - Measure performance against criteria

3. **Integration Testing**
   - Test system integrations
   - Verify data flow between components
   - Validate external service interactions
   - Test security controls and authentication

4. **Compliance Testing**
   - Verify regulatory requirement adherence
   - Test audit trail generation
   - Validate data privacy controls
   - Check security compliance measures

TEST DATA REQUIREMENTS:
- Valid user personas and accounts
- Edge case data scenarios
- Error condition triggers
- Performance testing datasets
- Security testing scenarios

AI TESTING PROMPT:
"Generate comprehensive test scenarios for this user story including positive cases, edge cases, and compliance validation: [STORY_TEXT]"
```

## 🚀 Implementation Guidelines

### Story Development Workflow

```
AGILE STORY DEVELOPMENT PROCESS:

1. **Story Creation**
   - Use AI prompts to generate initial stories
   - Apply persona-specific templates
   - Include business context and value

2. **Story Refinement**
   - Review with stakeholders
   - Apply INVEST criteria
   - Add detailed acceptance criteria
   - Estimate story points

3. **Story Validation**
   - Business value confirmation
   - Technical feasibility review
   - Compliance requirement check
   - User experience validation

4. **Story Implementation**
   - Development task breakdown
   - Progress tracking and updates
   - Continuous stakeholder feedback
   - Quality assurance testing

5. **Story Completion**
   - Acceptance criteria verification
   - User acceptance testing
   - Definition of Done confirmation
   - Story closure and retrospective

AI WORKFLOW SUPPORT:
- Story generation and refinement
- Acceptance criteria creation
- Test scenario development
- Documentation updates
```

---

*This template is part of the comprehensive AI-driven development course. For related templates, see the [Requirements Template](./requirements-template.md) and [Process Flow Template](./process-flow-template.md).*