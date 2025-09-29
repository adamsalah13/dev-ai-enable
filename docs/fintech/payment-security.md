# Payment Security Best Practices for Fintech Applications

## 🛡️ Overview

This guide provides comprehensive security best practices for implementing payment processing in fintech applications. These practices ensure compliance with industry standards while maintaining optimal security posture.

## 🎯 Security Framework

### Defense in Depth Strategy

```
┌─────────────────┐
│   Application   │ ← Input validation, authentication, authorization
├─────────────────┤
│    Network      │ ← TLS/SSL, VPN, firewall rules
├─────────────────┤
│   Infrastructure│ ← Encryption at rest, secure hosting
├─────────────────┤
│   Compliance    │ ← PCI DSS, SOX, audit logging
└─────────────────┘
```

## 🔐 Core Security Principles

### 1. Never Store Raw Payment Data

```typescript
// ❌ NEVER do this
interface PaymentRequest {
  cardNumber: string;        // Raw PAN - Never store!
  expiryDate: string;       // Sensitive data
  cvv: string;              // Highly sensitive
}

// ✅ Always tokenize sensitive data
interface SecurePaymentRequest {
  paymentToken: string;     // Tokenized card reference
  merchantId: string;       // Your merchant identifier
  amount: number;           // Transaction amount
  currency: string;         // Currency code
  transactionId: string;    // Unique transaction ID
}
```

### 2. Implement Proper Tokenization

```typescript
import { randomBytes, createHash } from 'crypto';

class PaymentTokenizer {
  private static readonly TOKEN_LENGTH = 32;
  
  /**
   * Generate a secure payment token
   */
  static generateToken(cardNumber: string, merchantId: string): string {
    // Create deterministic hash for card lookup
    const cardHash = createHash('sha256')
      .update(cardNumber + merchantId + process.env.TOKEN_SALT)
      .digest('hex');
    
    // Generate random token for storage
    const randomToken = randomBytes(PaymentTokenizer.TOKEN_LENGTH)
      .toString('hex');
    
    // Store mapping securely (encrypted database)
    this.storeTokenMapping(randomToken, cardHash);
    
    return randomToken;
  }
  
  /**
   * Validate token format and existence
   */
  static async validateToken(token: string): Promise<boolean> {
    if (!token || token.length !== PaymentTokenizer.TOKEN_LENGTH * 2) {
      return false;
    }
    
    return await this.tokenExists(token);
  }
}
```

### 3. Secure API Design

```typescript
import express from 'express';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';
import { body, validationResult } from 'express-validator';

// Security middleware stack
const securityMiddleware = [
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https:"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    }
  }),
  
  // Rate limiting for payment endpoints
  rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many payment requests from this IP',
    standardHeaders: true,
    legacyHeaders: false,
  })
];

// Payment processing endpoint
app.post('/api/v1/payments', 
  securityMiddleware,
  [
    body('amount')
      .isNumeric()
      .isFloat({ min: 0.01, max: 999999.99 })
      .withMessage('Invalid amount'),
    body('currency')
      .isLength({ min: 3, max: 3 })
      .isAlpha()
      .toUpperCase()
      .withMessage('Invalid currency code'),
    body('paymentToken')
      .isLength({ min: 64, max: 64 })
      .isHexadecimal()
      .withMessage('Invalid payment token'),
  ],
  validateRequest,
  authenticateUser,
  processPayment
);

async function validateRequest(req: express.Request, res: express.Response, next: express.NextFunction) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  next();
}
```

## 🏛️ PCI DSS Compliance

### Requirements Overview

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| 1. Firewall | Network security controls | WAF, network segmentation |
| 2. Passwords | Strong authentication | MFA, password policies |
| 3. Card Data | Protect stored data | Encryption, tokenization |
| 4. Encryption | Secure transmission | TLS 1.3, certificate pinning |
| 5. Antivirus | Malware protection | Regular scanning, updates |
| 6. Secure Systems | Vulnerability management | Patch management, testing |
| 7. Access Control | Restrict data access | RBAC, least privilege |
| 8. Authentication | Identify users | Unique IDs, strong auth |
| 9. Physical Access | Restrict physical access | Data center security |
| 10. Logging | Monitor access | Audit trails, log analysis |
| 11. Testing | Regular security testing | Penetration testing, scans |
| 12. Policy | Information security policy | Documented procedures |

### PCI DSS Implementation Example

```typescript
// PCI DSS Compliant Payment Processor
class PCICompliantPaymentProcessor {
  
  // Requirement 3: Protect stored cardholder data
  private async tokenizeCard(cardData: CardData): Promise<string> {
    // Never store raw PAN
    const token = await this.tokenService.createToken(cardData);
    
    // Log the operation (Requirement 10)
    await this.auditLogger.log({
      action: 'CARD_TOKENIZATION',
      userId: cardData.userId,
      timestamp: new Date(),
      result: 'SUCCESS',
      // Never log sensitive data
      metadata: { tokenId: token.id }
    });
    
    return token.id;
  }
  
  // Requirement 4: Encrypt transmission of cardholder data
  private async secureTransmission(paymentData: PaymentData): Promise<void> {
    const encryptedData = await this.encrypt(paymentData, {
      algorithm: 'AES-256-GCM',
      keyRotation: true,
      certificatePinning: true
    });
    
    // Send via TLS 1.3 only
    await this.httpClient.post(this.getProcessorUrl(), encryptedData, {
      httpsAgent: new https.Agent({
        minVersion: 'TLSv1.3',
        ciphers: 'ECDHE-RSA-AES256-GCM-SHA384'
      })
    });
  }
  
  // Requirement 7: Restrict access to cardholder data
  @RequireRole(['PAYMENT_PROCESSOR', 'ADMIN'])
  @AuditAccess
  async processPayment(paymentRequest: PaymentRequest): Promise<PaymentResult> {
    // Validate user permissions
    if (!await this.hasPermission(paymentRequest.userId, 'PROCESS_PAYMENT')) {
      throw new ForbiddenError('Insufficient permissions');
    }
    
    // Process payment with full audit trail
    return await this.executePayment(paymentRequest);
  }
}
```

## 🔒 Cryptographic Security

### Encryption Standards

```typescript
import crypto from 'crypto';

class CryptographicService {
  private static readonly ALGORITHM = 'aes-256-gcm';
  private static readonly IV_LENGTH = 16;
  private static readonly TAG_LENGTH = 16;
  
  /**
   * Encrypt sensitive data with AES-256-GCM
   */
  static encrypt(plaintext: string, key: Buffer): EncryptedData {
    const iv = crypto.randomBytes(CryptographicService.IV_LENGTH);
    const cipher = crypto.createCipher(CryptographicService.ALGORITHM, key, { iv });
    
    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const tag = cipher.getAuthTag();
    
    return {
      iv: iv.toString('hex'),
      encrypted,
      tag: tag.toString('hex')
    };
  }
  
  /**
   * Decrypt data with integrity verification
   */
  static decrypt(encryptedData: EncryptedData, key: Buffer): string {
    const decipher = crypto.createDecipher(
      CryptographicService.ALGORITHM, 
      key, 
      { iv: Buffer.from(encryptedData.iv, 'hex') }
    );
    
    decipher.setAuthTag(Buffer.from(encryptedData.tag, 'hex'));
    
    let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
  
  /**
   * Generate cryptographically secure random values
   */
  static generateSecureRandom(length: number): string {
    return crypto.randomBytes(length).toString('hex');
  }
}
```

### Key Management

```typescript
import { KMSClient, EncryptCommand, DecryptCommand } from '@aws-sdk/client-kms';

class KeyManagementService {
  private kmsClient: KMSClient;
  private keyId: string;
  
  constructor() {
    this.kmsClient = new KMSClient({ region: process.env.AWS_REGION });
    this.keyId = process.env.KMS_KEY_ID!;
  }
  
  /**
   * Encrypt data using AWS KMS
   */
  async encryptWithKMS(plaintext: string): Promise<string> {
    const command = new EncryptCommand({
      KeyId: this.keyId,
      Plaintext: Buffer.from(plaintext, 'utf8')
    });
    
    const response = await this.kmsClient.send(command);
    return Buffer.from(response.CiphertextBlob!).toString('base64');
  }
  
  /**
   * Decrypt data using AWS KMS
   */
  async decryptWithKMS(ciphertext: string): Promise<string> {
    const command = new DecryptCommand({
      CiphertextBlob: Buffer.from(ciphertext, 'base64')
    });
    
    const response = await this.kmsClient.send(command);
    return Buffer.from(response.Plaintext!).toString('utf8');
  }
  
  /**
   * Rotate encryption keys regularly
   */
  async rotateKeys(): Promise<void> {
    // Implement key rotation logic
    // Schedule this to run monthly
  }
}
```

## 🔍 Fraud Detection and Prevention

### Real-time Fraud Scoring

```typescript
interface FraudSignal {
  name: string;
  value: number;
  weight: number;
  threshold: number;
}

class FraudDetectionEngine {
  
  /**
   * Calculate fraud risk score
   */
  async calculateFraudScore(transaction: Transaction): Promise<FraudScore> {
    const signals: FraudSignal[] = [
      await this.checkVelocity(transaction),
      await this.checkGeolocation(transaction),
      await this.checkDeviceFingerprint(transaction),
      await this.checkAmountPattern(transaction),
      await this.checkMerchantRisk(transaction)
    ];
    
    const totalScore = signals.reduce((sum, signal) => {
      return sum + (signal.value * signal.weight);
    }, 0);
    
    return {
      score: Math.min(totalScore, 100),
      signals,
      riskLevel: this.getRiskLevel(totalScore),
      action: this.getRecommendedAction(totalScore)
    };
  }
  
  /**
   * Check transaction velocity patterns
   */
  private async checkVelocity(transaction: Transaction): Promise<FraudSignal> {
    const recentTransactions = await this.getRecentTransactions(
      transaction.userId, 
      '1 hour'
    );
    
    const velocityScore = Math.min(recentTransactions.length * 10, 100);
    
    return {
      name: 'velocity',
      value: velocityScore,
      weight: 0.3,
      threshold: 50
    };
  }
  
  /**
   * Analyze geolocation patterns
   */
  private async checkGeolocation(transaction: Transaction): Promise<FraudSignal> {
    const userLocation = await this.getUserLocation(transaction.userId);
    const transactionLocation = transaction.location;
    
    const distance = this.calculateDistance(userLocation, transactionLocation);
    const locationScore = distance > 1000 ? 80 : distance / 12.5;
    
    return {
      name: 'geolocation',
      value: locationScore,
      weight: 0.25,
      threshold: 60
    };
  }
}
```

### Machine Learning Integration

```typescript
import * as tf from '@tensorflow/tfjs-node';

class MLFraudDetection {
  private model: tf.LayersModel | null = null;
  
  async loadModel(): Promise<void> {
    this.model = await tf.loadLayersModel('file://./models/fraud-detection/model.json');
  }
  
  /**
   * Predict fraud probability using trained ML model
   */
  async predictFraud(features: TransactionFeatures): Promise<number> {
    if (!this.model) {
      throw new Error('Model not loaded');
    }
    
    // Normalize features
    const normalizedFeatures = this.normalizeFeatures(features);
    
    // Convert to tensor
    const inputTensor = tf.tensor2d([normalizedFeatures]);
    
    // Make prediction
    const prediction = this.model.predict(inputTensor) as tf.Tensor;
    const fraudProbability = await prediction.data();
    
    // Clean up tensors
    inputTensor.dispose();
    prediction.dispose();
    
    return fraudProbability[0];
  }
  
  /**
   * Feature engineering for ML model
   */
  private normalizeFeatures(features: TransactionFeatures): number[] {
    return [
      features.amount / 10000,              // Normalized amount
      features.dayOfWeek / 7,               // Day of week
      features.hourOfDay / 24,              // Hour of day
      features.merchantCategory / 100,       // Merchant category
      features.userAgeInDays / 365,         // User age
      features.avgTransactionAmount / 10000, // Average transaction amount
      features.transactionCount / 1000       // Transaction count
    ];
  }
}
```

## 🛡️ API Security Implementation

### Authentication and Authorization

```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

class SecurityMiddleware {
  
  /**
   * JWT-based authentication
   */
  static authenticateToken(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: 'Access token required' });
    }
    
    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET!, (err: any, user: any) => {
      if (err) {
        return res.status(403).json({ error: 'Invalid or expired token' });
      }
      
      req.user = user;
      next();
    });
  }
  
  /**
   * Role-based authorization
   */
  static requireRole(roles: string[]) {
    return (req: Request, res: Response, next: NextFunction) => {
      if (!req.user || !roles.includes(req.user.role)) {
        return res.status(403).json({ error: 'Insufficient permissions' });
      }
      next();
    };
  }
  
  /**
   * Request signing verification
   */
  static verifySignature(req: Request, res: Response, next: NextFunction) {
    const signature = req.headers['x-signature'] as string;
    const timestamp = req.headers['x-timestamp'] as string;
    const payload = JSON.stringify(req.body);
    
    // Check timestamp to prevent replay attacks
    const requestTime = parseInt(timestamp);
    const currentTime = Date.now();
    if (Math.abs(currentTime - requestTime) > 300000) { // 5 minutes
      return res.status(400).json({ error: 'Request timestamp too old' });
    }
    
    // Verify signature
    const expectedSignature = SecurityMiddleware.generateSignature(payload, timestamp);
    if (signature !== expectedSignature) {
      return res.status(400).json({ error: 'Invalid request signature' });
    }
    
    next();
  }
  
  private static generateSignature(payload: string, timestamp: string): string {
    const hmac = crypto.createHmac('sha256', process.env.WEBHOOK_SECRET!);
    hmac.update(timestamp + payload);
    return hmac.digest('hex');
  }
}
```

## 📊 Security Monitoring and Alerting

### Real-time Security Monitoring

```typescript
class SecurityMonitor {
  private alertThresholds = {
    failedLogins: 5,
    suspiciousTransactions: 10,
    apiRateLimit: 1000
  };
  
  /**
   * Monitor authentication failures
   */
  async monitorAuthFailures(userId: string): Promise<void> {
    const failureCount = await this.getFailureCount(userId, '5 minutes');
    
    if (failureCount >= this.alertThresholds.failedLogins) {
      await this.sendSecurityAlert({
        type: 'AUTHENTICATION_FAILURE',
        severity: 'HIGH',
        userId,
        details: `${failureCount} failed login attempts in 5 minutes`
      });
      
      // Temporarily lock account
      await this.lockAccount(userId, '15 minutes');
    }
  }
  
  /**
   * Monitor suspicious transaction patterns
   */
  async monitorTransactionPatterns(): Promise<void> {
    const suspiciousTransactions = await this.getSuspiciousTransactions('1 hour');
    
    if (suspiciousTransactions.length >= this.alertThresholds.suspiciousTransactions) {
      await this.sendSecurityAlert({
        type: 'SUSPICIOUS_PATTERN',
        severity: 'MEDIUM',
        details: `${suspiciousTransactions.length} suspicious transactions detected`
      });
    }
  }
  
  /**
   * Send security alerts to appropriate channels
   */
  private async sendSecurityAlert(alert: SecurityAlert): Promise<void> {
    // Send to security team
    await this.notificationService.sendSlackAlert('#security-alerts', alert);
    
    // Log to security information and event management (SIEM)
    await this.siemService.logEvent(alert);
    
    // For high severity, send SMS to on-call engineer
    if (alert.severity === 'HIGH') {
      await this.notificationService.sendSMS(process.env.ONCALL_PHONE!, alert);
    }
  }
}
```

## 🧪 Security Testing

### Automated Security Testing

```typescript
// Security test suite
describe('Payment Security Tests', () => {
  
  describe('Input Validation', () => {
    it('should reject invalid card numbers', async () => {
      const invalidCard = '1234567890123456'; // Invalid Luhn
      const response = await request(app)
        .post('/api/v1/payments')
        .send({ cardNumber: invalidCard })
        .expect(400);
      
      expect(response.body.error).toContain('Invalid card number');
    });
    
    it('should prevent SQL injection attempts', async () => {
      const maliciousInput = "'; DROP TABLE users; --";
      const response = await request(app)
        .post('/api/v1/payments')
        .send({ merchantId: maliciousInput })
        .expect(400);
      
      expect(response.body.error).toContain('Invalid input');
    });
  });
  
  describe('Authentication Security', () => {
    it('should require valid JWT token', async () => {
      await request(app)
        .post('/api/v1/payments')
        .send(validPaymentData)
        .expect(401);
    });
    
    it('should reject expired tokens', async () => {
      const expiredToken = jwt.sign({ userId: 1 }, 'secret', { expiresIn: '-1h' });
      
      await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${expiredToken}`)
        .send(validPaymentData)
        .expect(403);
    });
  });
  
  describe('Rate Limiting', () => {
    it('should enforce rate limits', async () => {
      const token = generateValidToken();
      
      // Send requests up to limit
      for (let i = 0; i < 100; i++) {
        await request(app)
          .post('/api/v1/payments')
          .set('Authorization', `Bearer ${token}`)
          .send(validPaymentData);
      }
      
      // 101st request should be rate limited
      await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${token}`)
        .send(validPaymentData)
        .expect(429);
    });
  });
});
```

## 📚 Security Checklist

### Pre-Production Security Review

- [ ] **Data Protection**
  - [ ] No raw card data storage
  - [ ] Encryption at rest and in transit
  - [ ] Secure key management
  - [ ] Data retention policies

- [ ] **Access Control**
  - [ ] Strong authentication (MFA)
  - [ ] Role-based access control
  - [ ] Principle of least privilege
  - [ ] Regular access reviews

- [ ] **Network Security**
  - [ ] TLS 1.3 for all communications
  - [ ] Certificate pinning
  - [ ] Web Application Firewall (WAF)
  - [ ] Network segmentation

- [ ] **Monitoring and Alerting**
  - [ ] Real-time fraud detection
  - [ ] Security event monitoring
  - [ ] Audit logging
  - [ ] Incident response procedures

- [ ] **Compliance**
  - [ ] PCI DSS compliance validated
  - [ ] SOX controls implemented
  - [ ] GDPR privacy controls
  - [ ] Regular compliance audits

## 🚨 Incident Response

### Security Incident Handling

```typescript
class IncidentResponse {
  
  /**
   * Handle security incident
   */
  async handleSecurityIncident(incident: SecurityIncident): Promise<void> {
    // 1. Immediate containment
    await this.containIncident(incident);
    
    // 2. Notify stakeholders
    await this.notifyStakeholders(incident);
    
    // 3. Investigate and document
    await this.investigateIncident(incident);
    
    // 4. Implement remediation
    await this.remediateIncident(incident);
    
    // 5. Post-incident review
    await this.conductPostIncidentReview(incident);
  }
  
  private async containIncident(incident: SecurityIncident): Promise<void> {
    switch (incident.type) {
      case 'DATA_BREACH':
        await this.isolateAffectedSystems();
        await this.revokeCompromisedCredentials();
        break;
      case 'FRAUD_DETECTED':
        await this.blockSuspiciousTransactions();
        await this.freezeAffectedAccounts();
        break;
      case 'SYSTEM_COMPROMISE':
        await this.shutdownAffectedServices();
        await this.preserveForensicEvidence();
        break;
    }
  }
}
```

---

*This guide is part of the comprehensive AI-driven development course. For implementation examples, see the [sample application](../../sample-app/README.md).*