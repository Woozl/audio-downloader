import { useState } from "react"

const DOWNLOAD_API = "http://localhost:3000/download";

function App() {
  const [url, setUrl] = useState("");

  const handleDownload: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    console.log("submit")

    const params = new URLSearchParams({
      url
    });

    const res = await fetch(`${DOWNLOAD_API}?${params}}`);
    const blob = await res.blob();

    // pull file name out of header
    const contentDisposition = res.headers.get('Content-Disposition')
    let filename = 'unknown_title.mp3';
    if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(contentDisposition);
        if (matches != null && matches[1]) { 
          filename = matches[1].replace(/['"]/g, '');
        }
    }

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
