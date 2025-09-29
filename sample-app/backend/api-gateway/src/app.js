const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const { createProxyMiddleware } = require('http-proxy-middleware');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const { logger } = require('./utils/logger');
const { authMiddleware } = require('./middleware/auth');
const { errorHandler } = require('./middleware/errorHandler');
const { validateConfig } = require('./config/validation');

class PayFlowAPIGateway {
  constructor() {
    this.app = express();
    this.config = this.loadConfiguration();
    this.setupMiddleware();
    this.setupRoutes();
    this.setupSwagger();
    this.setupErrorHandling();
  }

  loadConfiguration() {
    const config = {
      port: process.env.PORT || 3000,
      environment: process.env.NODE_ENV || 'development',
      corsOrigins: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3100'],
      services: {
        userService: process.env.USER_SERVICE_URL || 'http://localhost:3001',
        paymentService: process.env.PAYMENT_SERVICE_URL || 'http://localhost:3002',
        transactionService: process.env.TRANSACTION_SERVICE_URL || 'http://localhost:3003',
        notificationService: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:3004',
        complianceService: process.env.COMPLIANCE_SERVICE_URL || 'http://localhost:3005'
      },
      rateLimiting: {
        windowMs: 15 * 60 * 1000, // 15 minutes
        max: 100, // limit each IP to 100 requests per windowMs
        skipSuccessfulRequests: false
      }
    };

    if (validateConfig) {
      validateConfig(config);
    }
    return config;
  }

  setupMiddleware() {
    // Security middleware
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      }
    }));

    // CORS configuration
    this.app.use(cors({
      origin: this.config.corsOrigins,
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
    }));

    // Compression and parsing
    this.app.use(compression());
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));

    // Logging
    if (this.config.environment !== 'test') {
      this.app.use(morgan('combined', {
        stream: { write: (message) => logger.info(message.trim()) }
      }));
    }

    // Rate limiting
    this.app.use(rateLimit(this.config.rateLimiting));
  }

  setupRoutes() {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        environment: this.config.environment,
        version: process.env.npm_package_version || '1.0.0'
      });
    });

    // API versioning and routing
    this.setupAPIRoutes();
  }

  setupAPIRoutes() {
    // Public routes (no auth required)
    this.app.use('/api/v1/auth', (req, res) => {
      res.json({ message: 'Auth service would be proxied here' });
    });

    // Protected routes with basic middleware
    this.app.use('/api/v1/users', this.basicAuth, (req, res) => {
      res.json({ message: 'User service would be proxied here' });
    });

    this.app.use('/api/v1/payments', this.basicAuth, (req, res) => {
      res.json({ message: 'Payment service would be proxied here' });
    });

    this.app.use('/api/v1/transactions', this.basicAuth, (req, res) => {
      res.json({ message: 'Transaction service would be proxied here' });
    });
  }

  basicAuth(req, res, next) {
    // Basic auth check for demo
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      next();
    } else {
      res.status(401).json({ error: 'Authentication required' });
    }
  }

  setupSwagger() {
    const swaggerOptions = {
      definition: {
        openapi: '3.0.0',
        info: {
          title: 'PayFlow API Gateway',
          version: '1.0.0',
          description: 'PayFlow API Gateway - Central entry point for all API requests'
        }
      },
      apis: []
    };

    const swaggerSpec = swaggerJsdoc(swaggerOptions);
    this.app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
  }

  setupErrorHandling() {
    // 404 handler
    this.app.use('*', (req, res) => {
      res.status(404).json({
        error: 'Not Found',
        message: 'The requested resource was not found',
        path: req.originalUrl,
        timestamp: new Date().toISOString()
      });
    });

    // Global error handler
    this.app.use((err, req, res, next) => {
      logger.error('Unhandled error:', err);
      res.status(500).json({
        error: 'Internal Server Error',
        message: 'An unexpected error occurred',
        timestamp: new Date().toISOString()
      });
    });
  }

  start() {
    return new Promise((resolve, reject) => {
      try {
        const server = this.app.listen(this.config.port, () => {
          logger.info(`PayFlow API Gateway started on port ${this.config.port}`);
          logger.info(`Environment: ${this.config.environment}`);
          logger.info(`API Documentation: http://localhost:${this.config.port}/api-docs`);
          resolve(server);
        });

        // Graceful shutdown
        process.on('SIGTERM', () => {
          logger.info('SIGTERM received, shutting down gracefully');
          server.close(() => {
            logger.info('Process terminated');
            process.exit(0);
          });
        });

      } catch (error) {
        logger.error('Failed to start API Gateway:', error);
        reject(error);
      }
    });
  }

  getApp() {
    return this.app;
  }
}

module.exports = PayFlowAPIGateway;