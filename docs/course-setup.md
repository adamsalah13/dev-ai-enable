# Course Setup Guide

## 🎯 Overview

This guide will help you set up your development environment for the AI-Driven End-to-End CI/CD course. Follow these steps to ensure you have all the necessary tools and configurations.

## 📋 Prerequisites

### Required Accounts
- [ ] GitHub account with Copilot subscription
- [ ] VSCode or Cursor IDE installed
- [ ] Git installed and configured
- [ ] Node.js 18+ installed
- [ ] Docker Desktop installed

### Optional but Recommended
- [ ] Stripe test account (for payment features)
- [ ] SendGrid account (for email features)
- [ ] Postman account (for API testing)

## 🛠️ Environment Setup

### 1. Fork and Clone Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/dev-ai-enable.git
cd dev-ai-enable

# Add upstream remote for updates
git remote add upstream https://github.com/adamsalah13/dev-ai-enable.git
```

### 2. VSCode Setup

#### Install Required Extensions

```bash
# Core AI extensions
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat

# Development extensions
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-json

# Documentation extensions
code --install-extension yzhang.markdown-all-in-one
code --install-extension bierner.markdown-mermaid
code --install-extension jebbs.plantuml

# DevOps extensions
code --install-extension ms-vscode.vscode-docker
code --install-extension hashicorp.terraform
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools

# Testing extensions
code --install-extension ms-playwright.playwright
code --install-extension cypress-io.vscode-cypress
code --install-extension humao.rest-client
```

#### Configure VSCode Settings

Create `.vscode/settings.json` in your project:

```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": false,
    "markdown": true
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "emmet.includeLanguages": {
    "javascript": "javascriptreact",
    "typescript": "typescriptreact"
  },
  "files.associations": {
    "*.env.example": "dotenv",
    "Dockerfile.*": "dockerfile"
  }
}
```

### 3. Cursor IDE Setup (Alternative)

If you prefer Cursor IDE:

1. Download from https://cursor.sh/
2. Import your VSCode settings
3. Configure AI model preferences:
   - Go to Settings → AI
   - Select preferred model (GPT-4, Claude, etc.)
   - Configure context window size
4. Set up GitHub integration

### 4. Sample Application Setup

```bash
# Navigate to sample app
cd sample-app

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# STRIPE_SECRET_KEY=sk_test_...
# SENDGRID_API_KEY=SG...
# DATABASE_URL=postgresql://...
```

### 5. Docker Environment

```bash
# Start development services
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs if needed
docker-compose logs -f
```

### 6. Database Setup

```bash
# Run migrations
npm run migrate

# Seed test data
npm run seed

# Verify database connection
npm run db:status
```

## 🎯 Persona-Specific Setup

### Business Analyst Setup

```bash
# Install PlantUML for diagrams
npm install -g @plantuml/cli

# Install documentation tools
npm install -g @gitbook/cli

# Set up Miro or Figma for wireframes (optional)
```

### Developer Setup

```bash
# Install additional development tools
npm install -g typescript ts-node nodemon

# Set up database client (optional)
npm install -g @databases/pg-cli

# Install API testing tools
npm install -g newman @postman/newman-reporter-html
```

### DevOps Setup

```bash
# Install Kubernetes CLI
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### QA Setup

```bash
# Install testing frameworks
npm install -g cypress playwright

# Initialize Playwright
npx playwright install

# Install k6 for performance testing
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Documentation Setup

```bash
# Install documentation generators
npm install -g @docusaurus/init swagger-jsdoc

# Install diagram tools
npm install -g mermaid-cli

# Set up static site generator
npx @docusaurus/init@latest init documentation classic
```

## 🔧 AI Tools Configuration

### GitHub Copilot Configuration

1. Ensure you have an active GitHub Copilot subscription
2. Sign in to GitHub in VSCode
3. Test Copilot with a simple code suggestion:

```javascript
// Type this comment and wait for suggestion
// Function to calculate compound interest
```

### Cursor AI Configuration

1. Open Cursor IDE
2. Go to Settings → AI
3. Configure your preferred AI model
4. Test with Ctrl+K (Cmd+K on Mac) to open AI chat

### Copilot Chat Setup

1. Open Command Palette (Ctrl+Shift+P)
2. Type "GitHub Copilot: Open Chat"
3. Test with a simple question:
   ```
   @workspace How do I run the sample application?
   ```

## ✅ Verification Steps

### Test Your Setup

1. **Git and GitHub**:
   ```bash
   git status
   git remote -v
   ```

2. **Node.js and npm**:
   ```bash
   node --version  # Should be 18+
   npm --version
   ```

3. **Docker**:
   ```bash
   docker --version
   docker-compose --version
   ```

4. **Sample Application**:
   ```bash
   cd sample-app
   npm test
   npm run lint
   ```

5. **AI Tools**:
   - Test GitHub Copilot code suggestions
   - Test Copilot Chat responses
   - Test Cursor AI interactions (if using Cursor)

### Common Issues and Solutions

#### Issue: GitHub Copilot not working
**Solution**:
```bash
# Check authentication
gh auth status

# Re-authenticate if needed
gh auth login
```

#### Issue: Docker permission denied
**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or restart
newgrp docker
```

#### Issue: Node modules installation fails
**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Learning Path Setup

### Week 1: Foundation
- [ ] Complete environment setup
- [ ] Explore sample application
- [ ] Test AI tools integration
- [ ] Complete persona-specific setup

### Week 2: Persona Deep Dive
- [ ] Choose primary persona (BA, Dev, DevOps, QA, Docs)
- [ ] Complete persona-specific exercises
- [ ] Practice with AI prompt templates
- [ ] Contribute to sample application

### Week 3: Cross-Persona Collaboration
- [ ] Work with other persona team members
- [ ] Practice handoff workflows
- [ ] Use AI for cross-functional tasks
- [ ] Document learnings and improvements

### Week 4: Advanced Integration
- [ ] Implement end-to-end features
- [ ] Optimize AI workflows
- [ ] Measure productivity improvements
- [ ] Share best practices with team

## 🤝 Getting Help

### Support Channels
- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share experiences
- **Discord/Slack**: Real-time team communication (if available)
- **Weekly Office Hours**: Scheduled help sessions

### Documentation Resources
- [Course README](../README.md)
- [Persona Guides](../personas/)
- [Sample Application Docs](../sample-app/docs/)
- [AI Prompt Templates](../templates/)

### Troubleshooting Resources
- [Common Issues](./troubleshooting.md)
- [FAQ](./faq.md)
- [Best Practices](./best-practices.md)
- [Performance Tips](./performance-tips.md)

## 🔄 Staying Updated

### Regular Updates
```bash
# Fetch updates from upstream
git fetch upstream

# Merge updates to your main branch
git checkout main
git merge upstream/main

# Update dependencies
cd sample-app
npm update
```

### Course Material Updates
- Watch the repository for notifications
- Review weekly announcements
- Participate in community discussions
- Contribute improvements and feedback

---

**Ready to start your AI-driven development journey? 🚀**

Proceed to your chosen persona guide in the [personas](../personas/) directory and begin with Exercise 1!