// Define the handler function for the webhook
export default async (req: Request) => {
  try {
    // Parse the incoming request to get the `file` path from the new record
    const { new: newRecord } = await req.json();
    const filePath = newRecord.file;

    // Construct the URL for accessing metadata of the specific file in Supabase Storage
    const storageUrl = `${Deno.env.get("SUPABASE_DB_URL")}/storage/v1/object/info/${Deno.env.get("STORAGE_BUCKET_NAME")}/${filePath}`;

    // Perform a fetch request to retrieve the file metadata
    const response = await fetch(storageUrl, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${Deno.env.get("SERVICE_KEY")}`
      }
    });

    // Handle the response from Supabase
    if (!response.ok) {
      throw new Error(`Failed to fetch file metadata: ${response.statusText}`);
    }

    const fileMetadata = await response.json();

    // Return the file metadata as JSON response
    return new Response(JSON.stringify({ metadata: fileMetadata }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("Error retrieving file metadata:", err.message);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
};
