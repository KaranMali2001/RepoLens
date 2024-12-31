'use client';

import { motion } from 'framer-motion';
import { MonitorIcon, UploadIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardTitle, CardDescription } from '@/components/ui/card';

export function MeetingCard() {
  return (
    <motion.div
      initial={{ x: 20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay: 0.2 }}
    >
      <Card className="h-full flex flex-col items-center justify-center text-center p-8 ">
        <MonitorIcon className="h-16 w-16 mb-6 text-gray-400" />
        <CardTitle className="mb-2">Create a new meeting</CardTitle>
        <CardDescription className="mb-6">
          Analyse your meeting with Dionysus.
          <br />
          Powered by AI.
        </CardDescription>
        <Button className="bg-blue-600 hover:bg-blue-700 flex items-center gap-2">
          <UploadIcon className="h-4 w-4" />
          Upload Meeting
        </Button>
      </Card>
    </motion.div>
  );
}
