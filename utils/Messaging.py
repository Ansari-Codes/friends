from nicegui.ui import run_javascript
import asyncio

async def record_audio(duration: int = 5, timeout: int = 15) -> str:
    js_code = f"""
    new Promise(async (resolve, reject) => {{
        try {{
            const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
            const recorder = new MediaRecorder(stream);
            let chunks = [];
            
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = () => {{
                const blob = new Blob(chunks, {{ type: 'audio/webm' }});
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result.split(',')[1]);
                reader.readAsDataURL(blob);
            }};
            
            recorder.start();
            setTimeout(() => recorder.stop(), {duration} * 1000);
        }} catch(e) {{
            reject(e.toString());
        }}
    }});
    """
    
    try:
        base64_audio: str = await run_javascript(js_code, timeout=timeout)
        if not base64_audio:
            raise RuntimeError("No audio captured.")
        return base64_audio
    except Exception as e:
        raise RuntimeError(f"Recording failed: {e}") from e
