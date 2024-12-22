"use server";
import { ProjectType } from "@/types";
import { auth } from "@clerk/nextjs/server";
import axios, { AxiosError } from "axios";

export async function createProjects(reqData: ProjectType) {
  console.log("createProjects");
  const { getToken } = await auth();
  const token = await getToken();
  try {
    const res = await axios.post(
      `${process.env.NEXT_PUBLIC_BACKEND_API}users/create-project`,

      JSON.stringify(reqData),
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );

    return res.status === 200 ? res.data : null;
  } catch (error: unknown) {
    if (error instanceof AxiosError) {
      throw new Error(error.response?.data?.message || error.message);
    }

    throw new Error(
      error instanceof Error ? error.message : "An unknown error occurred",
    );
  }
}
