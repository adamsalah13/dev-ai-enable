# Requirements Gathering Template for AI-Assisted Business Analysis

## 🎯 Overview

This template provides structured prompts and frameworks for AI-assisted requirements gathering in fintech applications. Use these templates with GitHub Copilot, Cursor AI, or ChatGPT to efficiently capture, analyze, and document business requirements.

## 📋 Core Requirements Templates

### Business Requirements Analysis Prompt

```
You are a senior business analyst working on a fintech application for [PROJECT_NAME]. 

CONTEXT:
- Industry: [INDUSTRY_SECTOR] (e.g., digital lending, payments, wealth management)
- Target Users: [USER_PERSONAS] (e.g., retail customers, SMBs, enterprises)
- Regulatory Environment: [REGULATIONS] (e.g., PCI DSS, GDPR, SOX, CCPA)
- Business Scale: [SCALE] (e.g., startup, growth-stage, enterprise)

TASK: Generate comprehensive business requirements for [FEATURE_NAME] that include:

1. **Business Objectives**
   - Primary business goals and success metrics
   - Expected ROI and business value
   - Strategic alignment with company objectives

2. **User Needs and Pain Points**
   - Current user journey and friction points
   - Desired user experience improvements
   - User acceptance criteria

3. **Functional Requirements**
   - Core feature functionality
   - User interactions and workflows
   - System behaviors and responses

4. **Non-Functional Requirements**
   - Performance expectations (response times, throughput)
   - Security and compliance requirements
   - Scalability and availability needs

5. **Business Rules and Logic**
   - Validation rules and constraints
   - Decision logic and approval workflows
   - Exception handling procedures

6. **Integration Requirements**
   - Third-party service dependencies
   - Internal system integrations
   - Data exchange requirements

7. **Compliance and Risk Requirements**
   - Regulatory compliance obligations
   - Risk mitigation measures
   - Audit and reporting needs

FORMAT: Provide detailed requirements in user story format with acceptance criteria.
INCLUDE: Assumptions, constraints, and success metrics for each requirement.
PRIORITIZE: Requirements using MoSCoW method (Must have, Should have, Could have, Won't have).
```

### Stakeholder Analysis Template

```
As a business analyst, help me analyze stakeholders for [PROJECT_NAME].

PROJECT CONTEXT:
- Project: [PROJECT_DESCRIPTION]
- Duration: [TIMELINE]
- Budget: [BUDGET_RANGE]
- Complexity: [LOW/MEDIUM/HIGH]

ANALYZE THE FOLLOWING STAKEHOLDER CATEGORIES:

1. **Primary Stakeholders** (directly impacted)
   - End users and customers
   - Business sponsors and owners
   - Product managers and executives

2. **Secondary Stakeholders** (indirectly impacted)
   - IT teams and developers
   - Compliance and risk teams
   - Customer support teams

3. **External Stakeholders**
   - Regulatory bodies
   - Third-party vendors
   - Integration partners

FOR EACH STAKEHOLDER, PROVIDE:
- Name/Role and organization
- Interest level (High/Medium/Low)
- Influence level (High/Medium/Low)
- Impact on project success
- Communication preferences
- Key concerns and requirements
- Success criteria from their perspective

DELIVERABLE: Stakeholder matrix with engagement strategy and communication plan.
```

## 💰 Fintech-Specific Requirements Templates

### Digital Lending Requirements

```
You are analyzing requirements for a digital lending platform. Generate comprehensive requirements for [LENDING_PRODUCT] that address:

LENDING PRODUCT TYPE: [Personal loans / Business loans / Mortgage / BNPL / Payday alternative]
TARGET MARKET: [Consumer segment, business size, credit tier]
LOAN PARAMETERS: [Amount range, term options, rate structure]

CORE LENDING REQUIREMENTS:

1. **Application and Origination**
   - Online application process
   - Document collection and verification
   - Credit assessment and underwriting
   - Identity verification (KYC/AML)
   - Decision engine integration

2. **Risk Assessment**
   - Credit scoring models
   - Alternative data sources
   - Fraud detection mechanisms
   - Income verification methods
   - Debt-to-income calculations

3. **Compliance Requirements**
   - Truth in Lending Act (TILA) disclosures
   - Fair Credit Reporting Act (FCRA) compliance
   - Equal Credit Opportunity Act (ECOA) adherence
   - State-specific lending regulations
   - Anti-discrimination measures

4. **Loan Servicing**
   - Payment processing and scheduling
   - Customer account management
   - Collections and delinquency management
   - Modification and forbearance options
   - Customer communication preferences

5. **Reporting and Analytics**
   - Regulatory reporting requirements
   - Performance metrics and KPIs
   - Risk monitoring dashboards
   - Audit trail and documentation

INCLUDE: Specific user stories with acceptance criteria, business rules, and compliance considerations.
```

### Payment Processing Requirements

```
Generate detailed requirements for payment processing functionality in a fintech application.

PAYMENT CONTEXT:
- Payment Types: [Card payments, ACH, Wire, Digital wallets, Crypto]
- Transaction Volume: [Expected daily/monthly volume]
- Average Transaction Size: [Amount range]
- Geographic Scope: [Domestic/International]
- PCI Compliance Level: [Level 1/2/3/4]

PAYMENT REQUIREMENTS:

1. **Payment Acceptance**
   - Supported payment methods
   - Card brand acceptance (Visa, MC, Amex, Discover)
   - Digital wallet integration (Apple Pay, Google Pay, PayPal)
   - Bank account verification (ACH/Open Banking)
   - Alternative payment methods

2. **Security and Compliance**
   - PCI DSS compliance implementation
   - Tokenization of sensitive data
   - Encryption in transit and at rest
   - Fraud detection and prevention
   - 3D Secure authentication

3. **Transaction Processing**
   - Real-time authorization
   - Settlement and clearing processes
   - Multi-currency support
   - Partial payments and installments
   - Recurring payment setup

4. **User Experience**
   - Checkout flow optimization
   - Mobile payment experience
   - Payment method storage
   - Transaction history and receipts
   - Error handling and recovery

5. **Integration Requirements**
   - Payment gateway APIs
   - Webhook handling
   - Accounting system integration
   - CRM synchronization
   - Reporting and analytics tools

DELIVERABLE: Comprehensive payment requirements with security controls, user flows, and integration specifications.
```

### KYC/AML Requirements Template

```
Develop comprehensive KYC/AML requirements for a fintech application handling [BUSINESS_TYPE] transactions.

REGULATORY CONTEXT:
- Jurisdiction: [US/EU/UK/Multi-jurisdiction]
- Business Type: [MSB/Bank/Payment processor/Investment firm]
- Risk Level: [Low/Medium/High]
- Customer Types: [Individual/Business/Both]
- Transaction Volume: [Volume and value thresholds]

KYC/AML REQUIREMENTS:

1. **Customer Identification Program (CIP)**
   - Identity verification methods
   - Document collection requirements
   - Biometric verification options
   - Beneficial ownership identification
   - PEP (Politically Exposed Person) screening

2. **Customer Due Diligence (CDD)**
   - Risk assessment frameworks
   - Enhanced Due Diligence (EDD) triggers
   - Ongoing monitoring requirements
   - Customer risk rating systems
   - Periodic review schedules

3. **Transaction Monitoring**
   - Suspicious activity detection rules
   - Threshold-based monitoring
   - Pattern recognition algorithms
   - Real-time screening systems
   - Case management workflows

4. **Reporting and Documentation**
   - Suspicious Activity Report (SAR) generation
   - Currency Transaction Report (CTR) filing
   - Record keeping requirements
   - Audit trail maintenance
   - Regulatory submission processes

5. **Compliance Management**
   - Policy and procedure documentation
   - Staff training requirements
   - Independent testing programs
   - Compliance officer designation
   - Board oversight responsibilities

INCLUDE: Specific workflows, decision trees, and integration requirements with third-party verification services.
```

## 🔄 Process Flow Requirements

### Business Process Mapping Template

```
Help me map the business process for [PROCESS_NAME] in a fintech application.

PROCESS OVERVIEW:
- Process Name: [PROCESS_NAME]
- Process Owner: [DEPARTMENT/ROLE]
- Process Frequency: [Daily/Weekly/Monthly/On-demand]
- Process Complexity: [Simple/Moderate/Complex]
- Regulatory Impact: [High/Medium/Low]

PROCESS MAPPING REQUIREMENTS:

1. **Process Inputs**
   - Triggering events or conditions
   - Required data and information
   - Source systems and dependencies
   - User roles and permissions needed

2. **Process Steps**
   - Sequential workflow activities
   - Decision points and branches
   - Approval gates and checkpoints
   - Parallel processing opportunities
   - Exception handling procedures

3. **Process Outputs**
   - Expected deliverables
   - Data updates and notifications
   - Downstream system impacts
   - Reporting and audit trails

4. **Process Controls**
   - Quality assurance checkpoints
   - Risk mitigation measures
   - Compliance validation steps
   - Performance monitoring points

5. **Process Metrics**
   - Cycle time measurements
   - Quality indicators
   - Volume and capacity metrics
   - Error rates and exceptions

DELIVERABLE: 
- Process flow diagram (BPMN notation)
- Detailed process documentation
- System requirements derived from process needs
- Performance benchmarks and SLAs
```

### User Journey Mapping Template

```
Create a comprehensive user journey map for [USER_PERSONA] using [FEATURE/SERVICE].

USER CONTEXT:
- User Persona: [PERSONA_NAME and characteristics]
- User Goal: [Primary objective]
- User Experience Level: [First-time/Returning/Expert]
- Device/Channel: [Mobile/Web/API/Branch]
- Context of Use: [Situational factors]

JOURNEY MAPPING ELEMENTS:

1. **Pre-Journey Phase**
   - User needs and motivations
   - Awareness and research activities
   - External influences and triggers
   - Initial expectations and concerns

2. **Journey Touchpoints**
   - All interaction points with the system
   - User actions and inputs required
   - System responses and feedback
   - Support and help resources available

3. **User Experience Layers**
   - Emotional journey (feelings and frustrations)
   - Functional journey (tasks and activities)
   - Technical journey (system interactions)
   - Social journey (peer influences and reviews)

4. **Pain Points and Opportunities**
   - Current friction areas
   - Moments of delight
   - Abandonment risks
   - Improvement opportunities

5. **Business Impact**
   - Conversion metrics
   - Revenue implications
   - Cost considerations
   - Risk factors

DELIVERABLE: Visual journey map with detailed requirements for each touchpoint, including functional specifications and success metrics.
```

## 📊 Requirements Validation Templates

### Acceptance Criteria Template

```
Generate comprehensive acceptance criteria for [USER_STORY] using the Given-When-Then format.

USER STORY: [As a [role], I want [functionality] so that [business value]]

ACCEPTANCE CRITERIA STRUCTURE:

1. **Happy Path Scenarios**
   Given [initial context/preconditions]
   When [user action or system trigger]
   Then [expected outcome or system behavior]
   And [additional verification points]

2. **Alternative Flows**
   Given [different context]
   When [alternative action]
   Then [alternative outcome]

3. **Edge Cases**
   Given [boundary conditions]
   When [edge case trigger]
   Then [expected handling]

4. **Error Handling**
   Given [error conditions]
   When [error trigger]
   Then [error response and recovery]

5. **Non-Functional Criteria**
   - Performance: Response time < [X] seconds
   - Security: Encryption and access controls applied
   - Compliance: Regulatory requirements met
   - Accessibility: WCAG guidelines followed
   - Usability: User task completion rate > [X]%

VALIDATION METHODS:
- Unit testing approach
- Integration testing scenarios
- User acceptance testing steps
- Performance testing criteria
- Security testing requirements

INCLUDE: Test data requirements, mock services needed, and environment setup specifications.
```

### Requirements Traceability Template

```
Create a requirements traceability matrix for [PROJECT/FEATURE].

TRACEABILITY SCOPE:
- Business Requirements: [High-level business objectives]
- Functional Requirements: [Detailed feature specifications]
- Non-Functional Requirements: [Performance, security, usability]
- Technical Requirements: [System and integration needs]
- Test Requirements: [Validation and verification needs]

TRACEABILITY MATRIX STRUCTURE:

1. **Forward Traceability**
   Business Requirement → Functional Requirements → Design Elements → Test Cases

2. **Backward Traceability**
   Test Cases → Design Elements → Functional Requirements → Business Requirements

3. **Bi-Directional Links**
   - Requirement ID and description
   - Source stakeholder/document
   - Priority and category
   - Implementation status
   - Test coverage
   - Verification results

4. **Impact Analysis**
   - Change impact assessment
   - Dependency mapping
   - Risk analysis
   - Effort estimation

5. **Coverage Analysis**
   - Requirements coverage by tests
   - Test coverage by requirements
   - Gap identification
   - Completeness metrics

DELIVERABLE: Traceability matrix with automated links between requirements, design, code, and tests.
```

## 🎯 Success Metrics and KPIs

### Requirements Success Metrics

```
Define success metrics and KPIs for requirements gathering and management on [PROJECT_NAME].

METRICS CATEGORIES:

1. **Requirements Quality Metrics**
   - Requirements completeness percentage
   - Requirements clarity score (stakeholder feedback)
   - Requirements stability (change frequency)
   - Requirements testability index
   - Ambiguity detection rate

2. **Process Efficiency Metrics**
   - Time to capture requirements
   - Stakeholder engagement levels
   - Requirements approval cycle time
   - Change request processing time
   - Requirements review effectiveness

3. **Project Impact Metrics**
   - Requirements-related defects
   - Scope creep incidents
   - Rework due to unclear requirements
   - Stakeholder satisfaction scores
   - Project timeline adherence

4. **Business Value Metrics**
   - Feature adoption rates
   - User satisfaction scores
   - Business objective achievement
   - ROI from requirements investment
   - Compliance adherence levels

MEASUREMENT APPROACH:
- Data collection methods
- Reporting frequency
- Stakeholder communication
- Continuous improvement process
- Benchmarking against industry standards

TARGET BENCHMARKS:
- Requirements completion: >95%
- Stakeholder approval: <5 days
- Change request impact: <10% scope increase
- Defect prevention: >80% fewer requirements-related bugs
```

## 🛠️ Tools and Techniques

### AI-Assisted Requirements Elicitation

```
TECHNIQUE: AI-Powered Stakeholder Interviews

PREPARATION PROMPT:
"Generate interview questions for [STAKEHOLDER_ROLE] regarding [PROJECT_FEATURE]. Include:
- Open-ended discovery questions
- Scenario-based questions
- Pain point identification
- Success criteria definition
- Constraint and assumption validation"

ANALYSIS PROMPT:
"Analyze these interview transcripts and extract:
- Key themes and patterns
- Functional requirements
- Non-functional requirements
- Business rules and constraints
- Success criteria and metrics
- Risk factors and assumptions"

VALIDATION PROMPT:
"Review these requirements for:
- Completeness and consistency
- Clarity and testability
- Feasibility and constraints
- Priority and dependencies
- Compliance and risk factors"
```

### Requirements Documentation Templates

```
COMPREHENSIVE REQUIREMENTS DOCUMENT STRUCTURE:

1. **Executive Summary**
   - Project overview and objectives
   - Key stakeholders and sponsors
   - Success criteria and metrics
   - Timeline and resource needs

2. **Business Context**
   - Market analysis and opportunities
   - Competitive landscape
   - Regulatory environment
   - Strategic alignment

3. **User Analysis**
   - User personas and scenarios
   - User journey mapping
   - Pain points and opportunities
   - Experience requirements

4. **Functional Requirements**
   - Feature specifications
   - User stories and acceptance criteria
   - Business rules and logic
   - Integration requirements

5. **Non-Functional Requirements**
   - Performance and scalability
   - Security and compliance
   - Availability and reliability
   - Usability and accessibility

6. **Technical Constraints**
   - Technology stack limitations
   - Integration dependencies
   - Data and security requirements
   - Infrastructure needs

7. **Implementation Planning**
   - Phased delivery approach
   - Dependencies and risks
   - Resource requirements
   - Success metrics and KPIs

USE WITH AI: "Generate a detailed [SECTION_NAME] for our fintech [PROJECT_TYPE] based on the following context: [CONTEXT]"
```

---

*This template is part of the comprehensive AI-driven development course. For related templates, see the [User Story Template](./user-story-template.md) and [Process Flow Template](./process-flow-template.md).*