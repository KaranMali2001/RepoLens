// 'use client';
// import {
//   Sidebar,
//   SidebarContent,
//   SidebarGroup,
//   SidebarGroupContent,
//   SidebarGroupLabel,
//   SidebarHeader,
//   SidebarMenu,
//   SidebarMenuButton,
//   SidebarMenuItem,
//   useSidebar,
// } from '@/components/ui/sidebar';
// import useProject from '@/hooks/use-project';
// import { cn } from '@/lib/utils';
// import {
//   Bot,
//   Calendar,
//   LayoutDashboard,
//   Plus,
//   Presentation,
// } from 'lucide-react';
// import Image from 'next/image';
// import Link from 'next/link';
// import { usePathname } from 'next/navigation';
// import { Button } from './ui/button';
// export function AppSidebar() {
//   const {
//     projects,
//     selectedProjectId,
//     error,
//     isLoading,
//     setSelectedProjectId,
//   } = useProject();
//   const { open } = useSidebar();
//   const items = [
//     {
//       title: 'Dasboard',
//       url: '/dashboard',
//       icon: LayoutDashboard,
//     },
//     {
//       title: 'Q & A',
//       url: '/qa',
//       icon: Bot,
//     },
//     {
//       title: 'Calendar',
//       url: '#',
//       icon: Calendar,
//     },
//     {
//       title: '/Meetings',
//       url: '/meetings',
//       icon: Presentation,
//     },
//   ];

//   const pathname = usePathname();

//   return (
//     <Sidebar collapsible="icon" variant="floating">
//       <SidebarHeader>
//         <div className="flex items-center gap-2 ">
//           <Image src="/logo.png" alt="LOGO" width={40} height={40} />
//           {open && (
//             <h1 className="text-xl font-bold text-primary/80">REPOGPT</h1>
//           )}
//         </div>
//       </SidebarHeader>
//       <SidebarContent>
//         <SidebarGroup>
//           <SidebarGroupLabel>Menu</SidebarGroupLabel>
//           <SidebarGroupContent>
//             <SidebarMenu>
//               {items.map((item) => (
//                 <SidebarMenuItem key={item.title}>
//                   <SidebarMenuButton
//                     asChild
//                     variant="outline"
//                     size="sm"
//                     className="flex items-center gap-2 rounded-md p-2 text-sm outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0"
//                   >
//                     <Link
//                       href={item.url}
//                       className={cn({
//                         'bg-primary text-white': pathname === item.url,
//                       })}
//                     >
//                       <item.icon className="h-4 w-4" />
//                       <span>{item.title}</span>
//                     </Link>
//                   </SidebarMenuButton>
//                 </SidebarMenuItem>
//               ))}
//             </SidebarMenu>
//           </SidebarGroupContent>
//         </SidebarGroup>
//         <SidebarGroup>
//           <SidebarGroupLabel>Your Projects</SidebarGroupLabel>
//           <SidebarMenu>
//             {isLoading && <div>Loading...</div>}
//             {error && <div>Error: {error.message}</div>}
//             {projects?.map((project) => (
//               <SidebarMenuItem key={project.name}>
//                 <SidebarMenuButton asChild>
//                   <div onClick={() => setSelectedProjectId(project.id!)}>
//                     <div
//                       className={cn(
//                         'rounded-sm border size-6 flex items-center justify-center text-sm bg-white text-primary',
//                         {
//                           'bg-primary text-white':
//                             selectedProjectId === project.id,
//                         },
//                       )}
//                     >
//                       {project.name[0].toUpperCase()}
//                     </div>
//                     <span>{project.name}</span>
//                   </div>
//                 </SidebarMenuButton>
//               </SidebarMenuItem>
//             ))}
//             <div className=" h-3"></div>
//             <Link href={'/create-project'}>
//               <Button variant={'outline'} className="w-full">
//                 <Plus />
//                 {open && <div>Create Project </div>}
//               </Button>
//             </Link>
//           </SidebarMenu>
//         </SidebarGroup>
//       </SidebarContent>
//     </Sidebar>
//   );
// }
