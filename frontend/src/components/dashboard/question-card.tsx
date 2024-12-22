"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

export function QuestionCard() {
  return (
    <motion.div
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay: 0.1 }}
    >
      <Card className="h-full">
        <CardHeader>
          <CardTitle>Ask a question</CardTitle>
          <CardDescription>
            Dionysus has knowledge of the codebase
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Textarea
              placeholder="Which file should I edit to change the home page?"
              className="min-h-[100px] resize-none"
            />
            <Button className="bg-blue-600 hover:bg-blue-700">
              Ask Dionysus!
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
