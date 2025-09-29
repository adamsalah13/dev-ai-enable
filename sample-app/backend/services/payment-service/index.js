require('dotenv').config();

const PaymentService = require('./src/app');
const { logger } = require('./src/utils/logger');

async function startServer() {
  try {
    const service = new PaymentService();
    await service.start();
  } catch (error) {
    logger.error('Failed to start Payment Service:', error);
    process.exit(1);
  }
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception in Payment Service:', error);
  process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection in Payment Service:', promise, 'reason:', reason);
  process.exit(1);
});

startServer();