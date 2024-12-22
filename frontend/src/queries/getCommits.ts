"use server";

import { auth } from "@clerk/nextjs/server";
import axios from "axios";

export async function GetCommits(project_id: number) {
  console.log("inside get commits", project_id);
  const { getToken } = await auth();
  const token = await getToken();
  try {
    const res = await axios.post(
      `${process.env.NEXT_PUBLIC_BACKEND_API}github/commits`,
      JSON.stringify({ project_id }),
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (res.status === 200) {
      console.log("res", res.data);
      return res.data;
    }
    throw new Error("Failed to fetch commits");
  } catch (error) {
    console.log("Error getting commits:", error);
    throw new Error("Failed to fetch commits");
  }
}
