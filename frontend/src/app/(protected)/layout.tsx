import Navbar from '@/components/navBar';
import { Providers } from '../providers';

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Providers>
        <Navbar />
        {children}
      </Providers>
    </>
  );
}
