# PayFlow API Gateway Dockerfile
FROM node:18-alpine AS base

# Install security updates
RUN apk --no-cache add ca-certificates && \
    apk --no-cache update && \
    apk --no-cache upgrade

# Create app directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# Copy package files
COPY package*.json ./
COPY --chown=nodeuser:nodejs . .

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Switch to non-root user
USER nodeuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "index.js"]