# Process Flow Documentation Template for AI-Assisted Business Analysis

## 🎯 Overview

This template provides structured approaches for documenting and optimizing business processes using AI assistance. Perfect for business analysts who want to leverage AI tools for comprehensive process mapping, analysis, and improvement in fintech environments.

## 🔄 Core Process Flow Templates

### Business Process Mapping Prompt

```
You are a senior business analyst mapping processes for a fintech organization.

PROCESS CONTEXT:
- Process Name: [PROCESS_NAME]
- Process Owner: [DEPARTMENT/ROLE]
- Process Category: [Core/Support/Management]
- Frequency: [Daily/Weekly/Monthly/Ad-hoc]
- Stakeholders: [Internal and external parties involved]
- Regulatory Impact: [High/Medium/Low/None]

MAP THE COMPLETE PROCESS INCLUDING:

1. **Process Triggers**
   - Initiating events or conditions
   - Input requirements and sources
   - Prerequisites and dependencies
   - Timing and scheduling factors

2. **Process Steps** (in sequence)
   - Detailed activity descriptions
   - Responsible roles and actors
   - Decision points and criteria
   - Inputs, outputs, and transformations
   - Time estimates and SLAs

3. **Process Controls**
   - Quality checkpoints and validations  
   - Approval gates and authorization levels
   - Risk controls and mitigation measures
   - Compliance verification points
   - Exception handling procedures

4. **Process Outcomes**
   - Expected deliverables and outputs
   - Success criteria and measurements
   - Downstream impacts and notifications
   - Data updates and system changes
   - Customer or stakeholder communications

5. **Process Metrics**
   - Cycle time and throughput
   - Quality indicators and error rates
   - Cost and resource utilization
   - Customer satisfaction measures
   - Compliance and audit metrics

FORMAT: Provide a detailed process flow using BPMN notation descriptions, including swim lanes for different actors, decision diamonds, and parallel processing where applicable.

INCLUDE: Process improvement recommendations and automation opportunities.
```

### Process Analysis and Optimization Template

```
Analyze the current [PROCESS_NAME] and provide optimization recommendations.

CURRENT STATE ANALYSIS:
- Process Description: [BRIEF_OVERVIEW]
- Current Performance: [METRICS_AND_ISSUES]
- Pain Points: [KNOWN_PROBLEMS]
- Regulatory Requirements: [COMPLIANCE_NEEDS]
- Technology Environment: [CURRENT_SYSTEMS]

ANALYSIS FRAMEWORK:

1. **Efficiency Analysis**
   - Identify bottlenecks and delays
   - Calculate wait times and queue lengths
   - Analyze resource utilization
   - Map value-added vs non-value-added activities
   - Measure handoff points and rework instances

2. **Quality Analysis**
   - Identify error-prone steps
   - Analyze root causes of defects
   - Review quality control points
   - Assess customer satisfaction impact
   - Evaluate compliance gaps

3. **Cost Analysis**
   - Calculate process costs by activity
   - Identify resource-intensive steps
   - Analyze automation opportunities
   - Evaluate outsourcing potential
   - Assess technology investment needs

4. **Risk Analysis**
   - Identify operational risks
   - Assess compliance and regulatory risks
   - Evaluate security vulnerabilities
   - Analyze single points of failure
   - Review business continuity impacts

OPTIMIZATION RECOMMENDATIONS:

1. **Process Redesign**
   - Eliminate redundant steps
   - Combine related activities
   - Parallel processing opportunities
   - Reduce handoffs and approvals
   - Streamline decision making

2. **Technology Enhancement**
   - Automation opportunities
   - System integration improvements
   - Digital transformation initiatives
   - Self-service capabilities
   - Real-time monitoring implementation

3. **Performance Improvement**
   - SLA optimization
   - Resource reallocation
   - Training and skill development
   - Communication enhancement
   - Workflow standardization

DELIVERABLE: Provide current state process map, future state process map, gap analysis, and implementation roadmap with ROI projections.
```

## 💰 Fintech-Specific Process Templates

### Loan Origination Process Flow

```
Document the complete loan origination process from application to funding.

LOAN ORIGINATION CONTEXT:
- Loan Types: [Personal/Business/Mortgage/Auto]
- Loan Amounts: [Range and limits]
- Target Customers: [Customer segments]
- Regulatory Environment: [TILA, FCRA, ECOA, State regulations]
- Processing Goals: [Time to decision, approval rates, compliance]

LOAN ORIGINATION STAGES:

1. **Pre-Application Stage**
   - Customer acquisition channels
   - Lead qualification processes
   - Pre-qualification tools
   - Initial eligibility screening
   - Rate and terms presentation

2. **Application Stage**
   - Application form completion
   - Document collection requirements
   - Identity verification (KYC)
   - Employment and income verification
   - Credit history authorization

3. **Underwriting Stage**
   - Credit report retrieval and analysis
   - Income and asset verification
   - Debt-to-income calculations
   - Risk scoring and modeling
   - Policy and guideline application
   - Manual review triggers

4. **Decision Stage**
   - Automated decision processing
   - Manual underwriter review
   - Approval/denial determination
   - Terms and conditions finalization
   - Counter-offer generation

5. **Post-Decision Stage**
   - Decision communication
   - Document generation (Truth in Lending disclosures)
   - Loan agreement execution
   - Funding and disbursement
   - Loan setup and servicing handoff

PROCESS REQUIREMENTS:
- Decision timeframes (instant to 48 hours)
- Compliance documentation
- Audit trail maintenance
- Customer communication touchpoints
- Quality assurance checkpoints

AUTOMATION OPPORTUNITIES:
- Document collection and verification
- Credit scoring and risk assessment
- Compliance checking and validation
- Decision making for standard applications
- Customer communication and notifications

Generate detailed process flows with decision trees, exception handling, and compliance checkpoints.
```

### Payment Processing Workflow

```
Map the end-to-end payment processing workflow for multiple payment methods.

PAYMENT PROCESSING CONTEXT:
- Payment Methods: [Cards, ACH, Wire, Digital Wallets, BNPL]
- Transaction Types: [One-time, Recurring, Batch, Refunds]
- Processing Volumes: [Transactions per day/month]
- Geographic Scope: [Domestic/International]
- Compliance Requirements: [PCI DSS, AML, Regional regulations]

PAYMENT PROCESSING STAGES:

1. **Payment Initiation**
   - Customer payment method selection
   - Payment information capture
   - Tokenization and security processing
   - Initial validation and formatting
   - Fraud screening initiation

2. **Authorization Process**
   - Payment network routing
   - Issuer authorization request
   - Real-time fraud analysis
   - 3D Secure authentication (if required)
   - Authorization response handling

3. **Transaction Processing**
   - Payment capture and settlement
   - Currency conversion (if applicable)
   - Fee calculation and allocation
   - Merchant account processing
   - Network fee processing

4. **Post-Processing**
   - Transaction confirmation
   - Receipt generation and delivery
   - Accounting and reconciliation
   - Dispute and chargeback handling
   - Regulatory reporting

5. **Exception Handling**
   - Declined payment processing
   - Failed transaction recovery
   - Partial payment handling
   - Timeout and retry logic
   - Error notification and customer service

PROCESS FLOWS BY CHANNEL:
- Online/E-commerce checkout
- Point-of-sale (POS) systems
- Mobile application payments
- Recurring billing systems
- Business-to-business (B2B) payments

INTEGRATION TOUCHPOINTS:
- Payment gateways and processors
- Banking and card networks
- Fraud detection services
- Accounting and ERP systems
- Customer support platforms

MONITORING AND CONTROLS:
- Real-time transaction monitoring
- Performance dashboards
- Alert and escalation procedures
- Quality assurance processes
- Compliance audit trails

Create comprehensive workflow diagrams with swim lanes for different actors (customer, merchant, processor, bank) and include timing diagrams for performance optimization.
```

### KYC/AML Process Documentation

```
Document the Know Your Customer (KYC) and Anti-Money Laundering (AML) processes.

KYC/AML CONTEXT:
- Customer Types: [Individual, Business, High-risk, PEP]
- Risk Categories: [Low, Medium, High, Prohibited]
- Regulatory Framework: [BSA, PATRIOT Act, FATF, Local regulations]
- Verification Methods: [Documents, Biometrics, Database checks]
- Monitoring Requirements: [Ongoing, Transaction-based, Periodic review]

KYC PROCESS STAGES:

1. **Customer Identification**
   - Customer onboarding initiation
   - Identity document collection
   - Document verification and validation
   - Biometric capture and verification
   - Address and contact verification

2. **Customer Due Diligence (CDD)**
   - Risk assessment questionnaire
   - Source of funds verification
   - Business relationship purpose
   - Expected transaction patterns
   - Beneficial ownership identification (for entities)

3. **Enhanced Due Diligence (EDD)**
   - High-risk customer identification
   - Enhanced documentation requirements
   - Source of wealth verification
   - Enhanced monitoring setup
   - Senior management approval

4. **Ongoing Monitoring**
   - Transaction pattern analysis
   - Periodic customer review
   - Risk profile updates
   - Sanctions and PEP screening
   - Suspicious activity detection

AML MONITORING PROCESS:

1. **Transaction Screening**
   - Real-time transaction monitoring
   - Rule-based alert generation
   - Pattern recognition analysis
   - Threshold monitoring
   - Velocity checks

2. **Alert Investigation**
   - Alert triage and prioritization
   - Investigation workflow
   - Additional data collection
   - False positive identification
   - Case documentation

3. **Suspicious Activity Reporting**
   - SAR determination process
   - SAR filing requirements
   - Regulatory notification timelines
   - Case closure procedures
   - Record retention requirements

PROCESS CONTROLS:
- Independent validation procedures
- Quality assurance reviews
- Audit trail requirements
- Staff training and certification
- System access controls

TECHNOLOGY INTEGRATION:
- Identity verification services
- Sanctions and PEP databases
- Transaction monitoring systems
- Case management platforms
- Regulatory reporting tools

Provide detailed process maps with decision trees, escalation procedures, and compliance checkpoints for both individual and business customers.
```

## 📊 Process Documentation Templates

### Standard Operating Procedure (SOP) Template

```
Create a Standard Operating Procedure for [PROCESS_NAME].

SOP STRUCTURE:

1. **Purpose and Scope**
   - Process objectives and goals
   - Scope and boundaries
   - Applicable regulations and policies
   - Target audience and users

2. **Roles and Responsibilities**
   - Process owner and accountability
   - Key stakeholders and participants
   - Decision makers and approvers
   - Support functions and escalation contacts

3. **Process Overview**
   - High-level process flow
   - Key inputs and outputs
   - Success criteria and measurements
   - Related processes and dependencies

4. **Detailed Procedures**
   - Step-by-step instructions
   - Decision criteria and guidelines
   - Required forms and documentation
   - System interactions and data entry
   - Quality checks and validations

5. **Exception Handling**
   - Common exceptions and variations
   - Escalation procedures
   - Error recovery processes
   - Emergency procedures
   - Business continuity considerations

6. **Performance Metrics**
   - Key performance indicators (KPIs)
   - Service level agreements (SLAs)
   - Quality metrics and targets
   - Reporting requirements
   - Continuous improvement process

7. **Training and Compliance**
   - Required training and certification
   - Competency requirements
   - Compliance monitoring
   - Audit procedures
   - Record keeping requirements

8. **Document Control**
   - Version control and approval
   - Review and update schedule
   - Distribution and access controls
   - Related documents and references
   - Change management process

AI PROMPT FOR SOP GENERATION:
"Generate a comprehensive Standard Operating Procedure for [PROCESS_NAME] including step-by-step instructions, exception handling, and compliance requirements."
```

### Process Improvement Template

```
Conduct a comprehensive process improvement analysis for [PROCESS_NAME].

IMPROVEMENT METHODOLOGY:

1. **Current State Analysis**
   - Process mapping and documentation
   - Performance baseline establishment
   - Problem identification and root cause analysis
   - Stakeholder feedback collection
   - Compliance gap assessment

2. **Future State Design**
   - Process redesign and optimization
   - Automation opportunity identification
   - Technology enhancement requirements
   - Resource optimization plans
   - Risk mitigation strategies

3. **Gap Analysis**
   - Current vs future state comparison
   - Implementation requirements
   - Resource and skill gaps
   - Technology needs assessment
   - Change management requirements

4. **Implementation Planning**
   - Project timeline and milestones
   - Resource allocation and budgeting
   - Risk assessment and mitigation
   - Success metrics and KPIs
   - Communication and training plans

IMPROVEMENT FOCUS AREAS:

1. **Efficiency Improvements**
   - Cycle time reduction
   - Throughput increase
   - Resource optimization
   - Waste elimination
   - Automation implementation

2. **Quality Enhancements**
   - Error reduction
   - First-time-right improvements
   - Customer satisfaction increases
   - Compliance strengthening
   - Risk mitigation

3. **Cost Optimization**
   - Cost per transaction reduction
   - Resource productivity improvement
   - Technology ROI maximization
   - Outsourcing evaluation
   - Operational expense optimization

4. **Customer Experience**
   - Service delivery improvement
   - Response time reduction
   - Self-service capabilities
   - Communication enhancement
   - Accessibility improvements

IMPROVEMENT METRICS:
- Before/after performance comparison
- ROI and cost-benefit analysis
- Implementation success indicators
- Ongoing monitoring requirements
- Continuous improvement opportunities

AI IMPROVEMENT PROMPT:
"Analyze [PROCESS_NAME] for improvement opportunities and provide specific recommendations with implementation plans and ROI projections."
```

## 🔍 Process Analysis Templates

### Root Cause Analysis Template

```
Conduct root cause analysis for process issues in [PROCESS_NAME].

PROBLEM IDENTIFICATION:
- Problem Statement: [Clear description of the issue]
- Impact Assessment: [Business and customer impact]
- Frequency and Scope: [How often and where it occurs]
- Stakeholders Affected: [Who is impacted]
- Urgency Level: [Critical/High/Medium/Low]

ROOT CAUSE ANALYSIS METHODOLOGY:

1. **Problem Definition**
   - Detailed problem description
   - Symptoms vs root causes
   - Problem boundaries and scope
   - Success criteria for resolution
   - Timeline and urgency factors

2. **Data Collection**
   - Process performance data
   - Error logs and incident reports
   - Stakeholder interviews
   - System audit trails
   - Customer feedback

3. **Analysis Techniques**
   - 5 Whys analysis
   - Fishbone (Ishikawa) diagram
   - Fault tree analysis
   - Pareto analysis
   - Process flow analysis

4. **Root Cause Identification**
   - Primary root causes
   - Contributing factors
   - Systemic issues
   - Process design flaws
   - Human factors

5. **Solution Development**
   - Corrective actions for immediate fixes
   - Preventive measures for long-term solutions
   - Process improvements
   - System enhancements
   - Training and development needs

ANALYSIS CATEGORIES:

1. **People Factors**
   - Training and competency gaps
   - Communication breakdowns
   - Role clarity issues
   - Motivation and engagement
   - Performance management

2. **Process Factors**
   - Design flaws and inefficiencies
   - Missing controls and checkpoints
   - Unclear procedures
   - Inadequate exception handling
   - Poor integration points

3. **Technology Factors**
   - System limitations and bugs
   - Integration issues
   - Data quality problems
   - Performance bottlenecks
   - Security vulnerabilities

4. **Environmental Factors**
   - Regulatory changes
   - Market conditions
   - Organizational changes
   - Resource constraints
   - External dependencies

SOLUTION IMPLEMENTATION:
- Action plan with timelines
- Resource requirements
- Success metrics and monitoring
- Risk assessment and mitigation
- Change management approach

AI ROOT CAUSE PROMPT:
"Analyze the following process issue using the 5 Whys methodology and fishbone diagram approach: [PROBLEM_DESCRIPTION]"
```

### Process Risk Assessment Template

```
Conduct comprehensive risk assessment for [PROCESS_NAME].

RISK ASSESSMENT FRAMEWORK:

1. **Risk Identification**
   - Operational risks
   - Compliance and regulatory risks
   - Financial risks
   - Reputational risks
   - Strategic risks

2. **Risk Analysis**
   - Probability assessment (High/Medium/Low)
   - Impact assessment (Critical/High/Medium/Low)
   - Risk rating matrix
   - Interdependency analysis
   - Scenario modeling

3. **Risk Evaluation**
   - Risk tolerance thresholds
   - Regulatory requirements
   - Business impact assessment
   - Cost-benefit analysis
   - Stakeholder risk appetite

4. **Risk Treatment**
   - Risk mitigation strategies
   - Control implementation
   - Risk transfer options
   - Risk acceptance decisions
   - Monitoring and review plans

RISK CATEGORIES:

1. **Process Risks**
   - Process failure points
   - Quality control gaps
   - Performance bottlenecks
   - Resource dependencies
   - Integration vulnerabilities

2. **Compliance Risks**
   - Regulatory violation potential
   - Audit finding risks
   - Policy non-compliance
   - Documentation gaps
   - Training deficiencies

3. **Operational Risks**
   - System downtime impact
   - Human error potential
   - Fraud vulnerabilities
   - Business continuity threats
   - Third-party dependencies

4. **Financial Risks**
   - Cost overruns
   - Revenue impact
   - Penalty exposure
   - Loss potential
   - Investment risks

RISK CONTROLS:

1. **Preventive Controls**
   - Authorization and approval requirements
   - Segregation of duties
   - Input validation and verification
   - Access controls and security
   - Training and competency requirements

2. **Detective Controls**
   - Monitoring and surveillance
   - Exception reporting
   - Reconciliation procedures
   - Audit trails and logging
   - Performance monitoring

3. **Corrective Controls**
   - Exception handling procedures
   - Error correction processes
   - Incident response plans
   - Recovery procedures
   - Continuous improvement

RISK MONITORING:
- Key risk indicators (KRIs)
- Regular risk assessments
- Control effectiveness testing
- Incident tracking and analysis
- Risk reporting and escalation

AI RISK ASSESSMENT PROMPT:
"Identify and assess risks for [PROCESS_NAME] using a comprehensive risk framework, including probability, impact, and mitigation strategies."
```

## 📈 Process Performance Templates

### Key Performance Indicators (KPI) Framework

```
Develop KPIs and performance metrics for [PROCESS_NAME].

KPI DEVELOPMENT FRAMEWORK:

1. **Strategic Alignment**
   - Business objectives alignment
   - Stakeholder value creation
   - Competitive advantage support
   - Regulatory compliance support
   - Risk management contribution

2. **Performance Dimensions**
   - Efficiency metrics (time, cost, resources)
   - Quality metrics (accuracy, completeness, satisfaction)
   - Effectiveness metrics (outcomes, value delivery)
   - Compliance metrics (adherence, audit results)
   - Innovation metrics (improvement, adaptation)

3. **Measurement Approach**
   - Quantitative vs qualitative metrics
   - Leading vs lagging indicators
   - Absolute vs relative measurements
   - Benchmarking and targets
   - Frequency and timing

KPI CATEGORIES:

1. **Operational KPIs**
   - Cycle time and throughput
   - First-time-right rate
   - Error and rework rates
   - Resource utilization
   - Capacity and availability

2. **Customer KPIs**
   - Customer satisfaction scores
   - Service level achievement
   - Response and resolution times
   - Customer retention rates
   - Net Promoter Score (NPS)

3. **Financial KPIs**
   - Cost per transaction
   - Revenue per customer
   - Return on investment (ROI)
   - Cost reduction achievements
   - Profitability metrics

4. **Compliance KPIs**
   - Regulatory adherence rates
   - Audit finding trends
   - Policy compliance scores
   - Training completion rates
   - Risk incident frequency

5. **Innovation KPIs**
   - Process improvement implementations
   - Automation adoption rates
   - Digital transformation progress
   - Employee suggestion adoption
   - Technology utilization

KPI SPECIFICATION:
- KPI name and description
- Calculation formula
- Data sources and collection methods
- Target values and thresholds
- Reporting frequency and format
- Action triggers and escalation

PERFORMANCE DASHBOARD:
- Real-time monitoring capabilities
- Trend analysis and forecasting
- Exception highlighting
- Drill-down capabilities
- Mobile and self-service access

AI KPI DEVELOPMENT PROMPT:
"Create a comprehensive KPI framework for [PROCESS_NAME] including operational, customer, financial, and compliance metrics with targets and measurement approaches."
```

### Process Benchmarking Template

```
Conduct process benchmarking analysis for [PROCESS_NAME].

BENCHMARKING METHODOLOGY:

1. **Benchmarking Scope**
   - Process boundaries and scope
   - Performance dimensions to compare
   - Benchmarking partners and sources
   - Time frame and frequency
   - Success criteria and objectives

2. **Internal Benchmarking**
   - Cross-departmental comparisons
   - Historical performance analysis
   - Best practice identification
   - Lessons learned capture
   - Continuous improvement opportunities

3. **Competitive Benchmarking**
   - Industry peer comparison
   - Market leader analysis
   - Competitive advantage assessment
   - Performance gap identification
   - Strategic positioning

4. **Functional Benchmarking**
   - Best-in-class process comparison
   - Cross-industry learning
   - Innovation opportunity identification
   - Technology advancement evaluation
   - Breakthrough improvement potential

BENCHMARKING METRICS:

1. **Efficiency Benchmarks**
   - Cost per transaction
   - Processing time per unit
   - Resource productivity
   - Automation levels
   - Straight-through processing rates

2. **Quality Benchmarks**
   - Error rates and accuracy
   - Customer satisfaction scores
   - First-time-right rates
   - Compliance scores
   - Audit results

3. **Innovation Benchmarks**
   - Technology adoption rates
   - Digital transformation progress
   - Process automation levels
   - Self-service capabilities
   - Mobile accessibility

BENCHMARKING SOURCES:
- Industry reports and studies
- Regulatory benchmarking data
- Professional associations
- Consulting firm research
- Public company disclosures

GAP ANALYSIS:
- Current vs benchmark performance
- Root cause analysis of gaps
- Improvement opportunity prioritization
- Implementation feasibility assessment
- ROI and business case development

IMPROVEMENT ROADMAP:
- Short-term quick wins
- Medium-term strategic initiatives
- Long-term transformation projects
- Resource requirements and timelines
- Success metrics and monitoring

AI BENCHMARKING PROMPT:
"Compare [PROCESS_NAME] performance against industry benchmarks and identify improvement opportunities with implementation priorities."
```

## 🚀 Implementation Guidelines

### Process Implementation Roadmap

```
PROCESS IMPLEMENTATION STRATEGY:

1. **Preparation Phase**
   - Stakeholder alignment and buy-in
   - Resource allocation and planning
   - Risk assessment and mitigation
   - Communication and change management
   - Success criteria definition

2. **Design Phase**
   - Process design and documentation
   - Technology requirements definition
   - Training program development
   - Quality assurance planning
   - Pilot testing preparation

3. **Implementation Phase**
   - Pilot implementation and testing
   - Feedback collection and refinement
   - Full-scale rollout
   - Training delivery and support
   - Performance monitoring

4. **Optimization Phase**
   - Performance measurement and analysis
   - Continuous improvement implementation
   - Best practice sharing
   - Scaling and replication
   - Long-term sustainability

AI IMPLEMENTATION SUPPORT:
- Process documentation generation
- Training material development
- Performance monitoring setup
- Improvement recommendation generation
- Change impact assessment
```

---

*This template is part of the comprehensive AI-driven development course. For related templates, see the [Requirements Template](./requirements-template.md) and [User Story Template](./user-story-template.md).*