export default async (req: Request) => {
  try {
    // Parse the request body and log it for debugging
    const payload = await req.json();
    console.log("Service key set:", Boolean(Deno.env.get("SERVICE_KEY")));
    console.log("Received payload:", JSON.stringify(payload));

    // Extract the `file` path from the new record in the payload
    const { new: newRecord } = payload;
    const filePath = newRecord.file;

    // Your existing logic for handling the request
    const storageUrl = `${Deno.env.get("SUPABASE_DB_URL")}/storage/v1/object/info/${Deno.env.get("STORAGE_BUCKET_NAME")}/${filePath}`;

    const response = await fetch(storageUrl, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${Deno.env.get("SERVICE_KEY")}`
      }
    });

    if (!response.ok) {
      const responseText = await response.text();
      console.error(`Error fetching metadata. Status: ${response.status}. Response: ${responseText}`);
      throw new Error(`Failed to fetch file metadata: ${response.statusText}`);
    }

    const fileMetadata = await response.json();
    return new Response(JSON.stringify({ metadata: fileMetadata }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("Error processing request:", err.message);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
};
