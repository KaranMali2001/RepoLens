'use client';

import { motion } from 'framer-motion';
import { Github, Menu, Star, Terminal } from 'lucide-react';
import Link from 'next/link';
import * as React from 'react';

import { Button } from '@/components/ui/button';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';
import { UserButton } from '@clerk/nextjs';

export default function Navbar() {
  const [isScrolled, setIsScrolled] = React.useState(false);

  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`fixed top-0 z-50 w-full ${
        isScrolled
          ? 'bg-background/80 backdrop-blur-md shadow-sm'
          : 'bg-background'
      } transition-all duration-200`}
    >
      <div className="container flex h-16 items-center justify-between px-4">
        <Link
          href="/"
          className="flex items-center space-x-2 transition-transform hover:scale-105"
        >
          {/* <Terminal className="h-8 w-8 text-primary" /> */}
          <span className="text-xl font-bold tracking-tight">REPOGPT</span>
        </Link>

        <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
          <Link
            href="/dashboard"
            className="text-foreground/60 transition-colors hover:text-foreground"
          >
            Dashboard
          </Link>
          <Link
            href="/chat"
            className="text-foreground/60 transition-colors hover:text-foreground"
          >
            Chat
          </Link>
          <Link
            href="/meeting"
            className="text-foreground/60 transition-colors hover:text-foreground"
          >
            Documentation
          </Link>
          <div className="relative flex items-center space-x-2 rounded-full bg-primary/10 px-4 py-1.5">
            <Star className="h-4 w-4 text-primary" />
            <span className="text-sm font-semibold text-primary">
              1000 Credits
            </span>
          </div>
          <Button
            variant="default"
            size="sm"
            className="group relative overflow-hidden"
          >
            <Github className="mr-2 h-4 w-4" />
            <UserButton />
            <motion.div
              className="absolute inset-0 z-0 bg-primary/20"
              initial={{ x: '100%' }}
              whileHover={{ x: 0 }}
              transition={{ type: 'spring', stiffness: 200, damping: 30 }}
            />
          </Button>
        </nav>

        {/* Mobile Navigation */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent>
            <SheetHeader>
              <SheetTitle>
                <div className="flex items-center space-x-2">
                  <Terminal className="h-6 w-6 text-primary" />
                  <span className="font-bold">REPOGPT</span>
                </div>
              </SheetTitle>
            </SheetHeader>
            <nav className="mt-8 flex flex-col space-y-4">
              <Link
                href="/features"
                className="flex items-center text-lg font-medium"
              >
                Features
              </Link>
              <Link
                href="/pricing"
                className="flex items-center text-lg font-medium"
              >
                Pricing
              </Link>
              <Link
                href="/docs"
                className="flex items-center text-lg font-medium"
              >
                Documentation
              </Link>
              <div className="flex items-center space-x-2 rounded-lg bg-primary/10 p-3">
                <Star className="h-5 w-5 text-primary" />
                <span className="font-semibold text-primary">1000 Credits</span>
              </div>
              <Button className="w-full">
                <Github className="mr-2 h-4 w-4" />
                Sign In
              </Button>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </motion.header>
  );
}
