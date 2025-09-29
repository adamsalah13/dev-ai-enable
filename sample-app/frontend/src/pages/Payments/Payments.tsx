import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { Add as AddIcon, Payment as PaymentIcon } from '@mui/icons-material';

const Payments: React.FC = () => {
  const payments = [
    { id: 'pay_001', amount: '$1,250.00', status: 'completed', date: '2024-01-20', method: 'Card' },
    { id: 'pay_002', amount: '$750.50', status: 'pending', date: '2024-01-20', method: 'ACH' },
    { id: 'pay_003', amount: '$2,100.00', status: 'completed', date: '2024-01-19', method: 'Wire' },
    { id: 'pay_004', amount: '$450.25', status: 'failed', date: '2024-01-19', method: 'Card' },
    { id: 'pay_005', amount: '$3,200.00', status: 'completed', date: '2024-01-18', method: 'ACH' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'pending': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <div>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Payments
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Process and manage payments with AI-powered fraud detection
          </Typography>
        </div>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          size="large"
        >
          New Payment
        </Button>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <PaymentIcon color="primary" />
                <div>
                  <Typography variant="h5" fontWeight="bold">$127,450</Typography>
                  <Typography variant="body2" color="text.secondary">Total Today</Typography>
                </div>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <PaymentIcon color="success" />
                <div>
                  <Typography variant="h5" fontWeight="bold">284</Typography>
                  <Typography variant="body2" color="text.secondary">Successful</Typography>
                </div>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom fontWeight="bold">
            Recent Payments
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Payment ID</TableCell>
                  <TableCell>Amount</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Method</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {payments.map((payment) => (
                  <TableRow key={payment.id}>
                    <TableCell>{payment.id}</TableCell>
                    <TableCell>{payment.amount}</TableCell>
                    <TableCell>
                      <Chip 
                        label={payment.status} 
                        color={getStatusColor(payment.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{payment.date}</TableCell>
                    <TableCell>{payment.method}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Payments;