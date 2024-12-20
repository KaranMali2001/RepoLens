import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { ClerkLoaded, UserButton } from "@clerk/nextjs";

type Props = {
  children: React.ReactNode;
};
const SiderbarLayout = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="w-full m-2">
        <div className=" flex items-center gap=2 border-sidebar-border bg-sidebar border shadow rounded-md p-2 px-4">
          {/* search Bar  */}
          <div className=" ml-auto">
            <div className="">
              <UserButton />
            </div>
          </div>
        </div>
        <div className="h-4"></div>
        <div className="border-sidebar-border bg-sidebar border shadow rounded-md  h-[calc(100vh-6rem)] p-4">
          <ClerkLoaded>{children}</ClerkLoaded>
        </div>
      </main>
    </SidebarProvider>
  );
};
export default SiderbarLayout;
