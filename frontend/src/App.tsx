import { useState } from "react"

// For development, the Vite devserver is a separate process/host than the download server,
// so we set this env var in the devcontainer config. Basically this var becomes: 
//     dev  -> http://localhost:3000/download   // fetch on separate server
//     prod -> /download                        // fetch on same origin
const download_server_url = `${import.meta.env.VITE_LOCAL_DOWNLOAD_SERVER ?? ''}/download`;

function App() {
  const [url, setUrl] = useState("");

  const handleDownload: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
      url
    });
    const res = await fetch(`${download_server_url}?${params}}`);
    const blob = await res.blob();

    // pull file name out of header
    const contentDisposition = res.headers.get('Content-Disposition')
    let filename = contentDisposition?.replace("attachment; filename=", "") ?? "unknown_title.mp3";

    // create a new blob for the file and download it
    const file_url = window.URL.createObjectURL(new Blob([blob]));
    const link = document.createElement("a");
    link.href = file_url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(file_url);
  }

  return (
    <form onSubmit={handleDownload}>
      <input
        type="text"
        placeholder="URL"
        value={url}
        onChange={(e) => { setUrl(e.target.value); }}
      />

      <button
        type="button"
        onClick={async () => { setUrl(await navigator.clipboard.readText()) }}  
      >
        Paste
      </button>

      <br />
      <br />

      <input
        type="submit"
        value="Download"
      />
    </form>
  )
}

export default App
