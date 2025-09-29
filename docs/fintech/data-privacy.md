# Data Privacy in Fintech: GDPR, CCPA, and Best Practices

## 🛡️ Overview

Data privacy is a critical concern for fintech applications that handle sensitive financial and personal information. This guide covers key privacy regulations, implementation strategies, and AI-assisted privacy compliance techniques.

## 📋 Privacy Regulatory Framework

### Key Privacy Regulations

| Regulation | Jurisdiction | Scope | Key Requirements |
|------------|-------------|-------|------------------|
| **GDPR** | EU/EEA | EU residents' data | Consent, rights, DPO, breach notification |
| **CCPA/CPRA** | California | CA residents' data | Transparency, deletion, opt-out rights |
| **LGPD** | Brazil | Brazilian residents | Consent, purpose limitation, data protection |
| **PIPEDA** | Canada | Personal information | Consent, purpose limitation, safeguards |
| **APPs** | Australia | Personal information | Collection limitation, security, access |

### Privacy Principles Matrix

```typescript
interface PrivacyPrinciple {
  principle: string;
  gdprRequirement: boolean;
  ccpaRequirement: boolean;
  implementation: string[];
}

const PRIVACY_PRINCIPLES: PrivacyPrinciple[] = [
  {
    principle: 'Lawfulness, Fairness, Transparency',
    gdprRequirement: true,
    ccpaRequirement: true,
    implementation: ['Privacy notices', 'Consent mechanisms', 'Purpose specification']
  },
  {
    principle: 'Purpose Limitation',
    gdprRequirement: true,
    ccpaRequirement: true,
    implementation: ['Data collection policies', 'Use restrictions', 'Retention schedules']
  },
  {
    principle: 'Data Minimization',
    gdprRequirement: true,
    ccpaRequirement: false,
    implementation: ['Collection controls', 'Field validation', 'Progressive disclosure']
  },
  {
    principle: 'Accuracy',
    gdprRequirement: true,
    ccpaRequirement: false,
    implementation: ['Data validation', 'Update mechanisms', 'Correction workflows']
  },
  {
    principle: 'Storage Limitation',
    gdprRequirement: true,
    ccpaRequirement: false,
    implementation: ['Retention policies', 'Automated deletion', 'Archive procedures']
  },
  {
    principle: 'Security',
    gdprRequirement: true,
    ccpaRequirement: true,
    implementation: ['Encryption', 'Access controls', 'Security monitoring']
  },
  {
    principle: 'Accountability',
    gdprRequirement: true,
    ccpaRequirement: true,
    implementation: ['Privacy impact assessments', 'Documentation', 'Governance']
  }
];
```

## 🔐 GDPR Compliance Implementation

### Consent Management System

```typescript
interface ConsentRecord {
  userId: string;
  purposes: ConsentPurpose[];
  timestamp: Date;
  ipAddress: string;
  userAgent: string;
  consentMethod: 'EXPLICIT' | 'IMPLICIT' | 'LEGITIMATE_INTEREST';
  withdrawal?: Date;
  renewalRequired?: Date;
}

class GDPRConsentManager {
  
  /**
   * Record explicit consent for data processing
   */
  async recordConsent(consentRequest: ConsentRequest): Promise<ConsentRecord> {
    // Validate consent request
    this.validateConsentRequest(consentRequest);
    
    // Create consent record
    const consentRecord: ConsentRecord = {
      userId: consentRequest.userId,
      purposes: consentRequest.purposes,
      timestamp: new Date(),
      ipAddress: consentRequest.ipAddress,
      userAgent: consentRequest.userAgent,
      consentMethod: consentRequest.method,
      renewalRequired: this.calculateRenewalDate(consentRequest.purposes)
    };
    
    // Store consent record
    await this.storeConsentRecord(consentRecord);
    
    // Log for audit trail
    await this.auditLogger.log({
      action: 'CONSENT_RECORDED',
      userId: consentRequest.userId,
      purposes: consentRequest.purposes.map(p => p.purpose),
      timestamp: new Date()
    });
    
    return consentRecord;
  }
  
  /**
   * Handle consent withdrawal
   */
  async withdrawConsent(userId: string, purposes: string[]): Promise<void> {
    // Find existing consent records
    const existingConsent = await this.getConsentRecord(userId);
    if (!existingConsent) {
      throw new Error('No consent record found');
    }
    
    // Update consent record with withdrawal
    const updatedConsent = {
      ...existingConsent,
      withdrawal: new Date(),
      purposes: existingConsent.purposes.map(p => 
        purposes.includes(p.purpose) 
          ? { ...p, withdrawn: true, withdrawalDate: new Date() }
          : p
      )
    };
    
    await this.updateConsentRecord(updatedConsent);
    
    // Trigger data processing cessation
    await this.ceaseDataProcessing(userId, purposes);
    
    // Log withdrawal
    await this.auditLogger.log({
      action: 'CONSENT_WITHDRAWN',
      userId,
      purposes,
      timestamp: new Date()
    });
  }
  
  /**
   * Check if processing is lawful based on current consent
   */
  async isProcessingLawful(userId: string, purpose: string): Promise<boolean> {
    const consentRecord = await this.getConsentRecord(userId);
    if (!consentRecord) return false;
    
    const relevantConsent = consentRecord.purposes.find(p => p.purpose === purpose);
    if (!relevantConsent) return false;
    
    // Check if consent is still valid
    return !relevantConsent.withdrawn && 
           (!consentRecord.renewalRequired || consentRecord.renewalRequired > new Date());
  }
}
```

### Data Subject Rights Implementation

```typescript
class DataSubjectRightsManager {
  
  /**
   * Handle Subject Access Requests (SAR)
   */
  async handleAccessRequest(request: AccessRequest): Promise<AccessResponse> {
    // Verify identity
    await this.verifyIdentity(request.userId, request.identityProof);
    
    // Collect all personal data
    const personalData = await this.collectPersonalData(request.userId);
    
    // Prepare export in machine-readable format
    const exportData = await this.prepareDataExport(personalData);
    
    // Generate access report
    const accessReport = {
      userId: request.userId,
      requestDate: request.timestamp,
      responseDate: new Date(),
      dataCategories: Object.keys(personalData),
      exportFormat: 'JSON',
      dataRetentionInfo: await this.getRetentionInfo(request.userId),
      processingPurposes: await this.getProcessingPurposes(request.userId),
      dataRecipients: await this.getDataRecipients(request.userId),
      rightToObject: 'Available for certain processing activities',
      rightToRectification: 'Available through account settings or customer service',
      rightToErasure: 'Available with certain limitations for regulatory compliance'
    };
    
    // Log the access request
    await this.auditLogger.log({
      action: 'ACCESS_REQUEST_FULFILLED',
      userId: request.userId,
      timestamp: new Date(),
      dataProvided: true
    });
    
    return {
      report: accessReport,
      exportData,
      deliveryMethod: request.deliveryMethod
    };
  }
  
  /**
   * Handle Right to Erasure (Right to be Forgotten)
   */
  async handleErasureRequest(request: ErasureRequest): Promise<ErasureResponse> {
    // Verify identity
    await this.verifyIdentity(request.userId, request.identityProof);
    
    // Check if erasure is permissible
    const erasureCheck = await this.checkErasurePermissibility(request.userId);
    if (!erasureCheck.permitted) {
      return {
        granted: false,
        reason: erasureCheck.reason,
        legalBasis: erasureCheck.legalBasis,
        retentionRequirements: erasureCheck.retentionRequirements
      };
    }
    
    // Perform data erasure
    const erasureResults = await this.performDataErasure(request.userId);
    
    // Notify third parties if data was shared
    await this.notifyThirdPartiesOfErasure(request.userId);
    
    // Log erasure
    await this.auditLogger.log({
      action: 'DATA_ERASED',
      userId: request.userId,
      erasureScope: erasureResults.scope,
      timestamp: new Date()
    });
    
    return {
      granted: true,
      erasureDate: new Date(),
      scope: erasureResults.scope,
      retainedData: erasureResults.retained,
      retentionReason: 'Regulatory compliance requirements'
    };
  }
  
  /**
   * Handle Data Portability Requests
   */
  async handlePortabilityRequest(request: PortabilityRequest): Promise<PortabilityResponse> {
    // Verify identity and consent
    await this.verifyIdentity(request.userId, request.identityProof);
    
    // Collect portable data (only data provided by user and processed with consent)
    const portableData = await this.collectPortableData(request.userId);
    
    // Format in structured, machine-readable format
    const formattedData = await this.formatForPortability(portableData, request.format);
    
    // If direct transfer requested, validate recipient
    if (request.directTransfer && request.recipient) {
      await this.validateTransferRecipient(request.recipient);
      await this.transferDataDirectly(formattedData, request.recipient);
    }
    
    return {
      userId: request.userId,
      dataExported: true,
      format: request.format,
      exportDate: new Date(),
      directTransfer: !!request.directTransfer,
      recipient: request.recipient
    };
  }
}
```

### Privacy Impact Assessment (PIA)

```typescript
class PrivacyImpactAssessment {
  
  /**
   * Conduct Privacy Impact Assessment for new features
   */
  async conductPIA(feature: FeatureDescription): Promise<PIAResult> {
    // 1. Assess necessity for PIA
    const piaRequired = await this.assessPIANecessity(feature);
    if (!piaRequired.required) {
      return { required: false, reason: piaRequired.reason };
    }
    
    // 2. Identify data processing activities
    const processingActivities = await this.identifyProcessingActivities(feature);
    
    // 3. Assess privacy risks
    const riskAssessment = await this.assessPrivacyRisks(processingActivities);
    
    // 4. Identify mitigation measures
    const mitigationMeasures = await this.identifyMitigations(riskAssessment);
    
    // 5. Calculate residual risk
    const residualRisk = await this.calculateResidualRisk(riskAssessment, mitigationMeasures);
    
    // 6. Generate recommendations
    const recommendations = await this.generateRecommendations(residualRisk);
    
    return {
      required: true,
      feature: feature.name,
      assessmentDate: new Date(),
      processingActivities,
      riskAssessment,
      mitigationMeasures,
      residualRisk,
      recommendations,
      approvalRequired: residualRisk.level === 'HIGH',
      dpoConsultationRequired: residualRisk.level !== 'LOW'
    };
  }
  
  /**
   * AI-assisted privacy risk identification
   */
  private async assessPrivacyRisks(activities: ProcessingActivity[]): Promise<RiskAssessment> {
    const risks = [];
    
    for (const activity of activities) {
      // Use AI to identify potential privacy risks
      const aiRiskAnalysis = await this.aiService.analyzePrivacyRisks({
        dataTypes: activity.dataTypes,
        processingPurposes: activity.purposes,
        dataSubjects: activity.dataSubjects,
        technicalMeasures: activity.technicalMeasures,
        organizationalMeasures: activity.organizationalMeasures
      });
      
      // Combine with rule-based risk assessment
      const ruleBasedRisks = await this.assessRuleBasedRisks(activity);
      
      risks.push({
        activity: activity.name,
        aiIdentifiedRisks: aiRiskAnalysis.risks,
        ruleBasedRisks,
        likelihood: Math.max(aiRiskAnalysis.likelihood, ruleBasedRisks.likelihood),
        severity: Math.max(aiRiskAnalysis.severity, ruleBasedRisks.severity),
        overallRisk: this.calculateRiskScore(aiRiskAnalysis, ruleBasedRisks)
      });
    }
    
    return {
      overallRiskLevel: this.determineOverallRiskLevel(risks),
      individualRisks: risks,
      highestRisks: risks.filter(r => r.overallRisk > 7).slice(0, 5)
    };
  }
}
```

## 📊 CCPA/CPRA Compliance

### Consumer Rights Implementation

```typescript
class CCPAComplianceManager {
  
  /**
   * Handle "Do Not Sell" requests
   */
  async handleDoNotSellRequest(request: DoNotSellRequest): Promise<void> {
    // Record opt-out preference
    await this.recordOptOutPreference(request.consumerId, {
      optOutType: 'SALE',
      timestamp: new Date(),
      method: request.method,
      ipAddress: request.ipAddress
    });
    
    // Stop all data sales for this consumer
    await this.stopDataSales(request.consumerId);
    
    // Notify third parties about opt-out
    await this.notifyPartnersOfOptOut(request.consumerId, 'SALE');
    
    // Update consent records
    await this.updateConsentForSaleOptOut(request.consumerId);
    
    // Confirm opt-out to consumer
    await this.sendOptOutConfirmation(request.consumerId, 'SALE');
  }
  
  /**
   * Handle "Do Not Share" requests (CPRA)
   */
  async handleDoNotShareRequest(request: DoNotShareRequest): Promise<void> {
    // Record sharing opt-out
    await this.recordOptOutPreference(request.consumerId, {
      optOutType: 'SHARING',
      timestamp: new Date(),
      method: request.method,
      ipAddress: request.ipAddress
    });
    
    // Stop cross-context behavioral advertising
    await this.stopCrossContextSharing(request.consumerId);
    
    // Update tracking preferences
    await this.updateTrackingPreferences(request.consumerId, {
      crossContextSharing: false,
      behavioralAdvertising: false
    });
  }
  
  /**
   * Generate CCPA-compliant privacy notice
   */
  async generatePrivacyNotice(): Promise<CCPAPrivacyNotice> {
    const dataCollectionInfo = await this.getDataCollectionInfo();
    const dataSharingInfo = await this.getDataSharingInfo();
    const consumerRights = await this.getConsumerRights();
    
    return {
      lastUpdated: new Date(),
      categories: {
        collected: dataCollectionInfo.categories,
        sold: dataSharingInfo.soldCategories,
        shared: dataSharingInfo.sharedCategories
      },
      purposes: dataCollectionInfo.purposes,
      recipients: dataSharingInfo.recipients,
      retentionPeriods: await this.getRetentionPeriods(),
      consumerRights: {
        know: {
          available: true,
          description: 'Right to know what personal information is collected, used, shared or sold'
        },
        delete: {
          available: true,
          description: 'Right to delete personal information',
          limitations: ['Regulatory compliance', 'Fraud prevention', 'Security']
        },
        optOut: {
          available: true,
          description: 'Right to opt out of sale/sharing of personal information'
        },
        nonDiscrimination: {
          available: true,
          description: 'Right to non-discriminatory treatment for exercising privacy rights'
        }
      },
      contactInfo: {
        email: 'privacy@company.com',
        phone: '1-800-PRIVACY',
        webform: 'https://company.com/privacy-request'
      }
    };
  }
}
```

### Sensitive Personal Information Handling

```typescript
class SensitiveDataManager {
  
  // CPRA sensitive personal information categories
  private readonly SENSITIVE_CATEGORIES = [
    'SSN', 'DRIVERS_LICENSE', 'PASSPORT', 'PRECISE_GEOLOCATION',
    'RACIAL_ETHNIC_ORIGIN', 'RELIGIOUS_BELIEFS', 'BIOMETRIC_DATA',
    'HEALTH_DATA', 'SEX_LIFE', 'SEXUAL_ORIENTATION'
  ];
  
  /**
   * Identify and classify sensitive personal information
   */
  async classifyDataSensitivity(data: PersonalData): Promise<SensitivityClassification> {
    const classification = {
      standard: [],
      sensitive: [],
      requiresOptIn: []
    };
    
    for (const [field, value] of Object.entries(data)) {
      const sensitivity = await this.assessFieldSensitivity(field, value);
      
      if (this.SENSITIVE_CATEGORIES.includes(sensitivity.category)) {
        classification.sensitive.push({
          field,
          category: sensitivity.category,
          confidence: sensitivity.confidence
        });
        
        // Check if opt-in consent required for processing
        if (await this.requiresOptInConsent(sensitivity.category)) {
          classification.requiresOptIn.push(field);
        }
      } else {
        classification.standard.push({
          field,
          category: sensitivity.category
        });
      }
    }
    
    return classification;
  }
  
  /**
   * AI-powered sensitive data detection
   */
  private async assessFieldSensitivity(field: string, value: any): Promise<SensitivityAssessment> {
    // Use AI to analyze field content for sensitive information
    const aiAnalysis = await this.aiService.analyzeSensitivity({
      fieldName: field,
      fieldValue: typeof value === 'string' ? value.substring(0, 100) : String(value),
      context: 'FINTECH_APPLICATION'
    });
    
    // Combine with rule-based detection
    const ruleBasedAnalysis = this.ruleBasedSensitivity(field, value);
    
    return {
      category: aiAnalysis.category || ruleBasedAnalysis.category,
      confidence: Math.max(aiAnalysis.confidence, ruleBasedAnalysis.confidence),
      reasoning: aiAnalysis.reasoning || ruleBasedAnalysis.reasoning
    };
  }
}
```

## 🔒 Technical Privacy Controls

### Data Anonymization and Pseudonymization

```typescript
class DataAnonymization {
  
  /**
   * Pseudonymize personal data for analytics
   */
  async pseudonymizeData(dataset: PersonalDataRecord[]): Promise<PseudonymizedDataset> {
    const pseudonymizedRecords = [];
    const keyMapping = new Map<string, string>();
    
    for (const record of dataset) {
      const pseudonymizedRecord = { ...record };
      
      // Replace direct identifiers with pseudonyms
      for (const identifier of ['userId', 'email', 'phone', 'ssn']) {
        if (pseudonymizedRecord[identifier]) {
          const pseudonym = await this.generatePseudonym(
            pseudonymizedRecord[identifier], 
            identifier
          );
          keyMapping.set(pseudonymizedRecord[identifier], pseudonym);
          pseudonymizedRecord[identifier] = pseudonym;
        }
      }
      
      // Apply k-anonymity to quasi-identifiers
      pseudonymizedRecord.age = this.applyKAnonymity(pseudonymizedRecord.age, 'age', 5);
      pseudonymizedRecord.zipCode = this.applyKAnonymity(pseudonymizedRecord.zipCode, 'zipCode', 5);
      
      // Remove or generalize highly identifying attributes
      delete pseudonymizedRecord.fullAddress;
      pseudonymizedRecord.city = this.generalizeLocation(pseudonymizedRecord.city);
      
      pseudonymizedRecords.push(pseudonymizedRecord);
    }
    
    return {
      records: pseudonymizedRecords,
      anonymizationLevel: await this.assessAnonymizationLevel(pseudonymizedRecords),
      reidentificationRisk: await this.assessReidentificationRisk(pseudonymizedRecords),
      keyMapping: this.encryptKeyMapping(keyMapping)
    };
  }
  
  /**
   * Apply differential privacy for statistical queries
   */
  async applyDifferentialPrivacy(
    query: StatisticalQuery, 
    epsilon: number = 1.0
  ): Promise<DifferentialPrivacyResult> {
    // Execute original query
    const trueResult = await this.executeQuery(query);
    
    // Calculate sensitivity of the query
    const sensitivity = await this.calculateQuerySensitivity(query);
    
    // Add calibrated noise
    const noise = this.generateLaplaceNoise(sensitivity / epsilon);
    const noisyResult = trueResult + noise;
    
    // Track privacy budget consumption
    await this.updatePrivacyBudget(query.userId, epsilon);
    
    return {
      result: noisyResult,
      epsilon,
      sensitivity,
      noiseAdded: noise,
      privacyBudgetRemaining: await this.getRemainingPrivacyBudget(query.userId)
    };
  }
}
```

### Privacy-Preserving Analytics

```typescript
class PrivacyPreservingAnalytics {
  
  /**
   * Federated learning for customer insights without data sharing
   */
  async performFederatedAnalysis(analysisRequest: FederatedAnalysisRequest): Promise<AnalysisResult> {
    // Initialize federated learning parameters
    const federatedParams = {
      rounds: 10,
      clientSelection: 0.3,
      localEpochs: 5,
      learningRate: 0.01
    };
    
    // Coordinate federated learning across data silos
    const participants = await this.selectParticipants(
      analysisRequest.participants, 
      federatedParams.clientSelection
    );
    
    let globalModel = await this.initializeGlobalModel(analysisRequest.modelType);
    
    for (let round = 0; round < federatedParams.rounds; round++) {
      // Send global model to participants
      const localUpdates = await Promise.all(
        participants.map(participant => 
          this.trainLocalModel(participant, globalModel, federatedParams.localEpochs)
        )
      );
      
      // Aggregate local updates with differential privacy
      globalModel = await this.aggregateWithPrivacy(localUpdates, {
        epsilon: 1.0,
        delta: 1e-5
      });
      
      // Evaluate model performance
      const performance = await this.evaluateModel(globalModel, analysisRequest.testData);
      if (performance.accuracy > analysisRequest.targetAccuracy) {
        break;
      }
    }
    
    return {
      model: globalModel,
      accuracy: await this.evaluateModel(globalModel, analysisRequest.testData),
      privacyGuarantees: {
        epsilon: federatedParams.rounds * 1.0,
        delta: 1e-5
      },
      participantCount: participants.length
    };
  }
  
  /**
   * Homomorphic encryption for encrypted computation
   */
  async performEncryptedComputation(computation: EncryptedComputation): Promise<EncryptedResult> {
    // Initialize homomorphic encryption scheme
    const heScheme = await this.initializeHEScheme('CKKS');
    
    // Encrypt input data
    const encryptedInputs = await Promise.all(
      computation.inputs.map(input => heScheme.encrypt(input))
    );
    
    // Perform computation on encrypted data
    let result = encryptedInputs[0];
    for (let i = 1; i < encryptedInputs.length; i++) {
      switch (computation.operation) {
        case 'ADD':
          result = heScheme.add(result, encryptedInputs[i]);
          break;
        case 'MULTIPLY':
          result = heScheme.multiply(result, encryptedInputs[i]);
          break;
        case 'POLYNOMIAL':
          result = heScheme.evaluatePolynomial(result, computation.coefficients);
          break;
      }
    }
    
    return {
      encryptedResult: result,
      scheme: 'CKKS',
      computationProof: await this.generateComputationProof(computation, result)
    };
  }
}
```

## 🧪 Privacy Testing and Validation

### Automated Privacy Testing

```typescript
describe('Data Privacy Compliance Tests', () => {
  
  describe('GDPR Consent Management', () => {
    it('should record explicit consent properly', async () => {
      const consentRequest = {
        userId: 'test-user-123',
        purposes: [
          { purpose: 'MARKETING', lawfulBasis: 'CONSENT' },
          { purpose: 'ANALYTICS', lawfulBasis: 'LEGITIMATE_INTEREST' }
        ],
        method: 'EXPLICIT',
        ipAddress: '192.168.1.1',
        userAgent: 'Mozilla/5.0...'
      };
      
      const consentRecord = await consentManager.recordConsent(consentRequest);
      
      expect(consentRecord.userId).toBe('test-user-123');
      expect(consentRecord.purposes).toHaveLength(2);
      expect(consentRecord.consentMethod).toBe('EXPLICIT');
      expect(consentRecord.timestamp).toBeDefined();
    });
    
    it('should handle consent withdrawal correctly', async () => {
      const userId = 'test-user-123';
      const purposes = ['MARKETING'];
      
      await consentManager.withdrawConsent(userId, purposes);
      
      const isLawful = await consentManager.isProcessingLawful(userId, 'MARKETING');
      expect(isLawful).toBe(false);
    });
  });
  
  describe('Data Subject Rights', () => {
    it('should fulfill access requests within 30 days', async () => {
      const accessRequest = {
        userId: 'test-user-123',
        timestamp: new Date(),
        identityProof: 'verified',
        deliveryMethod: 'EMAIL'
      };
      
      const response = await rightsManager.handleAccessRequest(accessRequest);
      
      expect(response.report).toBeDefined();
      expect(response.exportData).toBeDefined();
      expect(response.report.dataCategories.length).toBeGreaterThan(0);
    });
    
    it('should handle erasure requests with regulatory exceptions', async () => {
      const erasureRequest = {
        userId: 'test-user-with-loans',
        timestamp: new Date(),
        identityProof: 'verified'
      };
      
      const response = await rightsManager.handleErasureRequest(erasureRequest);
      
      // Should not grant full erasure due to regulatory requirements
      expect(response.granted).toBe(false);
      expect(response.reason).toContain('regulatory compliance');
      expect(response.retentionRequirements).toBeDefined();
    });
  });
  
  describe('Data Anonymization', () => {
    it('should achieve k-anonymity of at least 5', async () => {
      const testDataset = generateTestDataset(1000);
      const anonymized = await anonymizer.pseudonymizeData(testDataset);
      
      expect(anonymized.anonymizationLevel.kAnonymity).toBeGreaterThanOrEqual(5);
      expect(anonymized.reidentificationRisk).toBeLessThan(0.2);
    });
    
    it('should apply differential privacy correctly', async () => {
      const query = {
        type: 'COUNT',
        table: 'customers',
        filters: { age: { $gte: 18, $lte: 65 } },
        userId: 'analyst-123'
      };
      
      const result = await analytics.applyDifferentialPrivacy(query, 1.0);
      
      expect(result.epsilon).toBe(1.0);
      expect(result.noiseAdded).toBeDefined();
      expect(Math.abs(result.noiseAdded)).toBeGreaterThan(0);
    });
  });
  
  describe('CCPA Compliance', () => {
    it('should handle "Do Not Sell" requests', async () => {
      const optOutRequest = {
        consumerId: 'ca-consumer-123',
        method: 'WEB_FORM',
        ipAddress: '192.168.1.1',
        timestamp: new Date()
      };
      
      await ccpaManager.handleDoNotSellRequest(optOutRequest);
      
      const optOutStatus = await ccpaManager.getOptOutStatus('ca-consumer-123');
      expect(optOutStatus.saleOptOut).toBe(true);
      expect(optOutStatus.optOutDate).toBeDefined();
    });
  });
});
```

### Privacy Risk Assessment

```typescript
class PrivacyRiskAssessment {
  
  /**
   * Automated privacy risk scanning
   */
  async scanForPrivacyRisks(): Promise<PrivacyRiskReport> {
    const risks = [];
    
    // Scan for data minimization issues
    const dataMinimizationRisks = await this.scanDataMinimization();
    risks.push(...dataMinimizationRisks);
    
    // Scan for retention policy violations
    const retentionRisks = await this.scanRetentionCompliance();
    risks.push(...retentionRisks);
    
    // Scan for consent issues
    const consentRisks = await this.scanConsentCompliance();
    risks.push(...consentRisks);
    
    // Scan for data sharing without proper basis
    const sharingRisks = await this.scanDataSharing();
    risks.push(...sharingRisks);
    
    return {
      totalRisks: risks.length,
      highRisks: risks.filter(r => r.severity === 'HIGH').length,
      mediumRisks: risks.filter(r => r.severity === 'MEDIUM').length,
      lowRisks: risks.filter(r => r.severity === 'LOW').length,
      risks,
      recommendations: await this.generateRiskRecommendations(risks),
      nextScanDate: this.calculateNextScanDate()
    };
  }
}
```

## 📋 Privacy Compliance Checklist

### Implementation Checklist

- [ ] **Legal Basis and Consent**
  - [ ] Lawful basis identified for all processing activities
  - [ ] Explicit consent mechanisms implemented
  - [ ] Consent withdrawal functionality
  - [ ] Legitimate interest assessments completed

- [ ] **Data Subject Rights**
  - [ ] Access request handling (30-day response)
  - [ ] Data portability in machine-readable format
  - [ ] Erasure request processing with exceptions
  - [ ] Rectification mechanisms

- [ ] **Technical Measures**
  - [ ] Data encryption at rest and in transit
  - [ ] Pseudonymization for analytics
  - [ ] Access controls and audit logging
  - [ ] Data minimization controls

- [ ] **Organizational Measures**
  - [ ] Privacy policy and notices
  - [ ] Staff privacy training
  - [ ] Privacy impact assessments
  - [ ] Data processing records (Article 30)

- [ ] **Cross-Border Transfers**
  - [ ] Adequacy decisions verified
  - [ ] Standard contractual clauses in place
  - [ ] Transfer impact assessments
  - [ ] Binding corporate rules (if applicable)

## 🚨 Privacy Incident Response

### Data Breach Response Plan

```typescript
class PrivacyIncidentResponse {
  
  /**
   * Handle privacy incidents and data breaches
   */
  async handlePrivacyIncident(incident: PrivacyIncident): Promise<IncidentResponse> {
    // 1. Immediate containment
    await this.containIncident(incident);
    
    // 2. Assess severity and scope
    const assessment = await this.assessIncidentSeverity(incident);
    
    // 3. Regulatory notification (72 hours for GDPR)
    if (assessment.regulatoryNotificationRequired) {
      await this.notifyRegulators(incident, assessment);
    }
    
    // 4. Individual notification if high risk
    if (assessment.individualNotificationRequired) {
      await this.notifyAffectedIndividuals(incident, assessment);
    }
    
    // 5. Document incident
    await this.documentIncident(incident, assessment);
    
    // 6. Implement remediation
    const remediation = await this.implementRemediation(incident);
    
    return {
      incidentId: incident.id,
      containedAt: new Date(),
      assessment,
      regulatoryNotified: assessment.regulatoryNotificationRequired,
      individualsNotified: assessment.individualNotificationRequired,
      remediation,
      followUpRequired: assessment.severity === 'HIGH'
    };
  }
}
```

---

*This guide is part of the comprehensive AI-driven development course. For implementation examples, see the [sample application](../../sample-app/README.md).*