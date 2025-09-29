import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Transactions: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Transactions
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        View and analyze transaction history with AI-powered insights
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="body1">
            Transaction management interface will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Transactions;