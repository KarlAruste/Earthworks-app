import os
from urllib.parse import quote
import streamlit as st
import boto3
from botocore.client import Config

st.set_page_config(page_title="Earthworks App", layout="wide")

# ----------------- THEME (same dark/orange style) -----------------
st.markdown("""
<style>
.stApp { background-color:#0f1117; color:#e5e7eb; }
section[data-testid="stSidebar"] { background-color:#141821; border-right:1px solid #1f2937; }
section[data-testid="stSidebar"] * { color:#e5e7eb; }
div[role="radiogroup"] > label > div:first-child { display:none; }
div[role="radiogroup"] label { padding:10px 12px; border-radius:10px; margin-bottom:6px; }
div[role="radiogroup"] label:hover { background-color:#1b1f2a; }
div[role="radiogroup"] label:has(input:checked) { background-color:#ff8a00; color:#000; }
h1,h2,h3 { color:#f9fafb; }
.block { background:#1b1f2a; border:1px solid #243042; border-radius:14px; padding:16px; }
.small { color:#9ca3af; font-size:13px; }
.stButton>button { background-color:#ff8a00; color:#000; border-radius:10px; border:none; }
.stButton>button:hover { background-color:#ffa733; }
</style>
""", unsafe_allow_html=True)

# ----------------- R2 (S3) client -----------------
def get_s3():
    endpoint = os.environ.get("R2_ENDPOINT")
    key_id = os.environ.get("R2_ACCESS_KEY_ID")
    secret = os.environ.get("R2_SECRET_ACCESS_KEY")
    region = os.environ.get("R2_REGION", "auto")

    if not endpoint or not key_id or not secret:
        st.error("R2 seaded puudu. Lisa Renderis env var: R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET.")
        st.stop()

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        region_name=region,
        config=Config(signature_version="s3v4"),
    )

BUCKET = os.environ.get("R2_BUCKET", "").strip()

def safe_name(name: str) -> str:
    keep = " ._-()[]{}@+"
    cleaned = "".join(ch for ch in name if ch.isalnum() or ch in keep).strip()
    return cleaned.replace("..", ".") or "unnamed"

def project_prefix(project: str) -> str:
    # "folder" in S3 = key prefix
    p = safe_name(project)
    if not p.endswith("/"):
        p += "/"
    return p

def list_projects(s3):
    # Projects are detected by common prefixes at delimiter "/"
    resp = s3.list_objects_v2(Bucket=BUCKET, Delimiter="/")
    prefixes = [cp["Prefix"].rstrip("/") for cp in resp.get("CommonPrefixes", [])]
    # If bucket empty, CommonPrefixes may be missing
    return sorted(prefixes)

def list_files(s3, prefix: str):
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    items = resp.get("Contents", [])
    files = []
    for it in items:
        key = it["Key"]
        if key.endswith("/"):
            continue
        files.append({
            "key": key,
            "name": key[len(prefix):],
            "size": it["Size"],
        })
    return sorted(files, key=lambda x: x["name"].lower())

def upload_file(s3, prefix: str, file):
    fname = safe_name(file.name)
    key = prefix + fname

    # avoid overwriting: if exists, append _2, _3...
    base, dot, ext = fname.partition(".")
    ext = (dot + ext) if dot else ""
    i = 2
    while True:
        try:
            s3.head_object(Bucket=BUCKET, Key=key)
            # exists -> new key
            key = prefix + f"{base}_{i}{ext}"
            i += 1
        except Exception:
            break

    s3.put_object(Bucket=BUCKET, Key=key, Body=file.getbuffer())
    return key

def download_bytes(s3, key: str) -> bytes:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return obj["Body"].read()

def delete_key(s3, key: str):
    s3.delete_object(Bucket=BUCKET, Key=key)

def ensure_project_marker(s3, prefix: str):
    # creates a "folder marker" so the project shows up even if empty
    marker = prefix
    try:
        s3.put_object(Bucket=BUCKET, Key=marker, Body=b"")
    except Exception:
        pass

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("## 🏗 Earthworks")
st.sidebar.caption("Kaevetööde kalkulaator")
st.sidebar.divider()

page = st.sidebar.radio(
    "",
    ["📁 Projects", "📐 Volumes", "🚜 Machines", "👷 Workers", "📊 Reports", "⚙️ Settings"],
)
st.sidebar.divider()
st.sidebar.caption("v0.1 • arenduses")

# ----------------- PAGES -----------------
if page == "📁 Projects":
    st.title("Projects")
    st.write("Projektide loetelu ja failide haldus (Cloudflare R2).")

    if not BUCKET:
        st.error("R2_BUCKET env var on puudu (Render Settings → Environment).")
        st.stop()

    s3 = get_s3()

    # --- Project selector / create ---
    st.markdown('<div class="block">', unsafe_allow_html=True)

    existing_projects = list_projects(s3)
    colA, colB = st.columns([2, 1])

    with colA:
        selected = st.selectbox("Vali projekt (kaust)", options=["— vali —"] + existing_projects)

    with colB:
        new_project = st.text_input("Uus projekti nimi", placeholder="nt Objekt_01")
        if st.button("➕ Loo projekt", use_container_width=True):
            if not new_project.strip():
                st.warning("Sisesta projekti nimi.")
            else:
                prefix = project_prefix(new_project)
                ensure_project_marker(s3, prefix)
                st.success(f"Loodud: {new_project}")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    # --- Project view ---
    if selected != "— vali —":
        prefix = project_prefix(selected)

        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.subheader(f"📂 {selected}")

        uploads = st.file_uploader(
            "Laadi üles failid (pdf, xlsx, csv, jpg, png, docx jne)",
            accept_multiple_files=True
        )

        if uploads:
            saved = 0
            for up in uploads:
                upload_file(s3, prefix, up)
                saved += 1
            st.success(f"Üles laaditud {saved} faili.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Failid")
        files = list_files(s3, prefix)

        if not files:
            st.info("Selles projektis pole veel faile.")
        else:
            for f in files:
                c1, c2, c3 = st.columns([6, 2, 2])
                with c1:
                    st.write(f"📄 {f['name']}")
                    st.caption(f"{f['size']/1024:.1f} KB")
                with c2:
                    data = download_bytes(s3, f["key"])
                    st.download_button(
                        "⬇️ Laadi alla",
                        data=data,
                        file_name=f["name"],
                        mime="application/octet-stream",
                        key=f"dl_{f['key']}",
                        use_container_width=True
                    )
                with c3:
                    if st.button("🗑️ Kustuta", key=f"del_{f['key']}", use_container_width=True):
                        delete_key(s3, f["key"])
                        st.rerun()

        st.caption("Salvestus: Cloudflare R2 (failid jäävad alles).")

    else:
        st.info("Vali projekt või loo uus projektikaust.")

elif page == "📐 Volumes":
    st.title("Volumes")
    st.write("Siia tuleb mahuarvutus (Excel/LandXML).")

elif page == "🚜 Machines":
    st.title("Machines")
    st.write("Siia tuleb masinate tunnihinnad ja tootlikkused.")

elif page == "👷 Workers":
    st.title("Workers")
    st.write("Siia tuleb tööjõu ja brigaadide osa.")

elif page == "📊 Reports":
    st.title("Reports")
    st.write("Siia tulevad aruanded (Excel/PDF).")

elif page == "⚙️ Settings":
    st.title("Settings")
    st.write("Rakenduse seaded.")
