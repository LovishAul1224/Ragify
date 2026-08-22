import streamlit.components.v1 as components


def google_drive_picker(
    api_key: str,
    client_id: str,
    app_id: str,
    height: int = 80,
    mime_types: str = "application/pdf",  # can be comma-separated
):
    """
    Google Drive PDF Picker for Streamlit.
    
    NOTE: This version only opens the picker.
    The selected file is sent via postMessage but pure components.html
    cannot return values to Python. See the note at the end for solutions.
    """

    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://apis.google.com/js/api.js"></script>
        <script src="https://accounts.google.com/gsi/client"></script>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            button {{
                width: 100%;
                padding: 12px 16px;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                background: white;
                cursor: pointer;
                font-size: 15px;
                font-weight: 500;
                transition: background 0.15s;
            }}
            button:hover {{
                background: #f5f5f5;
            }}
            button:disabled {{
                opacity: 0.6;
                cursor: not-allowed;
            }}
            #status {{
                margin-top: 8px;
                font-size: 13px;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <button id="pickerBtn" onclick="openPicker()">
            📂 Choose PDF from Google Drive
        </button>
        <div id="status"></div>

        <script>
            const API_KEY = "{api_key}";
            const CLIENT_ID = "{client_id}";
            const APP_ID = "{app_id}";
            const MIME_TYPES = "{mime_types}";

            // drive.file is safer, but many existing files need readonly
            const SCOPES = "https://www.googleapis.com/auth/drive.readonly";

            let tokenClient = null;
            let accessToken = null;
            let pickerInited = false;

            function setStatus(msg) {{
                document.getElementById("status").textContent = msg || "";
            }}

            function initialize() {{
                // Load Google Picker
                gapi.load("picker", {{
                    callback: () => {{
                        pickerInited = true;
                        console.log("Google Picker loaded");
                    }},
                    onerror: () => {{
                        setStatus("❌ Failed to load Google Picker");
                        console.error("Failed to load picker");
                    }}
                }});

                // Initialize OAuth token client
                tokenClient = google.accounts.oauth2.initTokenClient({{
                    client_id: CLIENT_ID,
                    scope: SCOPES,
                    callback: (response) => {{
                        if (response.error) {{
                            console.error("Token error:", response);
                            setStatus("❌ Auth failed: " + (response.error_description || response.error));
                            document.getElementById("pickerBtn").disabled = false;
                            return;
                        }}
                        accessToken = response.access_token;
                        setStatus("");
                        createPicker();
                    }},
                }});
            }}

            function openPicker() {{
                if (!pickerInited) {{
                    setStatus("⏳ Loading Google APIs...");
                    return;
                }}

                document.getElementById("pickerBtn").disabled = true;
                setStatus("⏳ Requesting access...");

                if (!accessToken) {{
                    // Force consent the first time
                    tokenClient.requestAccessToken({{ prompt: "consent" }});
                }} else {{
                    createPicker();
                }}
            }}

            function createPicker() {{
                const view = new google.picker.DocsView(google.picker.ViewId.DOCS)
                    .setMimeTypes(MIME_TYPES)
                    .setIncludeFolders(true)
                    .setSelectFolderEnabled(false);

                const picker = new google.picker.PickerBuilder()
                    .setDeveloperKey(API_KEY)
                    .setAppId(APP_ID)
                    .setOAuthToken(accessToken)
                    .addView(view)
                    // Optional: allow uploading too
                    // .addView(new google.picker.DocsUploadView())
                    .setOrigin(window.location.protocol + "//" + window.location.host)  // FIXED
                    .setCallback(pickerCallback)
                    .build();

                picker.setVisible(true);
                document.getElementById("pickerBtn").disabled = false;
                setStatus("");
            }}

            function pickerCallback(data) {{
                if (data.action === google.picker.Action.PICKED) {{
                    const file = data.docs[0];

                    const result = {{
                        id: file.id,
                        name: file.name,
                        mimeType: file.mimeType,
                        url: file.url || null,
                        sizeBytes: file.sizeBytes || null
                    }};

                    console.log("Selected file:", result);
                    setStatus("✅ Selected: " + result.name);

                    // Send to parent (Streamlit iframe)
                    window.parent.postMessage({{
                        type: "GOOGLE_DRIVE_FILE_SELECTED",
                        file: result
                    }}, "*");
                }}
                else if (data.action === google.picker.Action.CANCEL) {{
                    setStatus("Cancelled");
                }}
            }}

            // Start
            initialize();
        </script>
    </body>
    </html>
    """

    components.html(component_html, height=height)