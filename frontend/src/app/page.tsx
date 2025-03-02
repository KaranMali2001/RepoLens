import Link from 'next/link';

export default async function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      Hello App
      <Link href="/sign-in" className="mt-10 text-center text-blue-500">
        Sign In
      </Link>
    </div>
  );
}
