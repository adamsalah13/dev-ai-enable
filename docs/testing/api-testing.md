# API Testing Guide for Fintech Applications

## 🎯 Overview

This comprehensive guide covers API testing strategies for fintech applications, focusing on security, compliance, performance, and reliability. Learn to implement effective testing practices using modern tools and AI-assisted techniques.

## 🏗️ Testing Pyramid for APIs

### API Testing Strategy

```
    /\
   /  \          E2E Tests (10%)
  /____\         Integration Tests (20%) 
 /      \        Contract Tests (30%)
/__API__\       Unit Tests (40%)
```

**Test Distribution:**
- **Unit Tests (40%)**: Fast, isolated, focused on business logic
- **Contract Tests (30%)**: API contract validation, schema testing
- **Integration Tests (20%)**: Service-to-service communication
- **End-to-End Tests (10%)**: Complete user journeys

## 🔧 Testing Framework Setup

### Jest and Supertest Configuration

```typescript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: [
    '**/tests/**/*.test.ts',
    '**/src/**/*.test.ts'
  ],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/types/**',
    '!src/**/*.test.ts'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  testTimeout: 30000
};
```

### Test Environment Setup

```typescript
// tests/setup.ts
import { Application } from 'express';
import { Server } from 'http';
import { createTestApp } from '../src/app';
import { DatabaseManager } from '../src/database/DatabaseManager';
import { RedisManager } from '../src/cache/RedisManager';

export class TestEnvironment {
  public app: Application;
  public server: Server;
  private databaseManager: DatabaseManager;
  private redisManager: RedisManager;

  async setup(): Promise<void> {
    // Setup test database
    this.databaseManager = new DatabaseManager({
      host: process.env.TEST_DB_HOST || 'localhost',
      port: parseInt(process.env.TEST_DB_PORT || '5433'),
      database: process.env.TEST_DB_NAME || 'fintech_test',
      username: process.env.TEST_DB_USER || 'test',
      password: process.env.TEST_DB_PASSWORD || 'test'
    });

    await this.databaseManager.connect();
    await this.databaseManager.runMigrations();

    // Setup test Redis
    this.redisManager = new RedisManager({
      host: process.env.TEST_REDIS_HOST || 'localhost',
      port: parseInt(process.env.TEST_REDIS_PORT || '6380'),
      db: 1 // Use separate database for tests
    });

    await this.redisManager.connect();

    // Create test app
    this.app = createTestApp({
      database: this.databaseManager,
      redis: this.redisManager
    });

    // Start test server
    this.server = this.app.listen(0); // Use random available port
  }

  async teardown(): Promise<void> {
    if (this.server) {
      this.server.close();
    }
    
    if (this.databaseManager) {
      await this.databaseManager.clearAllTables();
      await this.databaseManager.disconnect();
    }
    
    if (this.redisManager) {
      await this.redisManager.flushAll();
      await this.redisManager.disconnect();
    }
  }

  getServerAddress(): string {
    const address = this.server.address();
    if (typeof address === 'string') {
      return address;
    }
    return `http://localhost:${address?.port}`;
  }
}

// Global test environment
let testEnv: TestEnvironment;

beforeAll(async () => {
  testEnv = new TestEnvironment();
  await testEnv.setup();
});

afterAll(async () => {
  await testEnv.teardown();
});

// Make test environment available globally
global.testEnv = testEnv;
```

## 🔒 Security Testing

### Authentication and Authorization Tests

```typescript
// tests/security/auth.test.ts
import request from 'supertest';
import jwt from 'jsonwebtoken';
import { Application } from 'express';
import { TestEnvironment } from '../setup';

describe('Authentication Security Tests', () => {
  let app: Application;
  let validToken: string;
  let expiredToken: string;

  beforeAll(() => {
    app = global.testEnv.app;
    
    // Generate test tokens
    validToken = jwt.sign(
      { userId: 'test-user-123', role: 'user' },
      process.env.JWT_SECRET || 'test-secret',
      { expiresIn: '1h' }
    );
    
    expiredToken = jwt.sign(
      { userId: 'test-user-123', role: 'user' },
      process.env.JWT_SECRET || 'test-secret',
      { expiresIn: '-1h' } // Expired token
    );
  });

  describe('JWT Token Validation', () => {
    it('should accept valid JWT tokens', async () => {
      const response = await request(app)
        .get('/api/v1/user/profile')
        .set('Authorization', `Bearer ${validToken}`)
        .expect(200);

      expect(response.body.userId).toBe('test-user-123');
    });

    it('should reject expired JWT tokens', async () => {
      const response = await request(app)
        .get('/api/v1/user/profile')
        .set('Authorization', `Bearer ${expiredToken}`)
        .expect(401);

      expect(response.body.error).toContain('expired');
    });

    it('should reject malformed JWT tokens', async () => {
      const response = await request(app)
        .get('/api/v1/user/profile')
        .set('Authorization', 'Bearer invalid.token.here')
        .expect(401);

      expect(response.body.error).toContain('invalid');
    });

    it('should reject requests without authorization header', async () => {
      await request(app)
        .get('/api/v1/user/profile')
        .expect(401);
    });
  });

  describe('Role-Based Access Control', () => {
    it('should allow admin access to admin endpoints', async () => {
      const adminToken = jwt.sign(
        { userId: 'admin-123', role: 'admin' },
        process.env.JWT_SECRET || 'test-secret',
        { expiresIn: '1h' }
      );

      await request(app)
        .get('/api/v1/admin/users')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);
    });

    it('should deny user access to admin endpoints', async () => {
      await request(app)
        .get('/api/v1/admin/users')
        .set('Authorization', `Bearer ${validToken}`)
        .expect(403);
    });
  });

  describe('Rate Limiting', () => {
    it('should enforce rate limits on sensitive endpoints', async () => {
      const endpoint = '/api/v1/auth/login';
      const requests = [];

      // Make multiple requests rapidly
      for (let i = 0; i < 10; i++) {
        requests.push(
          request(app)
            .post(endpoint)
            .send({ email: 'test@example.com', password: 'password' })
        );
      }

      const responses = await Promise.all(requests);
      const rateLimitedResponses = responses.filter(r => r.status === 429);
      
      expect(rateLimitedResponses.length).toBeGreaterThan(0);
    });
  });
});
```

### Input Validation and Sanitization Tests

```typescript
// tests/security/input-validation.test.ts
import request from 'supertest';
import { Application } from 'express';

describe('Input Validation Security Tests', () => {
  let app: Application;
  let authToken: string;

  beforeAll(() => {
    app = global.testEnv.app;
    authToken = generateValidToken();
  });

  describe('SQL Injection Prevention', () => {
    it('should prevent SQL injection in user lookup', async () => {
      const sqlInjectionPayloads = [
        "'; DROP TABLE users; --",
        "' OR 1=1 --",
        "' UNION SELECT * FROM users --",
        "'; DELETE FROM accounts WHERE 1=1; --"
      ];

      for (const payload of sqlInjectionPayloads) {
        const response = await request(app)
          .get(`/api/v1/users/${encodeURIComponent(payload)}`)
          .set('Authorization', `Bearer ${authToken}`)
          .expect(400);

        expect(response.body.error).toContain('Invalid user ID format');
      }
    });

    it('should validate and sanitize search parameters', async () => {
      const response = await request(app)
        .get('/api/v1/transactions')
        .query({ search: "'; DROP TABLE transactions; --" })
        .set('Authorization', `Bearer ${authToken}`)
        .expect(400);

      expect(response.body.error).toContain('Invalid search parameter');
    });
  });

  describe('XSS Prevention', () => {
    it('should sanitize HTML in user input', async () => {
      const xssPayloads = [
        '<script>alert("XSS")</script>',
        '<img src="x" onerror="alert(1)">',
        'javascript:alert("XSS")',
        '<svg onload="alert(1)">'
      ];

      for (const payload of xssPayloads) {
        const response = await request(app)
          .post('/api/v1/user/profile')
          .set('Authorization', `Bearer ${authToken}`)
          .send({ firstName: payload })
          .expect(400);

        expect(response.body.error).toContain('Invalid characters detected');
      }
    });
  });

  describe('Data Validation', () => {
    it('should validate email format strictly', async () => {
      const invalidEmails = [
        'invalid-email',
        '@domain.com',
        'user@',
        'user@domain',
        'user space@domain.com'
      ];

      for (const email of invalidEmails) {
        const response = await request(app)
          .post('/api/v1/auth/register')
          .send({ email, password: 'ValidPassword123!' })
          .expect(400);

        expect(response.body.errors).toContainEqual(
          expect.objectContaining({
            field: 'email',
            message: expect.stringContaining('valid email')
          })
        );
      }
    });

    it('should enforce strong password requirements', async () => {
      const weakPasswords = [
        'password',      // No uppercase, numbers, symbols
        'PASSWORD',      // No lowercase, numbers, symbols  
        '12345678',      // No letters, symbols
        'Pass123',       // Too short
        'Password123'    // No symbols
      ];

      for (const password of weakPasswords) {
        const response = await request(app)
          .post('/api/v1/auth/register')
          .send({ email: 'test@example.com', password })
          .expect(400);

        expect(response.body.errors).toContainEqual(
          expect.objectContaining({
            field: 'password',
            message: expect.stringContaining('password')
          })
        );
      }
    });
  });
});
```

## 💳 Payment API Testing

### Payment Processing Tests

```typescript
// tests/payments/payment-processing.test.ts
import request from 'supertest';
import { Application } from 'express';
import { PaymentTestHelper } from '../helpers/PaymentTestHelper';

describe('Payment Processing API Tests', () => {
  let app: Application;
  let authToken: string;
  let paymentHelper: PaymentTestHelper;

  beforeAll(() => {
    app = global.testEnv.app;
    authToken = generateValidToken();
    paymentHelper = new PaymentTestHelper();
  });

  describe('Credit Card Payments', () => {
    it('should process valid credit card payment', async () => {
      const paymentRequest = {
        amount: 10000, // $100.00 in cents
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: {
            token: paymentHelper.getValidCardToken()
          }
        },
        description: 'Test payment'
      };

      const response = await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send(paymentRequest)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        status: 'completed',
        amount: 10000,
        currency: 'USD',
        transactionId: expect.any(String)
      });

      // Verify payment was recorded in database
      const payment = await paymentHelper.getPaymentById(response.body.id);
      expect(payment.status).toBe('completed');
    });

    it('should handle declined credit card', async () => {
      const paymentRequest = {
        amount: 10000,
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: {
            token: paymentHelper.getDeclinedCardToken()
          }
        }
      };

      const response = await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send(paymentRequest)
        .expect(402);

      expect(response.body).toMatchObject({
        error: 'payment_failed',
        reason: 'card_declined',
        declineCode: expect.any(String)
      });
    });

    it('should validate payment amount limits', async () => {
      const testCases = [
        { amount: 0, expectedError: 'Amount must be greater than 0' },
        { amount: -100, expectedError: 'Amount must be positive' },
        { amount: 100000000, expectedError: 'Amount exceeds maximum limit' }
      ];

      for (const testCase of testCases) {
        const response = await request(app)
          .post('/api/v1/payments')
          .set('Authorization', `Bearer ${authToken}`)
          .send({
            amount: testCase.amount,
            currency: 'USD',
            paymentMethod: {
              type: 'card',
              card: { token: paymentHelper.getValidCardToken() }
            }
          })
          .expect(400);

        expect(response.body.error).toContain(testCase.expectedError);
      }
    });
  });

  describe('Fraud Detection', () => {
    it('should flag suspicious payment patterns', async () => {
      // Simulate rapid successive payments (velocity fraud)
      const paymentRequests = Array(5).fill(null).map(() => ({
        amount: 9999, // Just under $100 threshold
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: paymentHelper.getValidCardToken() }
        }
      }));

      const responses = await Promise.all(
        paymentRequests.map(req =>
          request(app)
            .post('/api/v1/payments')
            .set('Authorization', `Bearer ${authToken}`)
            .send(req)
        )
      );

      // At least one payment should be flagged for review
      const flaggedPayments = responses.filter(r => 
        r.status === 202 && r.body.status === 'pending_review'
      );

      expect(flaggedPayments.length).toBeGreaterThan(0);
    });

    it('should require additional verification for high-risk transactions', async () => {
      const highRiskPayment = {
        amount: 500000, // $5,000
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: paymentHelper.getValidCardToken() }
        },
        billingAddress: {
          country: 'NG' // High-risk country
        }
      };

      const response = await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send(highRiskPayment)
        .expect(202);

      expect(response.body).toMatchObject({
        status: 'pending_verification',
        verificationRequired: true,
        verificationMethods: expect.arrayContaining(['phone', 'email'])
      });
    });
  });

  describe('PCI Compliance', () => {
    it('should never return raw card data in responses', async () => {
      const response = await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          amount: 10000,
          currency: 'USD',
          paymentMethod: {
            type: 'card',
            card: { token: paymentHelper.getValidCardToken() }
          }
        })
        .expect(201);

      const responseString = JSON.stringify(response.body);
      
      // Ensure no card numbers in response
      expect(responseString).not.toMatch(/\d{13,19}/);
      
      // Ensure no CVV in response
      expect(responseString).not.toMatch(/cvv|cvc|cv2/i);
      
      // Ensure card data is masked if present
      if (response.body.paymentMethod?.card) {
        expect(response.body.paymentMethod.card.last4).toMatch(/\d{4}/);
        expect(response.body.paymentMethod.card.number).toBeUndefined();
      }
    });

    it('should log payment events for audit trail', async () => {
      const paymentRequest = {
        amount: 10000,
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: paymentHelper.getValidCardToken() }
        }
      };

      const response = await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send(paymentRequest)
        .expect(201);

      // Verify audit log entry was created
      const auditLogs = await paymentHelper.getAuditLogs(response.body.id);
      expect(auditLogs).toContainEqual(
        expect.objectContaining({
          action: 'PAYMENT_CREATED',
          paymentId: response.body.id,
          userId: expect.any(String),
          timestamp: expect.any(Date)
        })
      );
    });
  });
});
```

### Payment Webhook Testing

```typescript
// tests/payments/webhooks.test.ts
import request from 'supertest';
import crypto from 'crypto';
import { Application } from 'express';

describe('Payment Webhook Tests', () => {
  let app: Application;

  beforeAll(() => {
    app = global.testEnv.app;
  });

  describe('Stripe Webhooks', () => {
    it('should process payment succeeded webhook', async () => {
      const webhookPayload = {
        id: 'evt_test_webhook',
        object: 'event',
        type: 'payment_intent.succeeded',
        data: {
          object: {
            id: 'pi_test_payment_intent',
            status: 'succeeded',
            amount: 10000,
            currency: 'usd',
            metadata: {
              userId: 'test-user-123',
              orderId: 'order-456'
            }
          }
        }
      };

      const signature = generateStripeSignature(webhookPayload);

      const response = await request(app)
        .post('/api/v1/webhooks/stripe')
        .set('Stripe-Signature', signature)
        .send(webhookPayload)
        .expect(200);

      expect(response.body.received).toBe(true);

      // Verify payment status was updated
      const payment = await paymentHelper.getPaymentByStripeId('pi_test_payment_intent');
      expect(payment.status).toBe('completed');
    });

    it('should reject webhooks with invalid signatures', async () => {
      const webhookPayload = {
        id: 'evt_test_webhook',
        type: 'payment_intent.succeeded',
        data: { object: { id: 'pi_test' } }
      };

      await request(app)
        .post('/api/v1/webhooks/stripe')
        .set('Stripe-Signature', 'invalid_signature')
        .send(webhookPayload)
        .expect(400);
    });

    it('should handle duplicate webhook events', async () => {
      const webhookPayload = {
        id: 'evt_duplicate_test',
        type: 'payment_intent.succeeded',
        data: { object: { id: 'pi_duplicate_test' } }
      };

      const signature = generateStripeSignature(webhookPayload);

      // Send same webhook twice
      await request(app)
        .post('/api/v1/webhooks/stripe')
        .set('Stripe-Signature', signature)
        .send(webhookPayload)
        .expect(200);

      await request(app)
        .post('/api/v1/webhooks/stripe')
        .set('Stripe-Signature', signature)
        .send(webhookPayload)
        .expect(200);

      // Verify event was only processed once
      const processedEvents = await paymentHelper.getProcessedWebhookEvents('evt_duplicate_test');
      expect(processedEvents).toHaveLength(1);
    });
  });

  function generateStripeSignature(payload: any): string {
    const timestamp = Math.floor(Date.now() / 1000);
    const payloadString = JSON.stringify(payload);
    const secret = process.env.STRIPE_WEBHOOK_SECRET || 'test_secret';
    
    const signedPayload = `${timestamp}.${payloadString}`;
    const signature = crypto
      .createHmac('sha256', secret)
      .update(signedPayload, 'utf8')
      .digest('hex');
    
    return `t=${timestamp},v1=${signature}`;
  }
});
```

## 📊 Performance Testing

### Load Testing with Artillery

```yaml
# artillery-config.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120  
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"
  variables:
    authToken: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  
scenarios:
  - name: "Payment processing flow"
    weight: 70
    flow:
      - post:
          url: "/api/v1/payments"
          headers:
            Authorization: "{{ authToken }}"
            Content-Type: "application/json"
          json:
            amount: 10000
            currency: "USD"
            paymentMethod:
              type: "card"
              card:
                token: "tok_visa"
          capture:
            - json: "$.id"
              as: "paymentId"
      - get:
          url: "/api/v1/payments/{{ paymentId }}"
          headers:
            Authorization: "{{ authToken }}"
  
  - name: "User profile operations"
    weight: 20
    flow:
      - get:
          url: "/api/v1/user/profile"
          headers:
            Authorization: "{{ authToken }}"
      - put:
          url: "/api/v1/user/profile"
          headers:
            Authorization: "{{ authToken }}"
            Content-Type: "application/json"
          json:
            firstName: "Updated Name"
  
  - name: "Transaction history"
    weight: 10
    flow:
      - get:
          url: "/api/v1/transactions"
          headers:
            Authorization: "{{ authToken }}"
          qs:
            limit: 50
            offset: 0

expectations:
  - http.response_time.p95: 500
  - http.response_time.p99: 1000
  - http.codes.200: 95
  - http.codes.201: 4
  - http.codes.4xx: 1
  - http.codes.5xx: 0
```

### Performance Test Implementation

```typescript
// tests/performance/load-test.test.ts
import { performance } from 'perf_hooks';
import request from 'supertest';
import { Application } from 'express';

describe('Performance Tests', () => {
  let app: Application;
  let authToken: string;

  beforeAll(() => {
    app = global.testEnv.app;
    authToken = generateValidToken();
  });

  describe('Response Time Requirements', () => {
    it('should respond to health checks within 100ms', async () => {
      const iterations = 100;
      const responseTimes: number[] = [];

      for (let i = 0; i < iterations; i++) {
        const start = performance.now();
        
        await request(app)
          .get('/api/v1/health')
          .expect(200);
        
        const end = performance.now();
        responseTimes.push(end - start);
      }

      const averageTime = responseTimes.reduce((a, b) => a + b) / responseTimes.length;
      const p95Time = responseTimes.sort((a, b) => a - b)[Math.floor(iterations * 0.95)];

      expect(averageTime).toBeLessThan(100);
      expect(p95Time).toBeLessThan(200);
    });

    it('should process payments within 3 seconds', async () => {
      const paymentRequest = {
        amount: 10000,
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: 'tok_visa' }
        }
      };

      const start = performance.now();
      
      await request(app)
        .post('/api/v1/payments')
        .set('Authorization', `Bearer ${authToken}`)
        .send(paymentRequest)
        .expect(201);
      
      const end = performance.now();
      const responseTime = end - start;

      expect(responseTime).toBeLessThan(3000);
    });
  });

  describe('Concurrent Request Handling', () => {
    it('should handle concurrent payment requests', async () => {
      const concurrentRequests = 50;
      const paymentRequest = {
        amount: 10000,
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: 'tok_visa' }
        }
      };

      const promises = Array(concurrentRequests).fill(null).map(() =>
        request(app)
          .post('/api/v1/payments')
          .set('Authorization', `Bearer ${authToken}`)
          .send(paymentRequest)
      );

      const start = performance.now();
      const responses = await Promise.all(promises);
      const end = performance.now();

      const successfulResponses = responses.filter(r => r.status === 201);
      const totalTime = end - start;

      expect(successfulResponses.length).toBeGreaterThan(concurrentRequests * 0.95);
      expect(totalTime).toBeLessThan(10000); // Should complete within 10 seconds
    });
  });

  describe('Memory Usage', () => {
    it('should not leak memory during sustained operations', async () => {
      const initialMemory = process.memoryUsage();
      
      // Perform many operations
      for (let i = 0; i < 1000; i++) {
        await request(app)
          .get('/api/v1/health')
          .expect(200);
      }

      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }

      const finalMemory = process.memoryUsage();
      const memoryIncrease = finalMemory.heapUsed - initialMemory.heapUsed;

      // Memory increase should be minimal (less than 10MB)
      expect(memoryIncrease).toBeLessThan(10 * 1024 * 1024);
    });
  });
});
```

## 🔄 Contract Testing with Pact

### Consumer Contract Tests

```typescript
// tests/contracts/payment-consumer.test.ts
import { Pact } from '@pact-foundation/pact';
import { PaymentService } from '../../src/services/PaymentService';

describe('Payment Service Consumer Contract', () => {
  const provider = new Pact({
    consumer: 'api-gateway',
    provider: 'payment-service',
    port: 1234,
    log: path.resolve(process.cwd(), 'logs', 'pact.log'),
    dir: path.resolve(process.cwd(), 'pacts'),
    logLevel: 'INFO'
  });

  beforeAll(async () => {
    await provider.setup();
  });

  afterAll(async () => {
    await provider.finalize();
  });

  describe('Payment Processing', () => {
    it('should process a valid payment', async () => {
      await provider
        .given('payment processor is available')
        .uponReceiving('a request to process payment')
        .withRequest({
          method: 'POST',
          path: '/payments',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': Pact.Matchers.like('Bearer token')
          },
          body: {
            amount: Pact.Matchers.integer(10000),
            currency: Pact.Matchers.like('USD'),
            paymentMethod: {
              type: 'card',
              card: {
                token: Pact.Matchers.like('tok_visa')
              }
            }
          }
        })
        .willRespondWith({
          status: 201,
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            id: Pact.Matchers.uuid(),
            status: 'completed',
            amount: 10000,
            currency: 'USD',
            transactionId: Pact.Matchers.like('txn_12345'),
            createdAt: Pact.Matchers.iso8601DateTime()
          }
        });

      const paymentService = new PaymentService('http://localhost:1234');
      const result = await paymentService.processPayment({
        amount: 10000,
        currency: 'USD',
        paymentMethod: {
          type: 'card',
          card: { token: 'tok_visa' }
        }
      });

      expect(result.status).toBe('completed');
      expect(result.id).toBeDefined();
    });
  });
});
```

### Provider Contract Verification

```typescript
// tests/contracts/payment-provider.test.ts
import { Verifier } from '@pact-foundation/pact';
import { createTestApp } from '../../src/app';

describe('Payment Service Provider Contract', () => {
  let app: any;
  let server: any;

  beforeAll(async () => {
    app = createTestApp();
    server = app.listen(3001);
  });

  afterAll(async () => {
    server.close();
  });

  it('should verify the provider contract', async () => {
    const opts = {
      provider: 'payment-service',
      providerBaseUrl: 'http://localhost:3001',
      pactUrls: [
        path.resolve(__dirname, '../../pacts/api-gateway-payment-service.json')
      ],
      stateHandlers: {
        'payment processor is available': () => {
          // Setup test data for this state
          return Promise.resolve();
        },
        'user has insufficient funds': async () => {
          // Setup user with insufficient balance
          await setupUserWithInsufficientFunds();
        }
      },
      requestFilter: (req: any, res: any, next: any) => {
        // Add authentication for provider verification
        req.headers.authorization = 'Bearer test-token';
        next();
      }
    };

    const verifier = new Verifier(opts);
    await verifier.verifyProvider();
  });
});
```

## 🧪 Test Data Management

### Test Data Factory

```typescript
// tests/helpers/TestDataFactory.ts
import { faker } from '@faker-js/faker';

export class TestDataFactory {
  
  static createUser(overrides: Partial<User> = {}): User {
    return {
      id: faker.datatype.uuid(),
      email: faker.internet.email(),
      firstName: faker.name.firstName(),
      lastName: faker.name.lastName(),
      phone: faker.phone.number(),
      dateOfBirth: faker.date.past(30, new Date('2000-01-01')),
      address: this.createAddress(),
      kycStatus: 'verified',
      createdAt: faker.date.past(),
      updatedAt: faker.date.recent(),
      ...overrides
    };
  }

  static createAddress(overrides: Partial<Address> = {}): Address {
    return {
      street: faker.address.streetAddress(),
      city: faker.address.city(),
      state: faker.address.stateAbbr(),
      zipCode: faker.address.zipCode(),
      country: 'US',
      ...overrides
    };
  }

  static createPayment(overrides: Partial<Payment> = {}): Payment {
    return {
      id: faker.datatype.uuid(),
      userId: faker.datatype.uuid(),
      amount: faker.datatype.number({ min: 100, max: 100000 }),
      currency: faker.finance.currencyCode(),
      status: faker.helpers.arrayElement(['pending', 'completed', 'failed']),
      paymentMethod: 'card',
      description: faker.lorem.sentence(),
      createdAt: faker.date.recent(),
      updatedAt: faker.date.recent(),
      ...overrides
    };
  }

  static createCreditCardToken(): string {
    // Generate test card tokens based on standard test cards
    const testCards = [
      'tok_visa',
      'tok_visa_debit',
      'tok_mastercard',
      'tok_amex',
      'tok_discover'
    ];
    
    return faker.helpers.arrayElement(testCards);
  }

  static createDeclinedCardToken(): string {
    const declinedCards = [
      'tok_chargeDeclined',
      'tok_chargeDeclinedInsufficientFunds',
      'tok_chargeDeclinedLostCard',
      'tok_chargeDeclinedStolenCard'
    ];
    
    return faker.helpers.arrayElement(declinedCards);
  }

  static createTransaction(overrides: Partial<Transaction> = {}): Transaction {
    return {
      id: faker.datatype.uuid(),
      userId: faker.datatype.uuid(),
      accountId: faker.datatype.uuid(),
      type: faker.helpers.arrayElement(['credit', 'debit']),
      amount: faker.datatype.number({ min: 100, max: 50000 }),
      currency: 'USD',
      description: faker.lorem.sentence(),
      category: faker.helpers.arrayElement(['food', 'transport', 'entertainment', 'utilities']),
      createdAt: faker.date.recent(),
      ...overrides
    };
  }
}
```

### Database Seeding for Tests

```typescript
// tests/helpers/DatabaseSeeder.ts
import { DatabaseManager } from '../../src/database/DatabaseManager';
import { TestDataFactory } from './TestDataFactory';

export class DatabaseSeeder {
  constructor(private db: DatabaseManager) {}

  async seedTestData(): Promise<TestDataSeed> {
    const users = await this.seedUsers(10);
    const payments = await this.seedPayments(users, 50);
    const transactions = await this.seedTransactions(users, 200);

    return {
      users,
      payments,
      transactions
    };
  }

  private async seedUsers(count: number): Promise<User[]> {
    const users = Array(count).fill(null).map(() => TestDataFactory.createUser());
    
    for (const user of users) {
      await this.db.query(
        'INSERT INTO users (id, email, first_name, last_name, phone, date_of_birth, kyc_status, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        [user.id, user.email, user.firstName, user.lastName, user.phone, user.dateOfBirth, user.kycStatus, user.createdAt, user.updatedAt]
      );
    }

    return users;
  }

  private async seedPayments(users: User[], count: number): Promise<Payment[]> {
    const payments = Array(count).fill(null).map(() => 
      TestDataFactory.createPayment({
        userId: faker.helpers.arrayElement(users).id
      })
    );

    for (const payment of payments) {
      await this.db.query(
        'INSERT INTO payments (id, user_id, amount, currency, status, payment_method, description, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        [payment.id, payment.userId, payment.amount, payment.currency, payment.status, payment.paymentMethod, payment.description, payment.createdAt, payment.updatedAt]
      );
    }

    return payments;
  }

  async cleanupTestData(): Promise<void> {
    await this.db.query('DELETE FROM transactions WHERE created_at > NOW() - INTERVAL \'1 hour\'');
    await this.db.query('DELETE FROM payments WHERE created_at > NOW() - INTERVAL \'1 hour\'');
    await this.db.query('DELETE FROM users WHERE created_at > NOW() - INTERVAL \'1 hour\'');
  }
}

interface TestDataSeed {
  users: User[];
  payments: Payment[];
  transactions: Transaction[];
}
```

## 📋 Testing Checklist

### Security Testing Checklist

- [ ] **Authentication & Authorization**
  - [ ] JWT token validation (valid, expired, malformed)
  - [ ] Role-based access control enforcement
  - [ ] Session management and timeout
  - [ ] Multi-factor authentication flows

- [ ] **Input Validation**
  - [ ] SQL injection prevention
  - [ ] XSS prevention and sanitization
  - [ ] CSRF protection
  - [ ] Request size limits

- [ ] **API Security**
  - [ ] Rate limiting implementation
  - [ ] CORS configuration
  - [ ] HTTPS enforcement
  - [ ] Security headers validation

### Functional Testing Checklist

- [ ] **Payment Processing**
  - [ ] Valid payment scenarios
  - [ ] Declined payment handling
  - [ ] Fraud detection triggers
  - [ ] Refund processing

- [ ] **User Management**
  - [ ] Registration and verification
  - [ ] Profile updates
  - [ ] KYC workflow
  - [ ] Account management

- [ ] **Data Integrity**
  - [ ] Database transactions
  - [ ] Concurrent access handling
  - [ ] Data validation rules
  - [ ] Audit trail creation

### Performance Testing Checklist

- [ ] **Response Times**
  - [ ] API endpoint latency
  - [ ] Database query performance
  - [ ] External service integration
  - [ ] Error response times

- [ ] **Scalability**
  - [ ] Concurrent user handling
  - [ ] Load balancing effectiveness
  - [ ] Resource utilization
  - [ ] Horizontal scaling validation

- [ ] **Reliability**
  - [ ] Circuit breaker functionality
  - [ ] Retry mechanism validation
  - [ ] Graceful degradation
  - [ ] Disaster recovery testing

---

*This guide is part of the comprehensive AI-driven development course. For deployment testing, see the [Docker Guide](../deployment/docker-guide.md) and [Kubernetes Guide](../deployment/kubernetes-guide.md).*