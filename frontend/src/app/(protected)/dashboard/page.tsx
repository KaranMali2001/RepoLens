import { currentUser } from "@clerk/nextjs/server";
import Image from "next/image";

export default async function Page() {
  const user = await currentUser();
  if (!user) {
    return <div>User not found</div>;
  }
  return (
    <div>
      User ID: {user?.id} <br />
      <Image
        src={user?.imageUrl || ""}
        alt="User Profile"
        width={200}
        height={200}
      />
      <br />
      Full Name : {user?.firstName} {user?.lastName} <br />
      Email : {user?.emailAddresses[0].emailAddress} <br />
    </div>
  );
}
