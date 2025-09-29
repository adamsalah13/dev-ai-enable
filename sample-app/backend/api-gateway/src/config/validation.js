const Joi = require('joi');

const configSchema = Joi.object({
  port: Joi.number().port().default(3000),
  environment: Joi.string().valid('development', 'staging', 'production').default('development'),
  corsOrigins: Joi.array().items(Joi.string().uri()).min(1),
  services: Joi.object({
    userService: Joi.string().uri().required(),
    paymentService: Joi.string().uri().required(),
    transactionService: Joi.string().uri().required(),
    notificationService: Joi.string().uri().required(),
    complianceService: Joi.string().uri().required()
  }).required(),
  rateLimiting: Joi.object({
    windowMs: Joi.number().positive().required(),
    max: Joi.number().positive().required(),
    skipSuccessfulRequests: Joi.boolean().default(false)
  }).required()
});

function validateConfig(config) {
  const { error, value } = configSchema.validate(config, {
    allowUnknown: true,
    abortEarly: false
  });

  if (error) {
    const errorMessage = error.details.map(detail => detail.message).join(', ');
    throw new Error(`Configuration validation failed: ${errorMessage}`);
  }

  return value;
}

module.exports = { validateConfig };