const express = require('express');
const { validatePaymentRequest } = require('../middleware/validation');
const { logger, auditLogger } = require('../utils/logger');
const { v4: uuidv4 } = require('uuid');

const router = express.Router();

// Demo payment processing endpoint
router.post('/process', validatePaymentRequest, async (req, res) => {
  const { amount, currency, paymentMethod, description, metadata } = req.body;
  const paymentId = uuidv4();
  const transactionId = `txn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  try {
    // Log payment attempt for audit purposes
    auditLogger.info('Payment processing initiated', {
      paymentId,
      amount,
      currency,
      paymentMethodType: paymentMethod.type,
      requestId: req.requestId,
      clientIP: req.ip,
      userAgent: req.get('User-Agent')
    });

    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, Math.random() * 1500 + 500));

    // Simulate different payment outcomes
    const outcomes = ['completed', 'failed', 'pending'];
    const weights = [0.85, 0.10, 0.05]; // 85% success, 10% failure, 5% pending
    const randomValue = Math.random();
    let cumulativeWeight = 0;
    let status = 'completed';

    for (let i = 0; i < outcomes.length; i++) {
      cumulativeWeight += weights[i];
      if (randomValue <= cumulativeWeight) {
        status = outcomes[i];
        break;
      }
    }

    const paymentResult = {
      id: paymentId,
      status: status,
      amount: amount,
      currency: currency,
      transactionId: transactionId,
      paymentMethod: {
        type: paymentMethod.type,
        ...(paymentMethod.type === 'card' && { last4: '4242' }),
        ...(paymentMethod.type === 'ach' && { bankName: 'Demo Bank' })
      },
      description: description,
      metadata: metadata,
      processedAt: new Date().toISOString(),
      requestId: req.requestId
    };

    // Add failure details if payment failed
    if (status === 'failed') {
      const failureReasons = [
        'insufficient_funds',
        'card_declined',
        'invalid_card',
        'processing_error'
      ];
      paymentResult.failureReason = failureReasons[Math.floor(Math.random() * failureReasons.length)];
      paymentResult.failureMessage = 'Payment could not be processed';
    }

    // Log payment result
    auditLogger.info('Payment processing completed', {
      paymentId,
      status,
      transactionId,
      amount,
      currency,
      requestId: req.requestId
    });

    // Return appropriate status code based on result
    const statusCode = status === 'completed' ? 201 : status === 'pending' ? 202 : 400;
    res.status(statusCode).json(paymentResult);

  } catch (error) {
    logger.error('Payment processing error', {
      error: error.message,
      stack: error.stack,
      paymentId,
      requestId: req.requestId
    });

    auditLogger.error('Payment processing failed', {
      paymentId,
      error: error.message,
      requestId: req.requestId
    });

    res.status(500).json({
      error: 'Payment Processing Error',
      message: 'Unable to process payment at this time',
      paymentId: paymentId,
      requestId: req.requestId,
      timestamp: new Date().toISOString()
    });
  }
});

// Get payment status
router.get('/:paymentId', (req, res) => {
  const { paymentId } = req.params;
  
  // Demo payment status lookup
  const demoPayment = {
    id: paymentId,
    status: 'completed',
    amount: 100.00,
    currency: 'USD',
    transactionId: `txn_${Date.now()}`,
    processedAt: new Date().toISOString(),
    paymentMethod: {
      type: 'card',
      last4: '4242'
    }
  };

  logger.info('Payment status requested', {
    paymentId,
    requestId: req.requestId
  });

  res.json(demoPayment);
});

// Refund payment
router.post('/:paymentId/refund', (req, res) => {
  const { paymentId } = req.params;
  const { amount, reason } = req.body;
  const refundId = uuidv4();

  auditLogger.info('Refund initiated', {
    paymentId,
    refundId,
    amount,
    reason,
    requestId: req.requestId
  });

  // Demo refund processing
  const refundResult = {
    id: refundId,
    paymentId: paymentId,
    status: 'completed',
    amount: amount || 100.00,
    currency: 'USD',
    reason: reason || 'requested_by_customer',
    processedAt: new Date().toISOString(),
    requestId: req.requestId
  };

  res.status(201).json(refundResult);
});

// List payments (demo endpoint)
router.get('/', (req, res) => {
  const { limit = 10, offset = 0, status } = req.query;
  
  // Demo payment list
  const payments = Array.from({ length: Math.min(limit, 50) }, (_, i) => ({
    id: uuidv4(),
    status: status || ['completed', 'pending', 'failed'][Math.floor(Math.random() * 3)],
    amount: Math.floor(Math.random() * 1000) + 10,
    currency: 'USD',
    transactionId: `txn_${Date.now() + i}`,
    processedAt: new Date(Date.now() - Math.random() * 86400000 * 30).toISOString(),
    paymentMethod: {
      type: 'card',
      last4: '4242'
    }
  }));

  res.json({
    data: payments,
    pagination: {
      limit: parseInt(limit),
      offset: parseInt(offset),
      total: 1000,
      hasMore: offset + limit < 1000
    }
  });
});

module.exports = router;