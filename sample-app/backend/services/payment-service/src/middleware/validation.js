const Joi = require('joi');
const { logger } = require('../utils/logger');

// Payment request validation schema
const paymentRequestSchema = Joi.object({
  amount: Joi.number().positive().precision(2).max(1000000).required()
    .messages({
      'number.positive': 'Amount must be a positive number',
      'number.max': 'Amount cannot exceed $1,000,000',
      'any.required': 'Amount is required'
    }),
  
  currency: Joi.string().length(3).uppercase().valid('USD', 'EUR', 'GBP').required()
    .messages({
      'string.length': 'Currency must be a 3-character code',
      'any.only': 'Currency must be one of USD, EUR, GBP',
      'any.required': 'Currency is required'
    }),
  
  paymentMethod: Joi.object({
    type: Joi.string().valid('card', 'ach', 'wire').required(),
    card: Joi.when('type', {
      is: 'card',
      then: Joi.object({
        token: Joi.string().required().messages({
          'any.required': 'Card token is required for card payments'
        })
      }).required(),
      otherwise: Joi.forbidden()
    }),
    ach: Joi.when('type', {
      is: 'ach',
      then: Joi.object({
        accountToken: Joi.string().required()
      }).required(),
      otherwise: Joi.forbidden()
    })
  }).required(),
  
  description: Joi.string().max(255).optional(),
  
  metadata: Joi.object().pattern(
    Joi.string(),
    Joi.alternatives().try(Joi.string(), Joi.number(), Joi.boolean())
  ).optional()
});

function validatePaymentRequest(req, res, next) {
  const { error, value } = paymentRequestSchema.validate(req.body, {
    abortEarly: false,
    stripUnknown: true
  });

  if (error) {
    const validationErrors = error.details.map(detail => ({
      field: detail.path.join('.'),
      message: detail.message,
      value: detail.context?.value
    }));

    logger.warn('Payment validation failed', {
      requestId: req.requestId,
      errors: validationErrors,
      clientIP: req.ip
    });

    return res.status(400).json({
      error: 'Validation Error',
      message: 'Invalid payment request',
      details: validationErrors,
      requestId: req.requestId,
      timestamp: new Date().toISOString()
    });
  }

  // Replace request body with validated and sanitized data
  req.body = value;
  next();
}

// Card token validation (for demo purposes)
function validateCardToken(token) {
  // In real implementation, this would validate against payment processor
  return token && token.startsWith('tok_') && token.length >= 10;
}

// Amount validation helpers
function validateAmount(amount, currency = 'USD') {
  const minAmounts = {
    'USD': 0.50,
    'EUR': 0.50,
    'GBP': 0.30
  };

  const maxAmounts = {
    'USD': 999999.99,
    'EUR': 999999.99,
    'GBP': 999999.99
  };

  const min = minAmounts[currency] || 0.50;
  const max = maxAmounts[currency] || 999999.99;

  return amount >= min && amount <= max;
}

module.exports = {
  validatePaymentRequest,
  validateCardToken,
  validateAmount,
  paymentRequestSchema
};