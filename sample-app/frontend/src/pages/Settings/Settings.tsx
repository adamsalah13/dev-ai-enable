import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Configure system settings and AI parameters
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="body1">
            Settings interface will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;