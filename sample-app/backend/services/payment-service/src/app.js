const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const { v4: uuidv4 } = require('uuid');

const { logger } = require('./utils/logger');
const { validatePaymentRequest } = require('./middleware/validation');
const paymentRoutes = require('./routes/payments');

class PaymentService {
  constructor() {
    this.app = express();
    this.config = this.loadConfiguration();
    this.setupMiddleware();
    this.setupRoutes();
    this.setupErrorHandling();
  }

  loadConfiguration() {
    return {
      port: process.env.PORT || 3002,
      environment: process.env.NODE_ENV || 'development',
      stripeSecretKey: process.env.STRIPE_SECRET_KEY || 'sk_test_...',
      rateLimiting: {
        windowMs: 15 * 60 * 1000, // 15 minutes
        max: 50, // More restrictive for payment service
        message: 'Too many payment requests from this IP'
      }
    };
  }

  setupMiddleware() {
    // Security middleware - Enhanced for payment service
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'none'"], // No scripts allowed for security
          styleSrc: ["'self'"],
          imgSrc: ["'none'"],
        },
      },
      hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
      }
    }));

    // CORS - Restrictive for payment service
    this.app.use(cors({
      origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
      credentials: true,
      methods: ['GET', 'POST'],
      allowedHeaders: ['Content-Type', 'Authorization']
    }));

    this.app.use(compression());
    this.app.use(express.json({ limit: '1mb' })); // Smaller limit for security
    
    // Enhanced logging for compliance
    if (this.config.environment !== 'test') {
      this.app.use(morgan('combined', {
        stream: { write: (message) => logger.info(message.trim()) }
      }));
    }

    // Stricter rate limiting for payment endpoints
    this.app.use(rateLimit(this.config.rateLimiting));

    // Request ID for tracing
    this.app.use((req, res, next) => {
      req.requestId = uuidv4();
      res.setHeader('X-Request-ID', req.requestId);
      next();
    });
  }

  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.status(200).json({
        status: 'healthy',
        service: 'payment-service',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      });
    });

    // Payment routes
    this.app.use('/payments', paymentRoutes);

    // Demo endpoints for development
    this.app.get('/payments/demo', (req, res) => {
      res.json({
        service: 'Payment Service',
        message: 'Demo payment processing endpoint',
        features: [
          'Credit card processing',
          'ACH payments',
          'Fraud detection',
          'PCI DSS compliance',
          'Real-time notifications'
        ]
      });
    });

    this.app.post('/payments/process', validatePaymentRequest, (req, res) => {
      // Demo payment processing
      const { amount, currency, paymentMethod } = req.body;
      
      logger.info(`Processing payment: ${amount} ${currency}`, {
        requestId: req.requestId,
        paymentMethod: paymentMethod?.type
      });

      // Simulate payment processing
      setTimeout(() => {
        res.status(201).json({
          id: uuidv4(),
          status: 'completed',
          amount: amount,
          currency: currency,
          transactionId: `txn_${Date.now()}`,
          processedAt: new Date().toISOString(),
          requestId: req.requestId
        });
      }, Math.random() * 1000 + 500); // 500-1500ms processing time
    });
  }

  setupErrorHandling() {
    // 404 handler
    this.app.use('*', (req, res) => {
      res.status(404).json({
        error: 'Not Found',
        message: 'Payment endpoint not found',
        path: req.originalUrl,
        timestamp: new Date().toISOString()
      });
    });

    // Global error handler
    this.app.use((err, req, res, next) => {
      logger.error('Payment service error:', {
        error: err.message,
        stack: err.stack,
        requestId: req.requestId
      });

      // Don't expose internal errors in production
      const message = this.config.environment === 'production' 
        ? 'Payment processing error' 
        : err.message;

      res.status(err.statusCode || 500).json({
        error: 'Payment Error',
        message: message,
        requestId: req.requestId,
        timestamp: new Date().toISOString()
      });
    });
  }

  start() {
    return new Promise((resolve, reject) => {
      try {
        const server = this.app.listen(this.config.port, () => {
          logger.info(`Payment Service started on port ${this.config.port}`);
          logger.info(`Environment: ${this.config.environment}`);
          resolve(server);
        });

        // Graceful shutdown
        process.on('SIGTERM', () => {
          logger.info('SIGTERM received, shutting down payment service');
          server.close(() => {
            logger.info('Payment service terminated');
            process.exit(0);
          });
        });

      } catch (error) {
        logger.error('Failed to start Payment Service:', error);
        reject(error);
      }
    });
  }

  getApp() {
    return this.app;
  }
}

module.exports = PaymentService;