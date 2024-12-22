"use server";
import { ProjectType } from "@/types";
import { auth } from "@clerk/nextjs/server";
import axios from "axios";

export async function fetchProjects() {
  console.log("fetchProjects");
  const { getToken } = await auth();
  const token = await getToken();

  try {
    const data = await axios.get<ProjectType[]>(
      `${process.env.NEXT_PUBLIC_BACKEND_API}users/get-projects`,

      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );

    return data.data;
  } catch (error) {
    console.error("error", error);
    throw error;
  }
}
