import os, sys
import threading
import queue
import json
from typing import Dict, Any
import gradio as gr
from src.gradio_demo import SadTalker  


try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


def toggle_audio_file(choice):
    if choice == False:
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
def ref_video_fn(path_of_ref_video):
    if path_of_ref_video is not None:
        return gr.update(value=True)
    else:
        return gr.update(value=False)

def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):

    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")
        
        with gr.Row():
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", sources="upload", type="filepath", elem_id="img2img_image", width=512)

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload OR TTS'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio", sources="upload", type="filepath")

                        if sys.platform != 'win32' and not in_webui: 
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                                tts = gr.Button('Generate audio',elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])
                            
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        gr.Markdown("need help? please visit our [best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md) for more detials")
                        with gr.Column(variant='panel'):
                            # width = gr.Slider(minimum=64, elem_id="img2img_width", maximum=2048, step=8, label="Manually Crop Width", value=512) # img2img_width
                            # height = gr.Slider(minimum=64, elem_id="img2img_height", maximum=2048, step=8, label="Manually Crop Height", value=512) # img2img_width
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0) # 
                            size_of_image = gr.Radio([256, 512], value=256, label='face model resolution', info="use 256/512 model?") # 
                            preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='preprocess', info="How to handle input image?")
                            is_still_mode = gr.Checkbox(label="Still Mode (fewer head motion, works with preprocess `full`)")
                            batch_size = gr.Slider(label="batch size in generation", step=1, maximum=10, value=2)
                            enhancer = gr.Checkbox(label="GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')
                            
                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4", width=256)

        if warpfn:
            submit.click(
                        fn=warpfn(sad_talker.test), 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )
        else:
            submit.click(
                        fn=sad_talker.test, 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )

    return sadtalker_interface
 

if __name__ == "__main__":
    # Build Gradio UI
    demo = sadtalker_demo()

    # Expose a clean FastAPI endpoint for Postman/clients
    try:
        from uuid import uuid4
        from fastapi import File, UploadFile, Form
        from fastapi.responses import JSONResponse
        from fastapi.exceptions import RequestValidationError
        from fastapi import Request
        from starlette.exceptions import HTTPException as StarletteHTTPException

        app = demo.app

        # In-memory job store (simple, replace with Redis for production)
        JOBS: Dict[str, Dict[str, Any]] = {}
        PROGRESS_CHANNELS: Dict[str, "queue.Queue"] = {}

        def _emit(job_id: str, payload: Dict[str, Any]):
            payload = dict(payload or {})
            payload["job_id"] = job_id
            JOBS[job_id]["progress"] = payload.get("progress", JOBS[job_id].get("progress", 0))
            JOBS[job_id]["last_event"] = payload
            q = PROGRESS_CHANNELS.get(job_id)
            if q:
                try:
                    q.put_nowait(json.dumps(payload))
                except Exception:
                    pass

        def _run_job(job_id: str, src_path: str, aud_path: str, options: Dict[str, Any]):
            try:
                JOBS[job_id]["status"] = "running"

                def progress_cb(evt: Dict[str, Any]):
                    _emit(job_id, evt)

                sad_talker = SadTalker("checkpoints", "src/config", lazy_load=True)
                output_path = sad_talker.test(
                    source_image=src_path,
                    driven_audio=aud_path,
                    preprocess=options.get("preprocess", "crop"),
                    is_still_mode=options.get("still_mode", False) if "is_still_mode" in SadTalker.test.__code__.co_varnames else False,
                    still_mode=options.get("still_mode", False),
                    use_enhancer=options.get("use_enhancer", False),
                    batch_size=options.get("batch_size", 1),
                    size=options.get("size", 256),
                    pose_style=options.get("pose_style", 0),
                    result_dir=options.get("result_dir"),
                    progress_cb=progress_cb,
                )

                if isinstance(output_path, bytes):
                    fixed_path = os.path.join(options.get("result_dir"), "result.mp4")
                    with open(fixed_path, "wb") as f:
                        f.write(output_path)
                    output_path = fixed_path

                output_path = str(output_path)
                JOBS[job_id]["result_path"] = output_path

                # Optional S3 upload
                s3_url = None
                bucket = os.getenv("S3_BUCKET")
                if bucket:
                    try:
                        import boto3
                        from botocore.exceptions import BotoCoreError, ClientError
                        s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
                        key = f"sadtalker/{job_id}.mp4"
                        s3.upload_file(output_path, bucket, key, ExtraArgs={"ContentType": "video/mp4"})
                        region = os.getenv("AWS_REGION") or s3.meta.region_name or "us-east-1"
                        if region == "us-east-1":
                            s3_url = f"https://{bucket}.s3.amazonaws.com/{key}"
                        else:
                            s3_url = f"https://{bucket}.s3-{region}.amazonaws.com/{key}"
                        JOBS[job_id]["s3_url"] = s3_url
                        _emit(job_id, {"stage": "upload", "progress": 95, "message": "Uploaded to S3", "s3_url": s3_url})
                    except Exception as _e:
                        JOBS[job_id]["s3_error"] = str(_e)

                JOBS[job_id]["status"] = "completed"
                _emit(job_id, {"stage": "done", "progress": 100, "message": "Job completed", "output_path": output_path, "s3_url": s3_url})
            except Exception as e:
                JOBS[job_id]["status"] = "error"
                JOBS[job_id]["error"] = str(e)
                _emit(job_id, {"stage": "error", "message": str(e)})

        @app.exception_handler(RequestValidationError)
        async def gradio_validation_exception_handler(request: Request, exc: RequestValidationError):
            # Avoid UTF-8 decode of potential binary by stringifying the error only
            return JSONResponse(status_code=422, content={
                "status": "error",
                "message": str(exc)
            })

        @app.exception_handler(StarletteHTTPException)
        async def gradio_http_exception_handler(request: Request, exc: StarletteHTTPException):
            return JSONResponse(status_code=exc.status_code, content={
                "status": "error",
                "message": str(exc.detail)
            })

        @app.exception_handler(Exception)
        async def gradio_generic_exception_handler(request: Request, exc: Exception):
            return JSONResponse(status_code=500, content={
                "status": "error",
                "message": str(exc)
            })

        @app.post("/api/jobs")
        async def create_job(
            source_image: UploadFile = File(...),
            driven_audio: UploadFile = File(...),
            preprocess: str = Form("crop"),
            still_mode: bool = Form(False),
            use_enhancer: bool = Form(False),
            batch_size: int = Form(1),
            size: int = Form(256),
            pose_style: int = Form(0),
        ):
            try:
                tag = str(uuid4())
                base_dir = os.path.join("results", tag)
                input_dir = os.path.join(base_dir, "input")
                os.makedirs(input_dir, exist_ok=True)

                # Save uploads
                src_path = os.path.join(input_dir, source_image.filename)
                with open(src_path, "wb") as f:
                    f.write(await source_image.read())

                aud_path = os.path.join(input_dir, driven_audio.filename)
                with open(aud_path, "wb") as f:
                    f.write(await driven_audio.read())

                JOBS[tag] = {"status": "queued", "progress": 0, "base_dir": base_dir}
                PROGRESS_CHANNELS[tag] = queue.Queue(maxsize=100)

                options = {
                    "preprocess": preprocess,
                    "still_mode": still_mode,
                    "use_enhancer": use_enhancer,
                    "batch_size": batch_size,
                    "size": size,
                    "pose_style": pose_style,
                    "result_dir": base_dir,
                }

                t = threading.Thread(target=_run_job, args=(tag, src_path, aud_path, options), daemon=True)
                t.start()

                return JSONResponse({"status": "ok", "job_id": tag})
            except Exception as e:
                return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

        @app.get("/api/jobs/{job_id}")
        async def get_job(job_id: str):
            job = JOBS.get(job_id)
            if not job:
                return JSONResponse({"status": "error", "message": "Not found"}, status_code=404)
            resp = {
                "status": job.get("status"),
                "progress": job.get("progress", 0),
                "result_path": job.get("result_path"),
                "s3_url": job.get("s3_url"),
                "error": job.get("error"),
                "last_event": job.get("last_event"),
            }
            return JSONResponse(resp)

        # WebSocket for progress streaming
        try:
            from fastapi import WebSocket

            @app.websocket("/ws/jobs/{job_id}")
            async def ws_job(websocket: WebSocket, job_id: str):
                await websocket.accept()
                if job_id not in PROGRESS_CHANNELS:
                    await websocket.send_text(json.dumps({"error": "unknown job"}))
                    await websocket.close()
                    return
                q = PROGRESS_CHANNELS[job_id]
                # Send initial state
                job = JOBS.get(job_id)
                if job and job.get("last_event"):
                    await websocket.send_text(json.dumps(job["last_event"]))
                try:
                    while True:
                        msg = q.get()
                        await websocket.send_text(msg)
                except Exception:
                    pass
                finally:
                    try:
                        await websocket.close()
                    except Exception:
                        pass
        except Exception:
            # WebSocket unavailable in some environments
            pass
    except Exception as _:
        # If FastAPI is unavailable for any reason, continue with UI only
        pass

    demo.queue()
    demo.launch()


