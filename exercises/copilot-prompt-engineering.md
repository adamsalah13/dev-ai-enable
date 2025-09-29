# GitHub Copilot Prompt Engineering Exercise

## Objective
Learn to write effective prompts for GitHub Copilot to generate high-quality code.

## Prerequisites
- GitHub Copilot enabled in your IDE
- Basic understanding of the programming language you'll use
- Sample project to work with

## Exercise 1: Basic Function Generation
### Task
Generate a function to validate payment card numbers using the Luhn algorithm.

### Prompt Template
```
// Generate a function to validate credit card numbers using Luhn algorithm
// Parameters: cardNumber (string)
// Returns: boolean (true if valid, false if invalid)
// Include input validation and comments
```

### Expected Outcome
- Function with proper parameter validation
- Correct Luhn algorithm implementation
- Clear comments explaining the logic
- Error handling for edge cases

## Exercise 2: Complex Class Generation
### Task
Create a payment processor class with multiple methods.

### Prompt Template
```
// Create a PaymentProcessor class for fintech application
// Methods needed:
// - processPayment(amount, cardInfo, merchant)
// - validatePayment(paymentData)
// - handlePaymentError(error)
// - generateTransactionId()
// Include proper error handling and logging
```

## Exercise 3: Test Generation
### Task
Generate comprehensive tests for your payment functions.

### Prompt Template
```
// Generate unit tests for PaymentProcessor class
// Include:
// - Happy path scenarios
// - Edge cases and error conditions
// - Mock external dependencies
// - Use Jest testing framework
```

## Best Practices
1. Be specific about requirements
2. Include context about the application domain
3. Specify error handling needs
4. Mention testing frameworks or patterns to use
5. Ask for comments and documentation

## Evaluation Criteria
- Code quality and readability
- Proper error handling
- Security considerations
- Test coverage
- Documentation quality

## Next Steps
Apply these techniques to generate code for your assigned project components.
