# Advanced AI Prompt Patterns

Sophisticated prompting techniques for complex development scenarios and professional workflows.

## 🎯 Overview

Advanced prompt patterns go beyond basic code generation to create sophisticated workflows that handle complex business logic, architectural decisions, and enterprise-level development challenges.

## 🏗️ Architectural Patterns

### System Design Pattern
```
Prompt Template:
"Design a [system type] for [business domain] with the following requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Consider:
- Scalability for [expected load]
- Security requirements: [security needs]
- Integration with: [existing systems]
- Technology constraints: [constraints]

Provide:
1. High-level architecture diagram (text-based)
2. Technology stack recommendations
3. Data flow description
4. Potential challenges and solutions"

Example:
"Design a payment processing system for a fintech startup with:
- Handle 10,000 transactions per minute
- PCI DSS compliance required
- Integration with banks and card networks
- Real-time fraud detection
- Multi-currency support"
```

### Microservices Decomposition Pattern
```
"I have a monolithic [application type] with these main functions:
[List functions]

Help me decompose this into microservices by:
1. Identifying service boundaries
2. Defining data ownership
3. Mapping inter-service communication
4. Identifying shared concerns
5. Suggesting deployment strategy

Consider:
- Domain-driven design principles
- Data consistency requirements
- Performance implications
- Operational complexity"
```

## 🔄 Workflow Orchestration Patterns

### Multi-Step Process Pattern
```
"Create a workflow for [business process] that involves:

Step 1: [First step description]
- Input: [inputs]
- Validation: [validation rules]
- Output: [outputs]
- Error handling: [error scenarios]

Step 2: [Second step description]
- Dependencies: [what needs to complete first]
- Processing: [processing logic]
- Side effects: [logging, notifications, etc.]

[Continue for all steps]

Requirements:
- Handle failures gracefully
- Support retry mechanisms
- Provide audit trail
- Enable monitoring and alerting

Implement using [technology stack]"
```

### State Machine Pattern
```
"Model a [entity] state machine with:

States: [list all states]
Transitions: [list all valid transitions]
Events: [list triggering events]
Guards: [list conditions]
Actions: [list side effects]

Generate:
1. State transition diagram (text)
2. Implementation code
3. Unit tests for all transitions
4. Error handling for invalid transitions
5. Logging and monitoring hooks"
```

## 🧠 Complex Logic Patterns

### Business Rules Engine Pattern
```
"Create a business rules engine for [domain] that:

1. Evaluates complex conditions:
   - [Condition type 1]: [examples]
   - [Condition type 2]: [examples]
   - [Condition type 3]: [examples]

2. Supports rule composition:
   - AND/OR logic
   - Nested conditions
   - Priority ordering
   - Rule conflicts resolution

3. Provides:
   - Rule execution tracing
   - Performance monitoring
   - Rule validation
   - Dynamic rule loading

Implementation requirements:
- [Performance requirements]
- [Scalability requirements]
- [Maintainability requirements]"
```

### Algorithm Optimization Pattern
```
"I have an algorithm that [current behavior] with these characteristics:
- Time complexity: [current complexity]
- Space complexity: [current complexity]
- Typical input size: [size range]
- Performance bottlenecks: [identified issues]

Optimize for:
- [Primary optimization goal]
- [Secondary optimization goal]
- [Constraints to maintain]

Provide:
1. Optimized algorithm with complexity analysis
2. Trade-offs explanation
3. Benchmark code
4. Alternative approaches comparison
5. When to use each approach"
```

## 📊 Data Processing Patterns

### ETL Pipeline Pattern
```
"Design an ETL pipeline for [data source] to [destination] with:

Extraction:
- Source: [source details]
- Format: [data format]
- Volume: [data volume]
- Frequency: [update frequency]
- Challenges: [source-specific issues]

Transformation:
- [Transformation 1]: [description]
- [Transformation 2]: [description]
- Data quality rules: [validation rules]
- Error handling: [error scenarios]

Loading:
- Destination: [target system]
- Loading strategy: [incremental/full]
- Performance requirements: [SLA]
- Rollback strategy: [failure handling]

Provide complete implementation with monitoring and alerting."
```

### Real-time Stream Processing Pattern
```
"Create a stream processing system for [use case] that:

Input Streams:
- [Stream 1]: [characteristics]
- [Stream 2]: [characteristics]

Processing:
- [Processing rule 1]
- [Processing rule 2]
- Windowing: [time windows]
- Aggregations: [aggregation types]

Output:
- [Output destination 1]
- [Output destination 2]
- Alerting conditions: [alert rules]

Requirements:
- Latency: [latency requirements]
- Throughput: [throughput requirements]
- Fault tolerance: [reliability needs]"
```

## 🔐 Security Patterns

### Zero Trust Architecture Pattern
```
"Implement zero trust security for [application/system] with:

Identity Verification:
- Authentication methods: [methods]
- Authorization model: [RBAC/ABAC]
- Token management: [JWT/OAuth]

Network Security:
- Micro-segmentation: [network zones]
- Traffic encryption: [encryption requirements]
- Network monitoring: [monitoring needs]

Data Protection:
- Data classification: [classification levels]
- Encryption at rest: [encryption requirements]
- Encryption in transit: [transport security]

Monitoring:
- Threat detection: [detection capabilities]
- Anomaly detection: [behavioral analysis]
- Incident response: [response procedures]"
```

### Compliance Framework Pattern
```
"Implement [compliance standard] compliance for [system type]:

Requirements Analysis:
- [Requirement category 1]: [specific requirements]
- [Requirement category 2]: [specific requirements]

Implementation:
- Technical controls: [control implementations]
- Process controls: [process definitions]
- Monitoring controls: [monitoring setup]

Documentation:
- Policy documents: [required policies]
- Procedure documents: [required procedures]
- Evidence collection: [audit trail setup]

Validation:
- Compliance testing: [test procedures]
- Audit preparation: [audit readiness]
- Continuous monitoring: [ongoing compliance]"
```

## 🧪 Testing Patterns

### Comprehensive Test Strategy Pattern
```
"Create a comprehensive test strategy for [system/feature] including:

Unit Testing:
- Coverage targets: [coverage requirements]
- Mock strategies: [mocking approach]
- Test data management: [data approach]

Integration Testing:
- Integration points: [systems to test]
- Test environments: [environment setup]
- Data synchronization: [data management]

End-to-End Testing:
- User journeys: [critical paths]
- Test automation: [automation tools]
- Performance testing: [performance scenarios]

Specialty Testing:
- Security testing: [security scenarios]
- Accessibility testing: [accessibility requirements]
- Chaos engineering: [failure scenarios]

Test Infrastructure:
- CI/CD integration: [pipeline integration]
- Test reporting: [reporting requirements]
- Test maintenance: [maintenance procedures]"
```

## 🚀 Performance Patterns

### Caching Strategy Pattern
```
"Design a comprehensive caching strategy for [application] with:

Cache Layers:
- [Layer 1]: [cache type and purpose]
- [Layer 2]: [cache type and purpose]
- [Layer 3]: [cache type and purpose]

Cache Policies:
- TTL strategies: [expiration policies]
- Eviction policies: [eviction strategies]
- Invalidation strategies: [invalidation triggers]

Consistency:
- Cache coherence: [consistency requirements]
- Update propagation: [update strategies]
- Conflict resolution: [conflict handling]

Monitoring:
- Hit/miss ratios: [monitoring setup]
- Performance metrics: [key metrics]
- Capacity planning: [scaling strategies]"
```

## 📈 Monitoring and Observability Patterns

### Full-Stack Observability Pattern
```
"Implement comprehensive observability for [system] including:

Metrics:
- Business metrics: [KPIs to track]
- Technical metrics: [system metrics]
- SLI/SLO definitions: [service level objectives]

Logging:
- Structured logging: [log format]
- Log aggregation: [centralization strategy]
- Log retention: [retention policies]

Tracing:
- Distributed tracing: [tracing strategy]
- Trace sampling: [sampling policies]
- Trace analysis: [analysis tools]

Alerting:
- Alert conditions: [alerting rules]
- Alert routing: [notification strategy]
- Alert fatigue prevention: [alert optimization]

Dashboards:
- Operational dashboards: [ops views]
- Business dashboards: [business views]
- Incident dashboards: [incident response]"
```

## 🔧 DevOps Patterns

### Infrastructure as Code Pattern
```
"Create infrastructure as code for [infrastructure type] with:

Infrastructure Components:
- [Component 1]: [specifications]
- [Component 2]: [specifications]
- [Component 3]: [specifications]

Environment Management:
- Environment definitions: [dev/staging/prod]
- Configuration management: [config strategy]
- Secret management: [secret handling]

Deployment:
- Deployment strategies: [deployment approach]
- Rollback procedures: [rollback strategy]
- Health checks: [health monitoring]

Compliance:
- Security policies: [security requirements]
- Cost optimization: [cost controls]
- Resource tagging: [tagging strategy]"
```

## 🎯 Prompt Optimization Techniques

### Iterative Refinement
```
1. Start with basic prompt
2. Add specific constraints
3. Include examples
4. Specify output format
5. Add error handling requirements
6. Include edge cases
7. Request alternatives
```

### Context Layering
```
"Given the following context:
[Layer 1: Business context]
[Layer 2: Technical context]
[Layer 3: Constraint context]
[Layer 4: Quality context]

[Your specific request]

Consider all layers when providing the solution."
```

## 📚 Pattern Library

### Reusable Prompt Components
```
Qual
ity Requirements Template:
"Ensure the solution:
- Follows [coding standards]
- Includes comprehensive error handling
- Has [performance requirements]
- Meets [security requirements]
- Includes logging and monitoring
- Has unit tests with [coverage]% coverage
- Includes documentation"

Constraints Template:
"Within these constraints:
- Technology stack: [stack]
- Performance: [requirements]
- Security: [requirements]
- Scalability: [requirements]
- Budget: [limitations]
- Timeline: [deadlines]"
```

---

*Advanced patterns require iterative refinement and domain expertise. Start simple and gradually add complexity as you master each pattern.*
