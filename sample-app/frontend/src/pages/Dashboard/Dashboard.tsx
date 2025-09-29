import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Stack,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  AccountBalance as AccountBalanceIcon,
  Payment as PaymentIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';

interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: React.ReactNode;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, change, changeType, icon }) => {
  const getChangeColor = () => {
    switch (changeType) {
      case 'positive':
        return 'success.main';
      case 'negative':
        return 'error.main';
      default:
        return 'text.secondary';
    }
  };

  return (
    <Card>
      <CardContent>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <div>
            <Typography color="text.secondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h4" component="div" fontWeight="bold">
              {value}
            </Typography>
            <Typography variant="body2" color={getChangeColor()} sx={{ mt: 1 }}>
              {change}
            </Typography>
          </div>
          <Box sx={{ color: 'primary.main', fontSize: 40 }}>
            {icon}
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

const Dashboard: React.FC = () => {
  const metrics = [
    {
      title: 'Total Revenue',
      value: '$2,431,250',
      change: '+12.5% from last month',
      changeType: 'positive' as const,
      icon: <TrendingUpIcon fontSize="inherit" />,
    },
    {
      title: 'Transactions',
      value: '18,492',
      change: '+8.2% from last month',
      changeType: 'positive' as const,
      icon: <PaymentIcon fontSize="inherit" />,
    },
    {
      title: 'Active Accounts',
      value: '3,247',
      change: '+5.1% from last month',
      changeType: 'positive' as const,
      icon: <AccountBalanceIcon fontSize="inherit" />,
    },
    {
      title: 'Security Score',
      value: '98.5%',
      change: 'PCI DSS Compliant',
      changeType: 'neutral' as const,
      icon: <SecurityIcon fontSize="inherit" />,
    },
  ];

  const recentActivities = [
    { id: 1, type: 'Payment', description: 'Payment processed for $1,250.00', time: '2 minutes ago', status: 'completed' },
    { id: 2, type: 'Transfer', description: 'Wire transfer initiated $50,000.00', time: '5 minutes ago', status: 'pending' },
    { id: 3, type: 'Compliance', description: 'KYC verification completed', time: '10 minutes ago', status: 'completed' },
    { id: 4, type: 'Security', description: 'Security scan completed - No issues', time: '15 minutes ago', status: 'completed' },
    { id: 5, type: 'Alert', description: 'Fraud detection triggered review', time: '22 minutes ago', status: 'review' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'pending':
        return 'warning';
      case 'review':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        AI-Enabled Fintech Development Platform Overview
      </Typography>

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <MetricCard {...metric} />
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* System Status */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                System Status
              </Typography>
              <Stack spacing={2}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    API Gateway Performance
                  </Typography>
                  <LinearProgress variant="determinate" value={95} sx={{ mt: 1 }} />
                  <Typography variant="caption" color="text.secondary">
                    95% - Excellent
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Payment Processing
                  </Typography>
                  <LinearProgress variant="determinate" value={98} sx={{ mt: 1 }} />
                  <Typography variant="caption" color="text.secondary">
                    98% - Optimal
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Compliance Monitoring
                  </Typography>
                  <LinearProgress variant="determinate" value={100} sx={{ mt: 1 }} />
                  <Typography variant="caption" color="text.secondary">
                    100% - Fully Compliant
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Security Score
                  </Typography>
                  <LinearProgress variant="determinate" value={99} sx={{ mt: 1 }} />
                  <Typography variant="caption" color="text.secondary">
                    99% - Highly Secure
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Recent Activity
              </Typography>
              <Stack spacing={2}>
                {recentActivities.map((activity) => (
                  <Paper key={activity.id} variant="outlined" sx={{ p: 2 }}>
                    <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1 }}>
                      <Typography variant="body2" fontWeight="medium">
                        {activity.type}
                      </Typography>
                      <Chip 
                        label={activity.status} 
                        size="small" 
                        color={getStatusColor(activity.status) as any}
                      />
                    </Stack>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      {activity.description}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {activity.time}
                    </Typography>
                  </Paper>
                ))}
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Features Showcase */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom fontWeight="bold">
            AI-Enabled Features Available
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="primary">🤖</Typography>
                <Typography variant="body2" fontWeight="medium">AI Fraud Detection</Typography>
                <Typography variant="caption" color="text.secondary">Real-time monitoring</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="primary">📊</Typography>
                <Typography variant="body2" fontWeight="medium">Predictive Analytics</Typography>
                <Typography variant="caption" color="text.secondary">Risk assessment</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="primary">🛡️</Typography>
                <Typography variant="body2" fontWeight="medium">Auto Compliance</Typography>
                <Typography variant="caption" color="text.secondary">Regulatory monitoring</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="primary">💡</Typography>
                <Typography variant="body2" fontWeight="medium">Smart Insights</Typography>
                <Typography variant="caption" color="text.secondary">Business intelligence</Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;