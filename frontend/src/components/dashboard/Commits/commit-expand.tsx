import { motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

interface CommitExpandButtonProps {
  isExpanded: boolean;
}

export function CommitExpandButton({ isExpanded }: CommitExpandButtonProps) {
  return (
    <motion.div
      animate={{
        rotate: isExpanded ? 180 : 0,
      }}
      transition={{ duration: 0.3 }}
      className="bg-primary/10 text-primary rounded-full p-2 shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.1)]"
    >
      <ChevronDown className="w-6 h-6" />
    </motion.div>
  );
}
